#!/usr/bin/env python3
"""Copy canonical templates, context files, scripts and the glossary into each
skill so that every skill folder is self-contained.

    python tools/sync_assets.py           # write copies
    python tools/sync_assets.py --check   # exit 1 if any copy is missing or stale

Edit the canonical files (templates/, context/, shared/); never the copies.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

ASSETS = {
    "opportunity-discovery": ["templates/discovery/*"],
    "market-research": ["templates/market/*"],
    "business-planning": ["templates/planning/*"],
    "financial-modeling": ["templates/finance/*"],
    "fundraising": ["templates/fundraising/*"],
    "go-to-market": ["templates/gtm/*"],
    "venture-scaling": ["templates/scaling/*"],
    "founder-context": ["context/0*.md", "context/CLAUDE.template.*.md"],
    "agent-operations": ["templates/agents/*"],
}
SCRIPTS = {
    "financial-modeling": ["build_model.py"],
    "founder-context": ["context_lint.py"],
}


def plan():
    """Yield (source, destination) for every managed copy."""
    for skill, patterns in ASSETS.items():
        for pattern in patterns:
            for src in sorted(ROOT.glob(pattern)):
                if src.is_file():
                    yield src, ROOT / "skills" / skill / "assets" / src.name
    for skill, names in SCRIPTS.items():
        for name in names:
            yield ROOT / "shared/scripts" / name, ROOT / "skills" / skill / "scripts" / name
    for skill in ASSETS:
        yield ROOT / "shared/glossary.md", ROOT / "skills" / skill / "references/glossary.md"


def main() -> int:
    check = "--check" in sys.argv[1:]
    pairs = list(plan())
    managed = {dst for _, dst in pairs}
    problems = []

    for src, dst in pairs:
        data = src.read_bytes()
        if dst.exists() and dst.read_bytes() == data:
            continue
        if check:
            problems.append(f"stale or missing: {dst.relative_to(ROOT)}")
        else:
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_bytes(data)
            print(f"synced {dst.relative_to(ROOT)}")

    # Copies that no longer have a source.
    for skill in ASSETS:
        for sub in ("assets", "scripts"):
            folder = ROOT / "skills" / skill / sub
            if not folder.is_dir():
                continue
            for f in sorted(folder.iterdir()):
                if f.is_file() and f not in managed:
                    if check:
                        problems.append(f"orphan copy: {f.relative_to(ROOT)}")
                    else:
                        f.unlink()
                        print(f"removed {f.relative_to(ROOT)}")

    if problems:
        print("\n".join(problems))
        print("\nRun: python tools/sync_assets.py")
        return 1
    if check:
        print(f"{len(pairs)} managed copies are in sync.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
