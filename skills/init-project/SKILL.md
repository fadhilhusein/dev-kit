---
name: init-project
description: Full project init for the standard web stack - scaffolds Next.js + Tailwind + Motion + Prisma (PostgreSQL via Neon/Supabase), then writes AGENTS.md, CLAUDE.md, STACK.md and .env.example. Runs installs only after approval. Use when the user says "init project", "new website", "scaffold the stack".
---

# init-project

`init-project-lite` (docs) plus scaffold. Side effects (installs, file generation) happen only after the user approves the command table.

`$KIT` = dev-kit root = two levels above this skill's real directory (resolve symlinks/junctions first). Docs steps are those of the `init-project-lite` skill.

## Steps

1. **Inspect, read-only**: target dir (cwd or user path), `package.json` present? dir empty (ignoring `.git`)? Git repo? existing `AGENTS.md`/`CLAUDE.md`/`STACK.md`/`.env.example`.
   - `package.json` exists: stop scaffolding; run the `init-project-lite` flow instead and say so.
2. **Interview once** (AskUserQuestion, every run, never assume from a previous project): project folder name, database provider (Neon or Supabase), package manager (default: from lockfile, else npm), whether to design the UI in Pencil first with the `pencil-design-first` skill (yes or no), and whether to use the bundled Tailwind component library with the `tailwind-components` skill (yes or no).
3. **Show the plan and WAIT for approval.** Run `python "$KIT/scripts/scaffold.py" "<dir>" --pm <pm>` (add `--with-ui` if the user wants the Tailwind component library) (dry run) and present its commands, plus the file steps below. Non-empty dir: tell the user which files exist and pass `--allow-nonempty` only if they approve.
4. **Scaffold** after approval: same command with `--run`. It does: `create-next-app` (TS, Tailwind, ESLint, App Router, `src/`, alias `@/*`, `--no-agents-md` so it does not create its own AGENTS.md/CLAUDE.md), add `motion`, `@prisma/client`, `@prisma/adapter-pg`, dev `prisma` + `dotenv`, `prisma init`. Stops on first failure; report and ask before retrying.
5. **Prisma wiring** (agent edits, following `STACK.md` and the files `prisma init` generated; check current Prisma docs for the installed major): `prisma.config.ts` CLI url = `DIRECT_URL`; `src/lib/db.ts` singleton using the driver adapter with `DATABASE_URL`; schema generator output as generated. If `prisma init` wrote a `.env` with a placeholder URL, keep placeholders only. Add `db:generate` / `db:migrate` scripts to `package.json`.
6. **Docs.** `python "$KIT/scripts/install.py" "<dir>" --profile lite` (add `--ui-components` if the user wants the Tailwind component library), then trim `.env.example` to the chosen provider (only if this run created it). Existing-file handling is the same as `init-project-lite` step 6 (offer, apply on yes only).
7. **Check**: `lint` and `build` (build may need valid env; if it fails only for missing DB env, say so rather than faking values). Report only what actually ran.
8. **Design (only if the user said yes in step 2).** Invoke the `pencil-design-first` skill (`dev-kit:pencil-design-first` in Claude Code). Keep the generated starter page untouched; the skill designs in Pencil and waits for explicit approval before any UI code is written. If no, skip silently.
9. **UI components (only if the user said yes in step 2).** Do not build pages now. Tell the user the `tailwind-components` skill is ready (`dev-kit:tailwind-components`) and is referenced from `STACK.md`; use it when pages are requested, after the Pencil design is approved if that was chosen.
10. **Report**: commands run, files created/skipped, design and UI-library choices, what the user must do (paste real `DATABASE_URL`/`DIRECT_URL` into `.env`, then `prisma migrate dev`).

## Hard rules

- Never run `prisma migrate`, `db push`, `git init`/branch/worktree/commit/remote, or any deploy.
- Never write, print or commit real credentials; the user supplies connection strings.
- Never scaffold over an existing `package.json`; never overwrite existing files.
- Write no UI code yourself; with Pencil design chosen, UI code waits for the design approval gate.
