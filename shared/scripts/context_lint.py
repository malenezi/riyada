#!/usr/bin/env python3
"""Check a seven-layer context pack before agents rely on it.

Usage:
    python context_lint.py DIR [--max-age-days 90] [--max-words 900]
                               [--strict] [--format text|json] [--today YYYY-MM-DD]

DIR holds the layer files, named 01-*.md to 07-*.md. If DIR holds language
variants (01-*.en.md and 01-*.ar.md), each language is checked as its own pack.

Exit status: 0 clean, 1 errors found (or warnings with --strict), 2 usage error.
Standard library only. Works with English and Arabic packs.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

RULES = {
    "CTX001": ("error", "Layer file is missing"),
    "CTX002": ("error", "Unfilled placeholder"),
    "CTX003": ("error", "Section has a heading but no content"),
    "CTX004": ("error", "No valid 'Last reviewed' date"),
    "CTX005": ("warning", "Not reviewed within the allowed age"),
    "CTX006": ("warning", "File is long enough to dilute an agent's attention"),
    "CTX007": ("error", "Governance layer has no approval matrix"),
    "CTX008": ("error", "Governance layer has no 'Never' rule"),
    "CTX009": ("error", "Same field has different values in two files"),
    "CTX010": ("warning", "Table cell is empty"),
    "CTX011": ("error", "Possible secret in a context file"),
    "CTX012": ("warning", "Unfinished marker"),
    "CTX013": ("error", "More than one file for the same layer"),
}

LAYER_RE = re.compile(r"^(0[1-7])-.+?(?:\.(en|ar))?\.md$")
PLACEHOLDER_RE = re.compile(r"\{\{.*?\}\}")
REVIEWED_RE = re.compile(
    r"\*\*(?:Last reviewed|Reviewed|Updated|آخر مراجعة|تاريخ المراجعة|آخر تحديث):\*\*\s*(\S+)"
)
FIELD_RE = re.compile(r"^\s*-\s*\*\*(.+?):\*\*\s*(.+?)\s*$")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*\S)\s*$")
NEVER_RE = re.compile(r"\bnever\b|ممنوع|يُمنع|يمنع", re.IGNORECASE)
MARKER_RE = re.compile(r"\b(TODO|TBD|FIXME|XXX)\b|لاحقًا يُحدد|يحدد لاحقا")
SECRET_RES = [
    re.compile(r"\bsk-[A-Za-z0-9_-]{16,}"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"(?i)\b(password|passwd|api[_-]?key|secret|token)\s*[:=]\s*['\"]?[^\s'\"`{<]{8,}"),
]
# Fields that every layer repeats and that are expected to differ.
PER_FILE_FIELDS = {
    "owner", "last reviewed", "reviewed", "updated",
    "المسؤول", "آخر مراجعة", "تاريخ المراجعة", "آخر تحديث",
}


def strip_code(lines):
    """Yield (number, line) outside fenced code blocks."""
    fenced = False
    for i, line in enumerate(lines, 1):
        if line.lstrip().startswith("```"):
            fenced = not fenced
            continue
        if not fenced:
            yield i, line


def is_table_row(line: str) -> bool:
    s = line.strip()
    return s.startswith("|") and s.endswith("|") and len(s) > 2


def is_separator(line: str) -> bool:
    return bool(re.fullmatch(r"\|?[\s:|-]+\|?", line.strip())) and "-" in line


def split_cells(line: str):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def lint_file(path: Path, layer: str, args, today, findings, fields):
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    add = lambda rule, ln, detail: findings.append(
        {"file": str(path), "line": ln, "rule": rule,
         "severity": RULES[rule][0], "message": RULES[rule][1], "detail": detail})

    body = list(strip_code(lines))

    for ln, line in body:
        for m in PLACEHOLDER_RE.finditer(line):
            add("CTX002", ln, m.group(0)[:60])
        m = MARKER_RE.search(line)
        if m:
            add("CTX012", ln, m.group(0))
        for rx in SECRET_RES:
            if rx.search(line):
                add("CTX011", ln, "value hidden")
                break

    # Empty sections: a heading followed by a heading of the same or higher
    # level (or end of file) with nothing in between.
    headings = [(ln, len(m.group(1)), m.group(2))
                for ln, line in body if (m := HEADING_RE.match(line))]
    content_lines = {ln for ln, line in body if line.strip() and not HEADING_RE.match(line)}
    for idx, (ln, level, title) in enumerate(headings):
        if level < 2:
            continue
        end = len(lines) + 1
        for nln, nlevel, _ in headings[idx + 1:]:
            if nlevel <= level:
                end = nln
                break
        if not any(ln < c < end for c in content_lines):
            add("CTX003", ln, title)

    # Review date
    m = REVIEWED_RE.search(text)
    reviewed = None
    if m:
        try:
            reviewed = dt.date.fromisoformat(m.group(1).rstrip(".,،"))
        except ValueError:
            reviewed = None
    if reviewed is None:
        if not (m and PLACEHOLDER_RE.search(m.group(1))):
            add("CTX004", 1, "expected - **Last reviewed:** YYYY-MM-DD")
    else:
        age = (today - reviewed).days
        if age > args.max_age_days:
            add("CTX005", 1, f"{age} days old; limit is {args.max_age_days}")

    words = len(re.findall(r"\S+", text))
    if words > args.max_words:
        add("CTX006", 1, f"{words} words; limit is {args.max_words}")

    # Tables
    data_rows = 0
    for ln, line in body:
        if is_table_row(line) and not is_separator(line):
            cells = split_cells(line)
            data_rows += 1
            # Skip the blank corner cell of a header row and continuation rows
            # where the first cell is intentionally blank.
            if any(c == "" for c in cells[1:]):
                add("CTX010", ln, line.strip()[:60])

    if layer == "06":
        table_blocks, current = [], 0
        for _, line in body:
            if is_table_row(line):
                if not is_separator(line):
                    current += 1
            else:
                if current:
                    table_blocks.append(current)
                current = 0
        if current:
            table_blocks.append(current)
        # header row + at least two rules
        if not any(n >= 3 for n in table_blocks):
            add("CTX007", 1, "add a table of actions with a level for each")
        if not NEVER_RE.search(text):
            add("CTX008", 1, "state at least one action agents must never take")

    for ln, line in body:
        m = FIELD_RE.match(line)
        if not m:
            continue
        key = re.sub(r"\s+", " ", m.group(1).strip().lower())
        val = re.sub(r"\s+", " ", m.group(2).strip())
        if key in PER_FILE_FIELDS or PLACEHOLDER_RE.search(val):
            continue
        fields.setdefault(key, []).append((val, str(path), ln))


def lint_pack(files: dict, label: str, args, today):
    findings = []
    fields: dict = {}
    for layer in ("01", "02", "03", "04", "05", "06", "07"):
        paths = files.get(layer, [])
        if not paths:
            findings.append({"file": label, "line": 0, "rule": "CTX001",
                             "severity": "error", "message": RULES["CTX001"][1],
                             "detail": f"layer {layer}"})
            continue
        if len(paths) > 1:
            findings.append({"file": str(paths[1]), "line": 0, "rule": "CTX013",
                             "severity": "error", "message": RULES["CTX013"][1],
                             "detail": f"layer {layer}: " + ", ".join(p.name for p in paths)})
        for p in paths:
            lint_file(p, layer, args, today, findings, fields)

    for key, entries in fields.items():
        values = {}
        for val, f, ln in entries:
            values.setdefault(val.casefold(), (val, f, ln))
        files_involved = {f for _, f, _ in entries}
        if len(values) > 1 and len(files_involved) > 1:
            shown = "; ".join(f"{Path(f).name}:{ln} = {v[:40]}" for v, f, ln in values.values())
            _, f, ln = entries[-1]
            findings.append({"file": f, "line": ln, "rule": "CTX009",
                             "severity": "error", "message": RULES["CTX009"][1],
                             "detail": f"'{key}': {shown}"})
    return findings


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("directory")
    ap.add_argument("--max-age-days", type=int, default=90)
    ap.add_argument("--max-words", type=int, default=900)
    ap.add_argument("--strict", action="store_true", help="treat warnings as errors")
    ap.add_argument("--format", choices=["text", "json"], default="text")
    ap.add_argument("--today", help="override today's date (YYYY-MM-DD), for tests")
    args = ap.parse_args(argv)

    root = Path(args.directory)
    if not root.is_dir():
        print(f"not a directory: {root}", file=sys.stderr)
        return 2
    today = dt.date.fromisoformat(args.today) if args.today else dt.date.today()

    packs: dict = {}
    for p in sorted(root.iterdir()):
        m = LAYER_RE.match(p.name)
        if m and p.is_file():
            packs.setdefault(m.group(2) or "", {}).setdefault(m.group(1), []).append(p)
    if not packs:
        packs[""] = {}

    findings = []
    for lang, files in sorted(packs.items()):
        label = f"{root}" + (f" [{lang}]" if lang else "")
        findings += lint_pack(files, label, args, today)

    errors = sum(f["severity"] == "error" for f in findings)
    warnings = len(findings) - errors

    if args.format == "json":
        print(json.dumps({"errors": errors, "warnings": warnings, "findings": findings},
                         ensure_ascii=False, indent=2))
    else:
        for f in findings:
            loc = f["file"] + (f":{f['line']}" if f["line"] else "")
            print(f"{loc}: {f['severity']} {f['rule']} {f['message']}: {f['detail']}")
        print(f"\n{errors} error(s), {warnings} warning(s) in {root}")
        if not findings:
            print("Context pack is complete and consistent.")
    return 1 if errors or (args.strict and warnings) else 0


if __name__ == "__main__":
    sys.exit(main())
