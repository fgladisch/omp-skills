---
name: planning
description: Use while OMP plan mode is active to shape what goes into the plan file; also when the user asks for a plan or design without implementation, or a change has consequential unresolved decisions that warrant entering plan mode.
---

# Planning

Shape what goes into a plan, not how plan mode works: in plan mode the harness prompt owns the mechanics and the plan structure. This skill only adds content guidance; never restate or bypass the harness rules.

## Am I in plan mode?

There is no mode-query tool; detect it from the conversation:

- The harness injects a plan-mode notice when the mode turns on and replays it on resume; its marker is the literal `Plan mode active.` plus read-only rules. If the notice is present, plan mode is on; apply the sections below.
- The `write` tool description is the plan-mode variant (`xd://` device transport plus `local://` drafts only), or a write failed with a plan-mode guard error: same conclusion.
- Otherwise plan mode is off. Do not simulate the plan-mode flow. For implementation work with consequential unresolved decisions, suggest toggling plan mode (`/plan` or Alt+Shift+P). For a plan-only request, deliver the plan as the response artifact (written to disk only if asked), using the harness plan skeleton: Context, Approach, Critical files & anchors, Verification, Assumptions & contingencies. A clear implementation request needs no planning ceremony.

## Scope check

If the request spans independent subsystems, suggest one plan per subsystem; each must produce working, testable software on its own.

## Units and interfaces

- Right-size Approach units: the smallest step that carries its own verification and could be approved while its neighbor is rejected. Fold setup and scaffolding into the unit that needs them.
- When units go to different implementers, record what each consumes and produces (exact signatures) so the handoff needs no conversation.

## No placeholders

"TBD", "add appropriate error handling", "similar to unit N", or any step missing the actual content (code, signature, literal) the implementer needs is a plan failure.

## Self-review

Before proposing in plan mode (or delivering a plan-only artifact): every requested outcome maps to a unit; the placeholder scan is clean; names, signatures, and paths are consistent across units. Fix issues inline, then propose or deliver; do not re-review in a loop.
