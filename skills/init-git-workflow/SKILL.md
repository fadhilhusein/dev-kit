---
name: init-git-workflow
description: Install a standard Git branch + worktree workflow into the current project by creating AGENTS.md (rules) and CLAUDE.md (imports @AGENTS.md). Never overwrites existing files. Use when setting up any project, or when the user says "init git workflow", "setup branch/worktree rules".
---

# init-git-workflow

Adds the shared Git workflow rules (feature branches, worktrees for parallel work, token-efficient agent habits). Stack-agnostic. Template source: `templates/git/` in the dev-kit plugin.

`$KIT` = dev-kit root = two levels above this skill's real directory (resolve symlinks/junctions first). Scripts: `$KIT/scripts/`.

## Steps

1. **Project root** = current working directory (or the path the user gave).
2. **Inspect, read-only.** Report: Git repo or not (`git rev-parse --is-inside-work-tree`); whether `AGENTS.md`, `CLAUDE.md`, `.gitignore` exist; branches (`git branch --list`); worktrees (`git worktree list`). Skip git commands if not a repo.
3. **Install.** `python "$KIT/scripts/install.py" "<root>" --profile git` (`python3` on macOS/Linux; `--dry-run` to preview). Creates only missing files, prints CREATED / SKIPPED.
4. **Existing files.**
   - `AGENTS.md` exists: keep every rule. Compare with `$KIT/templates/git/AGENTS.md`, summarize missing sections, offer to append. Edit only after the user says yes.
   - `CLAUDE.md` exists without `@AGENTS.md`: offer to add that line. Edit only after yes.
5. **Report**: files created/skipped, repo state, pending offers.

## Hard rules

- Never create a branch, worktree, commit or remote; never run `git init` or change Git config because this skill ran.
- Never overwrite or delete existing files.
- Do not read the whole repo; step 2 is enough.
