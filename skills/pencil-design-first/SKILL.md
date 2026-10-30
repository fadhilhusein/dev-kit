---
name: pencil-design-first
description: Design-first gate for any NEW project with a user interface (website, landing page, web app, dashboard, mobile app, native/desktop app). Use BEFORE writing any UI code - designs the UI/UX in Pencil (pen.dev) via the Pencil MCP, then waits for user approval before implementing. Trigger on "build me an app/website", "new project", "create a landing page", "make a mobile app", "start a new UI". Skip for bug fixes, backend-only work, or small tweaks to an existing UI.
---

# Pencil Design First

No UI code until the design exists in Pencil and the user approved it.

## When it applies

- New project that has an interface, or a new major screen/flow from scratch.
- Skip: bug fix, backend/CLI/API only, small edit to existing UI, user says "skip design".

## Flow

### 1. Check Pencil MCP is online

Tools are `mcp__pencil__*` (`get_app_state`, `read_skill`, `get_style`, `execute`, `browser`). If deferred, load them with ToolSearch (`select:mcp__pencil__get_app_state,mcp__pencil__read_skill,mcp__pencil__get_style,mcp__pencil__execute`).

Call `get_app_state`. If tools are missing, call errors, or no app/connection:

- STOP. Do not write code. Do not switch to another design tool.
- Ask user (AskUserQuestion or plain message): "Open the Pencil app (pen.dev) so I can connect to the MCP. Tell me when it's open."
- Wait for the user to confirm, then retry `get_app_state`. Repeat until online.

### 2. Brief (one round, max 4 questions)

Ask only what you cannot infer: purpose and audience, platform (web / mobile / desktop), pages or screens needed, style direction (reference sites, brand colors, mood). If the user already gave this, skip and state your assumptions.

### 3. Design in Pencil

- Run `read_skill` for Pencil's own design guidance and `get_style` for style options; follow them. `.pen` files are encrypted: touch them only through Pencil tools, never Read/Grep.
- Build with `execute`: define tokens first (colors, type scale, spacing, radius), then reusable components, then screens.
- Cover: every key screen, plus the states that matter (empty, loading, error, hover/active) and the responsive variant (mobile + desktop for web).
- Real, plausible copy. No lorem ipsum. Never invent numbers or claims the user did not give.
- Accessibility: contrast, tap targets >= 44px, readable type sizes.
- Verify visually (screenshot/inspect the canvas via the tool) and fix overlaps, clipping, misalignment before showing the user.
- Keep a copy of the design in the repo (see step 3b).

### 3b. Save the design into the repository (mandatory)

User opens the project from other devices, so the design must travel with the repo.

- Pass a `filePath` inside the project (e.g. `<project>/design/<app-name>.pen`) to `execute` so the design lives in the repo from the start.
- If the design is only an unsaved draft in Pencil, ask the user to use the draft menu's **Share** option (pen.dev) and save/export the file to `<project>/design/`, or save it there yourself if the tools allow. Confirm the file exists on disk (`ls`).
- Never Read/Grep the `.pen` file (encrypted). Just make sure it exists and is not git-ignored (`git check-ignore`).
- Record the path in the project README (one line: "Design: `design/<app-name>.pen`, open with Pencil / pen.dev").
- Re-save the copy after every revision, so the repo always has the latest version. Commit it only if the user asked you to commit.

### 4. Approval gate (mandatory)

Summarize the design in a few lines: screens, style, tokens, anything assumed. Tell the user where to look in Pencil and where the repo copy lives. Then ask with AskUserQuestion:

- "Approve - start coding"
- "Revise" (user says what to change)

Never implement on silence or a vague reply. On revise: edit the design, re-verify, ask again. Loop until explicit approval.

### 5. Implement (only after approval)

- Match the approved design: same tokens, spacing, components, copy, states.
- Read exact values from the Pencil design rather than guessing from memory.
- Deviation needed (technical limit)? Tell the user, do not silently drift.
