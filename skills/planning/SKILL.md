---
name: planning
description: Use when the user asks for a design or implementation plan, or when a requested change has consequential unresolved decisions that should be settled before editing.
---

# Planning

Produce only the design or implementation detail needed to make the next action reliable.

## Decide whether planning is needed

- If the user asks only for analysis, design, or a plan, inspect the relevant material and return that artifact. Do not implement.
- If the user asks for implementation and the requirements are clear, proceed without a mandatory planning ceremony.
- Pause when an unresolved choice could materially change behavior, compatibility, data handling, security, or scope. Ask the smallest necessary set of independent questions together and recommend answers. Ask sequentially only when one answer determines the next question.
- Resolve questions from the repository, documentation, or existing conventions before asking the user.

## Build the plan

1. Inspect project instructions, relevant code, tests, documentation, and recent changes.
2. State the goal, constraints, success criteria, and non-goals.
3. Record consequential decisions and the reason for the chosen approach. Compare alternatives only when the choice is real.
4. Identify affected components, interfaces, data flow, failure handling, and validation.
5. Break implementation into ordered units with exact paths when the work needs a durable handoff.

Scale the artifact to the task. A small change may need a short inline plan. A broad or risky change may need a written design and task plan. Do not create documents or commits unless requested or required by project instructions.

## Approval boundaries

Safe local inspection and planning do not need confirmation. Ask before:

- choosing between materially different product behaviors when context cannot decide;
- expanding scope beyond the request;
- writing externally, spending money, or performing destructive actions.

When the user requested implementation, design approval is optional unless a consequential ambiguity remains.

## Output

Lead with the recommended approach. Include affected areas, validation, and any unresolved risk. Omit repeated rationale, generic best practices, and implementation detail that the next worker can infer safely from the repository.
