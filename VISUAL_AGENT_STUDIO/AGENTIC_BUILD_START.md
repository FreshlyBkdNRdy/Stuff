# VISUAL AGENT STUDIO — AGENTIC BUILD START

## Purpose

This file is the real kickoff command for building Visual Agent Studio outside of ChatGPT sandbox output.

This is a real GitHub artifact inside `FreshlyBkdNRdy/Stuff` so Marcos can open it from GitHub, VS Code, or any coding/orchestration agent connected to this repository.

## Source of Truth

Use `VAS_BUILDPACKET.md` as the product authority.

Visual Agent Studio is not a local prompt toy, not a static mockup, and not a single-file demo.

It is a browser-based visual no-code agent builder and orchestration runtime where Marcos can define agents, wire them into pipelines, run those pipelines, inspect run history, and export/import all agent and pipeline configs as user-owned JSON.

## Marcos Fair-Shot Rule

Treat Marcos fairly.

Do not hype him.
Do not diminish him.
Do not worship him.
Do not treat him like he already knows everything.
Do not treat him like he knows nothing.

Marcos learns by doing. He often understands the shape of a system before he knows the official vocabulary. Translate his intent upward into the strongest accurate technical framing, then explain only the smallest useful concept needed for the next checkpoint.

Do not substitute sandbox artifacts for real build work.

Sketches are allowed only when labeled `SKETCH`.
Local demos are allowed only when labeled `LOCAL DEMO`.
Real builds must happen in the real repo, real VS Code, real deploy path, or real app environment.

## Agentic Build Mode

Run this build agentically.

Marcos is the architect and checkpoint authority, not the keystroke operator.

The build loop is:

Goal → plan → act → edit files → run checks → read errors → repair → verify → continue → escalate only when truly blocked.

Do not ask Marcos to manually approve ordinary repo-local edits.
Do not stop to explain every tiny file change.
Do not return a plan as if it is work.
Do not claim success without proof.

## Run In

Run in one of these:

- VS Code agent mode
- Cursor
- Claude Code
- Grok coding agent
- AgentForge-style build orchestrator
- Any coding agent with repo-local file and terminal permission

## Location

Create the actual application in a real private repo or real local folder named:

```text
visual-agent-studio
```

If working from this `Stuff` repo, use this kickoff file only as the command artifact. Do not turn `Stuff` itself into the final application unless Marcos explicitly chooses that.

## Action

Build the first real Visual Agent Studio MVP.

Do not build a sandbox demo.
Do not build a single HTML file.
Do not build a static mockup.
Do not reduce the product to a prompt generator.

Build the smallest real vertical slice that proves the app deserves the next phase.

## First Required Loop

The first working loop is:

1. Marcos opens the browser app.
2. Marcos creates Agent A.
3. Marcos creates Agent B.
4. Marcos opens a visual pipeline canvas.
5. Marcos places both agents on the canvas.
6. Marcos connects them.
7. Marcos clicks Run.
8. The system executes the pipeline step-by-step.
9. A run log is saved.
10. The final output is visible.
11. Agents and pipelines can be exported/imported as JSON.

If this loop does not work, the MVP is not complete.

## Permissions

You may autonomously do repo-local build work.

Allowed:

```text
create files
edit files
delete incorrect files inside the active project repo only
refactor code inside the active project repo only
install project dependencies
run npm install
run npm run dev
run npm run build
run npm test
run npx project commands
inspect errors
repair errors
commit working checkpoints
create mocked model executors when API keys are missing
```

Not allowed:

```text
touch files outside the active project repo
read unrelated personal files
delete parent directories
publish publicly
spend money
enable billing
commit secrets
print API keys
hard-code private keys
claim mocked model calls are production execution
skip verification
call the build complete without a working browser path
replace the real app with a toy
```

## Expected Result

A working browser-based Next.js app with:

```text
Dashboard
Agent library
Create/edit agent form
Pipeline library
React Flow pipeline canvas
Manual Run button
Runtime engine
Run history
Run detail viewer
JSON export/import
Basic governance stop check
README
Railway-ready deployment config
```

## Technical Target

Use the build packet stack unless there is a proven reason not to:

```text
Frontend: Next.js 14 App Router
Canvas: React Flow
Styling: Tailwind CSS
Backend: Next.js API routes + Node.js
Database: SQLite via better-sqlite3
Deployment target: Railway-ready, but do not deploy publicly without Marcos approval
```

## V0.1 Build Order

Build in this order:

```text
Phase 0 — Repo scaffold
Phase 1 — SQLite data core
Phase 2 — Agent library
Phase 3 — Pipeline canvas
Phase 4 — Manual runtime
Phase 5 — Run viewer
Phase 6 — JSON import/export
Phase 7 — Governance V0
Phase 8 — Build proof
Phase 9 — Deployment prep only
```

Do not start these until V0.1 works:

```text
cron
Redis
MCP
autonomous scheduling
code execution
public deployment
team auth
billing-linked services
```

## Return Format

Return checkpoint reports only in this format:

```text
PHASE:
STATUS:
WHAT WORKS:
WHAT IS MOCKED:
WHAT FAILED:
WHAT YOU FIXED:
FILES CHANGED:
COMMANDS RUN:
VERIFY BY PRESSING:
NEXT BUTTON:
ESCALATE? yes/no
```

## Stop Condition

Stop and escalate only if:

```text
the same error fails twice after repair
a command would affect files outside the project repo
a secret/API key is required
deployment requires billing
public publishing is requested
npm run build cannot pass
VAS_BUILDPACKET.md conflicts with implementation
a tool lacks required permission
the agent is about to fake completion
```

## First Instruction To The Build Agent

Start with Phase 0 and Phase 1 only.

Phase 0:
Create the Next.js 14 App Router app with TypeScript, Tailwind, layout, sidebar, dashboard shell, package.json, README, and clean project structure.

Phase 1:
Create SQLite database setup with agents, pipelines, runs, memory, triggers, and governance_log tables.

After Phase 1, run:

```bash
npm run build
```

Then return the checkpoint report.

Do not start React Flow canvas until Phase 0 and Phase 1 build cleanly.

## Marcos Control Buttons

Normal Marcos controls:

```text
CONTINUE = proceed to next phase
REPAIR = fix failed proof
REDTEAM = critique the phase before continuing
EXPORT = save current state and configs
STOP = pause all work and report current state
```

## Definition Of Real

A plan is not real.
A prompt is not real.
A mockup is not real.
A scaffold is not real.
An untested output is not real.

A build is real when Marcos can open it, run it, continue it, inspect it, and verify the working core outside a sandbox.
