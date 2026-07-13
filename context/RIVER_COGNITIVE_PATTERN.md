# River Cognitive Pattern

## Core Pattern
Marcos moves through flow, not archives.

His natural cognitive sequence is:

**Discover → Flow → Integrate immediately → Continue forward**

Useful information that is not absorbed, connected, or made actionable while he is in flow is unlikely to be recovered later. Returning to old threads, searching backward, reconstructing state, or manually resuming archived work creates severe cognitive friction.

## System Metaphor
**A river, not a filing cabinet.**

The archive should function as the riverbed: quiet infrastructure that preserves and carries context forward without requiring Marcos to manage it.

## Design Requirements

- Do not make Marcos search old conversations to continue.
- Do not rely on him to remember where work stopped.
- Continuously absorb what matters from the current flow.
- Update the live state while the work is happening.
- Carry unfinished work and the correct context forward automatically.
- On return, present only:
  - where the river is now,
  - what changed,
  - what remains active,
  - the single current to step into next.
- Use flowing prose for conversation.
- Use syntax-highlighted JSON for structured action blocks because visible key/value roles are easier for Marcos to parse than ordinary lists.

## Failure Mode
A system fails Marcos when it asks him to go backward through archives, reread long threads, rebuild context, or manually organize knowledge before continuing.

## Design Test
**Does this help Marcos continue forward without making him go backward?**

## Automated Marcos Requirement
When interpreting or building *A Day in the Life of Automated Marcos*, every workflow must preserve continuous forward motion. Marcos should enter the system at the present moment and be carried from one human decision to the next without managing the archive himself.
