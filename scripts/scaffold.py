#!/usr/bin/env python3
"""Scaffold Next.js + Tailwind + Motion + Prisma. Prints the command table by default; --run executes it.

Only CLI commands live here. Files that depend on the generated Prisma version
(prisma.config.ts, src/lib/db.ts) are edited by the agent afterwards, per STACK.md.
Never runs git, prisma migrate, or deploy. Stops on the first failing command.
"""
import argparse
import shutil
import subprocess
import sys
from pathlib import Path

PM = {  # create-next-app flag, add, add-dev, exec
    "npm": ("--use-npm", "npm install", "npm install -D", "npx"),
    "pnpm": ("--use-pnpm", "pnpm add", "pnpm add -D", "pnpm dlx"),
    "yarn": ("--use-yarn", "yarn add", "yarn add -D", "yarn dlx"),
    "bun": ("--use-bun", "bun add", "bun add -d", "bunx"),
}


def node_ok() -> bool:
    try:
        out = subprocess.run(["node", "-v"], capture_output=True, text=True, check=True).stdout
        major, minor = (int(x) for x in out.strip().lstrip("v").split(".")[:2])
        return (major, minor) >= (20, 9)  # Next.js 16 minimum
    except (OSError, subprocess.CalledProcessError, ValueError):
        return False


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("project", help="target dir (created if missing; '.' for current)")
    ap.add_argument("--pm", choices=PM, default="npm")
    ap.add_argument("--allow-nonempty", action="store_true")
    ap.add_argument("--run", action="store_true", help="execute (default: print only)")
    args = ap.parse_args()

    root = Path(args.project).expanduser().resolve()
    if root.exists() and not root.is_dir():
        print(f"error: not a directory: {root}", file=sys.stderr)
        return 2
    extra = [p.name for p in root.iterdir() if p.name != ".git"] if root.is_dir() else []
    if (root / "package.json").exists():
        print("package.json exists: refusing to scaffold over an existing project.", file=sys.stderr)
        return 2
    if extra and not args.allow_nonempty:
        print(f"{root} is not empty ({', '.join(extra[:5])}); use --allow-nonempty after user approval.", file=sys.stderr)
        return 2

    flag, add, add_dev, ex = PM[args.pm]
    cmds = [
        (root.parent, f'{ex} create-next-app@latest "{root.name}" --yes --ts --tailwind --eslint --app --src-dir '
                      f'--import-alias "@/*" --no-agents-md {flag}'),
        (root, f"{add} motion @prisma/client @prisma/adapter-pg"),
        (root, f"{add_dev} prisma dotenv"),
        (root, f"{ex} prisma init --datasource-provider postgresql"),
    ]
    print(f"Node >= 20.9: {'ok' if node_ok() else 'MISSING/TOO OLD'}")
    for cwd, c in cmds:
        print(f"[{cwd}] {c}")
    if not args.run:
        print("(dry run: pass --run to execute)")
        return 0
    if not node_ok() or not shutil.which(args.pm):
        print(f"error: need Node >= 20.9 and '{args.pm}' on PATH", file=sys.stderr)
        return 2
    root.parent.mkdir(parents=True, exist_ok=True)
    for cwd, c in cmds:
        print(f"\n$ {c}")
        if subprocess.run(c, cwd=cwd, shell=True).returncode:
            print("stopped: command failed", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
