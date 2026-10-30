#!/usr/bin/env python3
"""Regenerate assets/tailwind-components/INDEX.md (group > section > count). Run after changing the library."""
import sys
from collections import defaultdict
from pathlib import Path

LIB = Path(__file__).resolve().parent.parent / "assets" / "tailwind-components"
ROOT = LIB / "react" / "components"


def main() -> int:
    if not ROOT.is_dir():
        print(f"error: missing {ROOT}", file=sys.stderr)
        return 2
    groups = defaultdict(lambda: defaultdict(list))  # group -> section path -> [names]
    for f in sorted(ROOT.rglob("*.jsx")):
        rel = f.relative_to(ROOT)
        groups[rel.parts[0]]["/".join(rel.parts[1:-1])].append(f.stem)

    total = sum(len(v) for g in groups.values() for v in g.values())
    out = [
        "# Tailwind component index (React, Tailwind v4)",
        "",
        f"{total} components. Path: `react/components/<group>/<section>/<name>.jsx`. "
        "List one section dir to see its files; read only the ones you need.",
        "",
    ]
    for g in sorted(groups):
        out.append(f"## {g}")
        for sec in sorted(groups[g]):
            out.append(f"- `{sec}` ({len(groups[g][sec])})")
        out.append("")
    (LIB / "INDEX.md").write_text("\n".join(out), encoding="utf-8", newline="\n")
    print(f"INDEX.md: {total} components, {sum(len(g) for g in groups.values())} sections")
    return 0


if __name__ == "__main__":
    sys.exit(main())
