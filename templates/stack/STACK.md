# Web Stack Standard

Stack: Next.js (App Router) + Tailwind CSS + Motion + Prisma ORM + PostgreSQL (Neon or Supabase).
Follow the versions installed in `package.json`; check current docs before using an API that changed between majors.

## Next.js
- App Router, TypeScript `strict`, `src/` layout, import alias `@/*`.
- Server Components by default. Add `"use client"` only for state, effects, browser APIs, or Motion elements.
- Data access only on the server (Server Components, Server Actions, Route Handlers). Validate all input at those boundaries.
- Read env vars in one place (`src/env.ts`); never use `NEXT_PUBLIC_` for secrets.

## Tailwind CSS
- Use the installed major's setup (v4: CSS-first `@theme` in `globals.css`).
- Colors, fonts, spacing come from theme tokens; no one-off hex values in components.
- Mobile-first; verify layout at phone width.

## Motion
- Package `motion`, import from `motion/react` (client components). Never add `framer-motion`.
- Animate `transform` and `opacity` only. Honor `prefers-reduced-motion` (`useReducedMotion` or `MotionConfig reducedMotion="user"`).
- Keep animation in small client components; do not turn whole pages into client components.

## Prisma + PostgreSQL
- Schema in `prisma/schema.prisma`; migrations in `prisma/migrations/` are committed.
- One shared client in `src/lib/db.ts` (global singleton in dev to survive hot reload).
- Dev: `prisma migrate dev`. Prod/CI: `prisma migrate deploy`. Never `db push` or `migrate reset` against a shared/prod database.
- Never build SQL by string concatenation; use the client or tagged `$queryRaw`.
- Two connection strings:
  - `DATABASE_URL` = pooled, used by the app at runtime.
  - `DIRECT_URL` = direct, used by the Prisma CLI for migrations.
- Prisma 7+: the schema `datasource` has no `url`; the CLI URL is `datasource.url: env("DIRECT_URL")` in `prisma.config.ts`, and the runtime client uses a driver adapter (`@prisma/adapter-pg`) with `DATABASE_URL`. Prisma 6 and older: `url = env("DATABASE_URL")` and `directUrl = env("DIRECT_URL")` in the schema.
- Neon: pooled host contains `-pooler`; direct host does not. Supabase: transaction pooler (port 6543) for `DATABASE_URL`, direct/session connection (port 5432) for `DIRECT_URL`.

## Secrets
- Real values only in `.env` / `.env.local` (git-ignored). Commit `.env.example` with placeholders only.
- Never print, log, or commit connection strings, keys, or tokens. The user pastes real values themselves.

## Standard task flow
schema change -> migration -> server action / route handler -> UI -> checks -> completion report (see Git Workflow rules).

## Expected scripts
`dev`, `build`, `lint`, and when present `typecheck`, `test`. Run `lint` and `build` (plus `typecheck`/`test` if defined) before reporting done; report only what actually ran.
