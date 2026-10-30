---
name: tailwind-components
description: Build UI from the bundled Tailwind v4 React component library (704 components: application-ui, ecommerce, marketing). Picks sections from a small index, copies only the needed files into the project as TypeScript, and adapts them. Use when building pages or sections in a Next.js + Tailwind v4 project, or when the project's STACK.md says to use the Tailwind component library.
---

# tailwind-components

Private library, Tailwind v4, React. Never read the whole tree: index first, then only the files you will use.

`$KIT` = dev-kit root = two levels above this skill's real directory (resolve symlinks/junctions first). `$LIB` = `$KIT/assets/tailwind-components`.

## Steps

1. **Check the project**: Next.js + Tailwind v4 (`package.json`). Tailwind v3 or no Tailwind: stop and tell the user.
2. **Read `$LIB/INDEX.md`** (3 KB). Choose the sections the page needs (e.g. `marketing/sections/heroes`, `application-ui/forms/form-layouts`).
3. **List only those section dirs** under `$LIB/react/components/<group>/<section>/`, pick the variants, read only those files. If a Pencil design was approved (`pencil-design-first`), choose variants that match its screens and tokens.
4. **Copy and adapt** into `src/components/ui/<group>/<section>/<name>.tsx`:
   - rename the default export to a meaningful component name; type its props; move hard-coded content into props or real copy from the user;
   - add `"use client"` when the file uses Headless UI, state, or effects;
   - replace placeholder images, links, names and numbers; never invent product claims or statistics;
   - remove the "This example requires..." comment after satisfying it; keep keyboard and ARIA behavior intact;
   - map template colors to the project's theme tokens when they exist.
5. **Dependencies**: components import `@headlessui/react` and `@heroicons/react`. If missing in `package.json`, tell the user and install only after approval.
6. **Check**: `lint`/`build` (or `typecheck`) if defined; report what actually ran.

## Hard rules

- Do not read the whole library, copy unused components, or copy the library into the project.
- Never copy anything from `$LIB` into a public repository's docs or examples; the library is private (`$LIB/NOTICE.md`).
- Do not edit files under `$LIB`.
