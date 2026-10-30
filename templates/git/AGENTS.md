# Git Workflow

Rules for every AI agent (Claude Code, Codex, others) working in this repository.

## A. Core principles

- Never develop features directly on `main`.
- Each independent feature gets its own branch. Each bug fix gets its own branch.
- Use a worktree only when several independent tasks must run at the same time.
- No branch/worktree for tiny changes (typo, one-line tweak): do them on the current task branch.
- Prefer ONE agent when work is sequential.
- Never let two agents edit the same file at the same time.
- Never discard the user's changes.
- Never merge or push without explicit user authorization.

## B. Branch naming

Format `<type>/<description>`, lowercase kebab-case:

`feature/` `fix/` `hotfix/` `refactor/` `docs/` `test/`

Examples: `feature/user-auth`, `fix/cart-total`, `hotfix/payment-timeout`.

- `main` is the stable branch.
- `develop` is optional: use it only if the project already has it as an integration branch. If it does not exist, use `main` as the base.

## C. Worktree layout

Keep worktrees OUTSIDE the main repository, in a sibling folder:

```
projects/
├── my-project/                  # main repo
└── my-project-worktrees/
    ├── feature-auth/
    ├── feature-dashboard/
    └── hotfix-payment/
```

Folder name = branch name with `/` replaced by `-`. Never place extra worktrees inside the main repo.

## D. Creating a worktree

First confirm the base branch exists:

```
git rev-parse --verify develop     # or main
```

Then:

```
git worktree add -b feature/auth ../my-project-worktrees/feature-auth develop
git worktree add -b hotfix/payment ../my-project-worktrees/hotfix-payment main
git worktree list
```

(Use `main` instead of `develop` when the project has no `develop`.)

## E. Task lifecycle

1. Understand requirements.
2. Inspect existing code (only relevant files).
3. Plan the implementation.
4. Select or create the branch.
5. Create a worktree only when justified (see A, F).
6. Implement.
7. Run tests.
8. Review the diff.
9. Commit.
10. Report completion (see J).

Never claim tests pass unless they were actually run. If they could not run, say so.

## F. Parallel agents

Only when tasks are independent and the time saved is worth the extra tokens.

- One worktree + one branch per agent.
- Give each agent a clear scope; avoid overlapping files.
- The coordinator owns integration.
- Run integration tests after everything is combined.
- Do not parallelize small tasks that depend on each other.

## G. Token efficiency

- Default to a single agent. Spawn subagents only when truly needed.
- Do not read the whole repository without a reason; read only files relevant to the task.
- Do not repeat investigation already done; reuse earlier findings.
- Avoid duplicate reviews.
- Report findings briefly. Trim long logs to the relevant lines.
- Use parallel agents only when the time gain justifies the added tokens.

A Git worktree by itself costs no AI tokens. Token usage comes from AI agent activity (reading, reasoning, output), and every extra agent multiplies it.

## H. Hotfix workflow

Production bug while other features are in progress:

1. Do not disturb running feature worktrees.
2. Create a new worktree from `main` on a `hotfix/<description>` branch.
3. Fix in isolation, run tests, commit.
4. Merge only with user authorization.

## I. Safety

Do NOT run these without explicit user approval:

```
git reset --hard
git clean -fd
git branch -D
git worktree remove --force
```

Also never:

- Delete user changes.
- Remove a worktree that has uncommitted changes.
- Overwrite an existing `AGENTS.md` or `CLAUDE.md`.
- Rewrite published Git history without permission.
- Commit credentials, API keys, or `.env` files.

## J. Completion report

End every task with:

```
Task:
Branch:
Worktree:
Base branch:
Files changed:
Tests/checks:
Commit:
Merge/PR status:
Remaining risks:
```
