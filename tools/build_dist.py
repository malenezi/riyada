#!/usr/bin/env python3
"""Package each skill as a zip for upload to Claude apps.

    python tools/build_dist.py     # writes dist/<skill>.zip

Each archive contains one top-level folder named after the skill.
"""
from __future__ import annotations

import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    dist = ROOT / "dist"
    dist.mkdir(exist_ok=True)
    for skill in sorted(p for p in (ROOT / "skills").iterdir() if p.is_dir()):
        out = dist / f"{skill.name}.zip"
        with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
            for f in sorted(skill.rglob("*")):
                if f.is_file() and "__pycache__" not in f.parts:
                    z.write(f, Path(skill.name) / f.relative_to(skill))
        print(f"wrote {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
