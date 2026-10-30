#!/usr/bin/env python3
"""Install dev-kit docs into a project. Never overwrites, never runs git.

Profiles:
  git   AGENTS.md (git workflow rules) + CLAUDE.md (@AGENTS.md)
  lite  git + STACK.md + .env.example; a newly created AGENTS.md gets '@STACK.md' appended
Flag --ui-components (lite): a newly created STACK.md also gets the Tailwind component library section.
"""
import argparse
import sys
from pathlib import Path

TEMPLATES = Path(__file__).resolve().parent.parent / "templates"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument("project", nargs="?", default=".", help="project root (default: cwd)")
    ap.add_argument("--profile", choices=("git", "lite"), default="git")
    ap.add_argument("--ui-components", action="store_true", help="lite only: add the Tailwind component library section to a newly created STACK.md")
    ap.add_argument("--dry-run", action="store_true", help="show actions, write nothing")
    args = ap.parse_args()
    if args.ui_components and args.profile != "lite":
        ap.error("--ui-components requires --profile lite")

    root = Path(args.project).expanduser().resolve()
    if not root.is_dir():
        print(f"error: not a directory: {root}", file=sys.stderr)
        return 2

    tpl = lambda rel: (TEMPLATES / rel).read_text(encoding="utf-8")
    agents = tpl("git/AGENTS.md")
    plan = [("CLAUDE.md", tpl("git/CLAUDE.md"))]
    if args.profile == "lite":
        agents += "\n@STACK.md\n"  # only reaches a file this run creates
        stack = tpl("stack/STACK.md") + (tpl("stack/UI-COMPONENTS.md") if args.ui_components else "")
        plan += [("STACK.md", stack), (".env.example", tpl("stack/env.example"))]
    plan.insert(0, ("AGENTS.md", agents))

    print(f"Project: {root}")
    print(f"Git repo: {'yes' if (root / '.git').exists() else 'no (not initialized; left as is)'}")
    for name, text in plan:
        dst = root / name
        if dst.exists():
            print(f"SKIPPED  {name} (already exists, not modified)")
        elif args.dry_run:
            print(f"WOULD CREATE  {name}")
        else:
            try:
                with open(dst, "x", encoding="utf-8", newline="\n") as f:  # "x": never clobber
                    f.write(text)
                print(f"CREATED  {name}")
            except FileExistsError:
                print(f"SKIPPED  {name} (already exists, not modified)")

    def has(name, needle):
        p = root / name
        return p.is_file() and needle in p.read_text(encoding="utf-8", errors="replace")

    if (root / "CLAUDE.md").is_file() and not has("CLAUDE.md", "@AGENTS.md"):
        print("NOTE  CLAUDE.md does not import @AGENTS.md; ask the user before adding it.")
    if args.profile == "lite" and (root / "AGENTS.md").is_file() and not has("AGENTS.md", "@STACK.md"):
        print("NOTE  AGENTS.md does not import @STACK.md; offer to add it, only with user approval.")
    if args.ui_components and (root / "STACK.md").is_file() and not has("STACK.md", "## UI components"):
        print("NOTE  STACK.md has no 'UI components' section; offer to append templates/stack/UI-COMPONENTS.md, only with user approval.")
    if (root / ".gitignore").is_file() and not has(".gitignore", ".env"):
        print("NOTE  .gitignore does not ignore .env; offer to add it, only with user approval.")
    print("No branch, worktree, commit, remote or git config was touched.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
