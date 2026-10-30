---
name: init-project-lite
description: Docs-only project init for the standard web stack (Next.js, Tailwind, Motion, Prisma, PostgreSQL via Neon/Supabase). Writes AGENTS.md (git rules), CLAUDE.md, STACK.md and .env.example without installing or scaffolding anything. Use when the user says "init project lite", "add stack rules", or wants the standards only.
---

# init-project-lite

Git workflow rules + web stack standard as documents only. No `npm`, no `create-next-app`, no network. Templates: `templates/git/`, `templates/stack/` in the dev-kit plugin.

`$KIT` = dev-kit root = two levels above this skill's real directory (resolve symlinks/junctions first).

## Steps

1. **Project root** = current working directory (or the path the user gave).
2. **Inspect, read-only**: Git repo or not; `AGENTS.md`, `CLAUDE.md`, `STACK.md`, `.env.example`, `.gitignore`, `package.json` exist; branches and worktrees if a repo.
3. **Ask once** (AskUserQuestion, every run, never assume from a previous project): (a) database provider, Neon or Supabase; (b) design the UI in Pencil first with the `pencil-design-first` skill, yes or no.
4. **Install.** `python "$KIT/scripts/install.py" "<root>" --profile lite` (`python3` on macOS/Linux; `--dry-run` to preview). Creates only missing files; a newly created `AGENTS.md` gets `@STACK.md`.
5. **Trim `.env.example`** to the chosen provider block, only if this run created it.
6. **Existing files** (never overwritten): offer, and apply only after the user says yes:
   - `AGENTS.md` exists: append missing sections from `$KIT/templates/git/AGENTS.md` and an `@STACK.md` line.
   - `CLAUDE.md` lacks `@AGENTS.md`: add that line.
   - `.gitignore` lacks `.env`: add it.
7. **Design (only if the user said yes in step 3).** Invoke the `pencil-design-first` skill (`dev-kit:pencil-design-first` in Claude Code) after the docs exist. It checks that the Pencil app is open, designs, and waits for explicit approval; write no UI code before that approval. If no, skip silently.
8. **Report**: created/skipped, repo state, design choice, pending offers. Remind the user to paste real connection strings into `.env` themselves.

## Hard rules

- No installs, no scaffolding, no `git init`, branch, worktree, commit, remote, or Git config change.
- Never write real credentials anywhere.
- Never overwrite or delete existing files.
