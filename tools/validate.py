#!/usr/bin/env python3
"""Repository checks: skill metadata, Arabic/English parity, links, JSON.

    python tools/validate.py

Exit status 0 when everything passes, 1 otherwise. Standard library only.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ARABIC = re.compile(r"[؀-ۿ]")
LINK = re.compile(r"(?<!\!)\[[^\]]*\]\(([^)\s]+)\)")
NAME = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
PAIRED_DIRS = ["context", "templates", "workflows", "frameworks"]

errors: list[str] = []


def err(path: Path, msg: str):
    errors.append(f"{path.relative_to(ROOT)}: {msg}")


def frontmatter(text: str) -> dict | None:
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 4)
    if end < 0:
        return None
    out: dict = {}
    for line in text[4:end].splitlines():
        m = re.match(r"^([A-Za-z_-]+):\s*(.*)$", line)
        if m and not line.startswith(" "):
            out[m.group(1)] = m.group(2).strip()
    out["_body"] = text[end + 5:]
    return out


def check_skills():
    skills = sorted(p for p in (ROOT / "skills").iterdir() if p.is_dir())
    if not skills:
        errors.append("skills/: no skills found")
    for d in skills:
        f = d / "SKILL.md"
        if not f.exists():
            err(d, "missing SKILL.md")
            continue
        fm = frontmatter(f.read_text(encoding="utf-8"))
        if fm is None:
            err(f, "missing or malformed frontmatter")
            continue
        name, desc = fm.get("name", ""), fm.get("description", "")
        if name != d.name:
            err(f, f"name '{name}' does not match folder '{d.name}'")
        if not NAME.match(name) or len(name) > 64:
            err(f, "name must be lowercase letters, digits and hyphens, at most 64 characters")
        if not desc:
            err(f, "description is empty")
        if len(desc) > 1024:
            err(f, f"description is {len(desc)} characters; limit is 1024")
        if ": " in desc:
            err(f, "description contains ': ', which breaks plain YAML; rephrase")
        if not ARABIC.search(desc):
            err(f, "description has no Arabic trigger terms")
        if "Use when" not in desc:
            err(f, "description should say when to use the skill ('Use when ...')")
        if fm.get("license") != "MIT":
            err(f, "license should be MIT")
        body_lines = fm["_body"].count("\n")
        if body_lines > 500:
            err(f, f"body is {body_lines} lines; keep SKILL.md under 500 and move detail to references/")
        if not (d / "references/glossary.md").exists():
            err(d, "missing references/glossary.md (run tools/sync_assets.py)")
        # Every assets/..., references/..., scripts/... path named in the body exists.
        for ref in set(re.findall(r"`((?:assets|references|scripts)/[A-Za-z0-9_.\-/]+)`", fm["_body"])):
            target = d / ref
            if target.exists() or list(target.parent.glob(target.name + ".*")):
                continue
            err(f, f"mentions {ref}, which does not exist in the skill")


def shape(text: str):
    lines = [l for l in text.splitlines()]
    headings = [len(m.group(1)) for l in lines if (m := re.match(r"^(#{1,6})\s", l))]
    table_rows = sum(1 for l in lines if l.strip().startswith("|"))
    placeholders = len(re.findall(r"\{\{.*?\}\}", text))
    return headings, table_rows, placeholders


def check_pairs():
    for folder in PAIRED_DIRS:
        base = ROOT / folder
        en_files = sorted(base.rglob("*.en.md"))
        ar_files = sorted(base.rglob("*.ar.md"))
        for en in en_files:
            ar = en.with_name(en.name[:-len(".en.md")] + ".ar.md")
            if not ar.exists():
                err(en, "no Arabic counterpart (.ar.md)")
                continue
            en_text, ar_text = en.read_text(encoding="utf-8"), ar.read_text(encoding="utf-8")
            if not ARABIC.search(ar_text):
                err(ar, "contains no Arabic text")
            eh, et, ep = shape(en_text)
            ah, at, ap = shape(ar_text)
            if eh != ah:
                err(ar, f"heading structure differs from English ({len(ah)} vs {len(eh)} headings)")
            if et != at:
                err(ar, f"table rows differ from English ({at} vs {et})")
            if ep != ap:
                err(ar, f"placeholder count differs from English ({ap} vs {ep})")
        for ar in ar_files:
            en = ar.with_name(ar.name[:-len(".ar.md")] + ".en.md")
            if not en.exists():
                err(ar, "no English counterpart (.en.md)")
        # Every Markdown file in a paired folder must belong to a pair.
        for md in sorted(base.rglob("*.md")):
            if not md.name.endswith((".en.md", ".ar.md")) and md.name.lower() != "readme.md":
                err(md, "expected a .en.md / .ar.md pair")


def check_example_packs():
    en, ar = ROOT / "examples/mawja/context/en", ROOT / "examples/mawja/context/ar"
    for f in sorted(en.glob("*.md")):
        other = ar / f.name
        if not other.exists():
            err(f, "example has no Arabic counterpart")
            continue
        if shape(f.read_text(encoding="utf-8"))[:2] != shape(other.read_text(encoding="utf-8"))[:2]:
            err(other, "structure differs from the English example")


def check_links():
    for md in sorted(ROOT.rglob("*.md")):
        if any(part in {".git", "dist", "node_modules"} for part in md.parts):
            continue
        text = re.sub(r"```.*?```", "", md.read_text(encoding="utf-8"), flags=re.S)
        for target in LINK.findall(text):
            if re.match(r"^[a-z][a-z0-9+.-]*:", target) or target.startswith("#"):
                continue
            path = target.split("#")[0]
            if not path or "{{" in path:
                continue
            if not (md.parent / path).exists():
                err(md, f"broken link: {target}")


def check_json():
    for f in [ROOT / ".claude-plugin/plugin.json", ROOT / ".claude-plugin/marketplace.json",
              *sorted(ROOT.rglob("assumptions.json"))]:
        if not f.exists():
            err(f, "missing")
            continue
        try:
            json.loads(f.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            err(f, f"invalid JSON: {e}")


def main() -> int:
    check_skills()
    check_pairs()
    check_example_packs()
    check_links()
    check_json()
    if errors:
        print("\n".join(errors))
        print(f"\n{len(errors)} problem(s).")
        return 1
    n_skills = len([p for p in (ROOT / 'skills').iterdir() if p.is_dir()])
    n_pairs = sum(len(list((ROOT / d).rglob("*.en.md"))) for d in PAIRED_DIRS)
    print(f"OK: {n_skills} skills, {n_pairs} Arabic/English pairs, links and JSON valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
