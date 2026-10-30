# dev-kit

Claude Code plugin (and Codex-compatible skills) that bootstraps a project with a Git branch/worktree workflow and, optionally, an opinionated web stack: **Next.js + Tailwind CSS + Motion + Prisma + PostgreSQL (Neon or Supabase)**.

| Skill | Does |
|-------|------|
| `init-git-workflow` | `AGENTS.md` (git branch/worktree rules) + `CLAUDE.md` (`@AGENTS.md`). Any project. |
| `init-project-lite` | Git rules + `STACK.md` + `.env.example`. Docs only, nothing installed. |
| `init-project` | Scaffolds the stack (after you approve the command list), then the same docs. |
| `pencil-design-first` | Design-first gate for new UI: designs in [Pencil](https://pen.dev) via its MCP, saves the `.pen` file in the repo, and waits for your approval before any UI code. Needs the Pencil app and MCP. |

Both `init-project*` skills ask on every run whether to use `pencil-design-first`.

Safety: never overwrites existing files, never creates branches/worktrees/commits/remotes or touches Git config, never writes real credentials. Existing `AGENTS.md`/`CLAUDE.md` are only merged with your approval.

## Install (Claude Code)

```
/plugin marketplace add fadhilhusein/dev-kit
/plugin install dev-kit@dev-kit
```

Skills: `/dev-kit:init-git-workflow`, `/dev-kit:init-project-lite`, `/dev-kit:init-project`, `/dev-kit:pencil-design-first`.

From a local clone: `/plugin marketplace add /path/to/dev-kit`.

## Install (Codex)

Link each skill folder from a clone (no copies). Skills find `scripts/` and `templates/` two levels above their real directory, so link to the clone, don't copy a single skill.

macOS / Linux:
```bash
mkdir -p ~/.agents/skills
for s in init-git-workflow init-project-lite init-project pencil-design-first; do ln -s /path/to/dev-kit/skills/$s ~/.agents/skills/$s; done
```
Windows (PowerShell):
```powershell
New-Item -ItemType Directory -Force "$HOME\.agents\skills" | Out-Null
foreach ($s in "init-git-workflow","init-project-lite","init-project","pencil-design-first") {
  New-Item -ItemType Junction -Path "$HOME\.agents\skills\$s" -Target "C:\path\to\dev-kit\skills\$s"
}
```

## Structure

```
dev-kit/
├── .claude-plugin/{plugin.json, marketplace.json}
├── skills/{init-git-workflow, init-project-lite, init-project, pencil-design-first}/SKILL.md
├── templates/git/{AGENTS.md, CLAUDE.md}      # git rules: single source
├── templates/stack/{STACK.md, env.example}   # stack rules: single source
└── scripts/{install.py, scaffold.py}         # Python 3 stdlib only; macOS, Linux, Windows
```

## Scripts

```bash
python scripts/install.py [project] [--profile git|lite] [--dry-run]
python scripts/scaffold.py <dir> [--pm npm|pnpm|yarn|bun] [--allow-nonempty] [--run]   # prints commands unless --run
```

## Customize

Edit `templates/git/AGENTS.md` or `templates/stack/STACK.md`; they are the only sources. Projects already initialized keep their copy.

## Notes and limits

- The stack is opinionated (see `templates/stack/STACK.md`). Fork and edit the templates for a different stack.
- `create-next-app` 16+ generates its own `AGENTS.md`/`CLAUDE.md`; `init-project` passes `--no-agents-md` so these rules stay the single source.
- Prisma 7 moved the CLI connection URL to `prisma.config.ts` and requires a driver adapter at runtime; `STACK.md` covers Prisma 6 and 7. The agent wires these files after `prisma init`, reading what was generated.
- Tested: the installer (fresh, re-run, pre-existing files, Git state unchanged), scaffold dry-run and guards, plugin validation. **Not yet verified end to end:** `scaffold.py --run` (needs network and package installs) and the Prisma wiring step. Try it in a throwaway folder first.

## License

MIT, see [LICENSE](LICENSE).
