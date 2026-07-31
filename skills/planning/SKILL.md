---
name: planning
description: Use when the user asks for a design or implementation plan, or when a requested change has consequential unresolved decisions that should be settled before editing.
---

# Planning

Produce only the design or implementation detail needed to make the next action reliable.

## Decide whether planning is needed

- For analysis, design, or plan-only requests, inspect the relevant material and return the requested artifact without implementing.
- For a clear implementation request, proceed without a planning ceremony.
- When an unresolved choice materially affects behavior, compatibility, data handling, security, or scope, use OMP's `ask` tool. Ask the smallest independent set of questions together, provide 2–5 concrete options, and mark the safest default as recommended.
- Resolve questions from repository evidence before asking the user.

## Research with OMP

Use the narrowest authoritative surface:

- `read` for project instructions, files, documents, URLs, `issue://`, and `pr://`;
- `glob` to map relevant paths and `grep` for textual evidence;
- `lsp` for definitions, implementations, references, and symbol relationships;
- `bash` only for focused external commands or repository history that dedicated tools do not expose.

Do not delegate the top-level plan. A broad investigation may use a read-only `scout` through `task` only after the goal and independent research slice are explicit.

## Build the plan

1. State the goal, constraints, success criteria, and non-goals.
2. Record consequential decisions and why the selected approach wins.
3. Identify affected paths, interfaces, data flow, failure handling, migration or compatibility concerns, and validation.
4. Break implementation into ordered units with exact paths when a durable handoff is useful.

Scale the artifact to the task. Write specifications to `docs/omp/specs/` and implementation plans to `docs/omp/plans/` unless repository instructions specify another location. Use `write` for a new artifact and `edit` for an existing one. Ask for review and approval of the written artifact before implementing it; do not commit it unless requested.

Use `todo` to track an approved multi-step implementation, not as a substitute for the design and not for a plan-only request.

## Approval boundaries

Safe local inspection and planning do not need confirmation. Use `ask` before choosing between materially different product behaviors that evidence cannot resolve, expanding scope, writing externally, spending money, or performing destructive actions. Once approved, execute the in-scope plan without repeated confirmation.

## Output

Lead with the recommended approach. Include affected areas, validation, and unresolved risks. Omit generic best practices and detail the implementer can safely infer from the repository.
