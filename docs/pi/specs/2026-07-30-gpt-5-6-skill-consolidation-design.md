# GPT-5.6 Skill Consolidation Design

## Goal

Refactor this repository's skill library around the GPT-5.6 prompting guidance published by OpenAI. Reduce prompt volume and workflow overhead while preserving the specialized instructions that materially improve coding outcomes or protect consequential actions.

Source: <https://developers.openai.com/api/docs/guides/latest-model#prompting-best-practices>

## Design principles

The revised library will apply these rules:

1. State each instruction once. Remove repeated warnings, motivational prose, duplicated examples, and overlapping workflow descriptions.
2. Define outcomes, relevant context, hard constraints, approval boundaries, success criteria, and required evidence. Avoid prescribing steps that GPT-5.6 can infer safely.
3. Permit safe, in-scope local inspection, editing, and non-destructive validation without approval.
4. Ask when an ambiguity could materially change the result. Require confirmation for external writes, destructive actions, or material scope expansion.
5. Select subagents by task shape. Use parallel work only for independent workstreams, and use fresh independent review where the risk justifies its cost.
6. Preserve concise output requirements that identify which facts, evidence, caveats, and next actions must survive trimming.
7. Keep examples only when they encode a repository-specific contract or prevent a demonstrated failure mode.

## Skill inventory

The repository will contain seven skills after consolidation.

### `planning`

Replaces `brainstorming` and `writing-plans`.

Use when the user asks for a design or plan, or when implementation has consequential unresolved decisions. Inspect the repository before asking questions. Proceed directly when requirements are clear. Produce planning detail proportional to the task, with explicit decisions, affected areas, validation, and unresolved risks. A written spec or implementation plan is optional unless the user requests one or the task needs a durable handoff.

### `code-review`

Replaces `requesting-code-review`, `receiving-code-review`, and `simplify`.

Use for reviewing a change, processing review feedback, or cleaning up a scoped diff. Establish the review scope and requirements, inspect evidence, rank actionable findings by impact, reject unsupported findings with reasons, fix accepted findings when authorized, and validate the result. One focused reviewer is the default. Parallel reviewers are reserved for broad or high-risk diffs with genuinely distinct review angles.

### `systematic-debugging`

Keep and rewrite.

Use for bugs, failing tests, and unexpected behavior. Reproduce the symptom, gather evidence, identify a supported root-cause hypothesis, test it with the smallest useful experiment, implement a focused fix, and verify both the original symptom and relevant regressions. Escalate when evidence is unavailable or repeated failed hypotheses indicate a deeper design problem.

### `test-driven-development`

Keep and rewrite as pragmatic test-first guidance.

Use for observable behavior changes and bug fixes when an automated test is feasible. Establish a failing test or equivalent reproduction, confirm the failure is relevant, implement the smallest sufficient change, and run focused plus broader validation. Allow justified exceptions for documentation, generated artifacts, configuration-only changes, exploratory spikes, or environments where automated tests are impractical. Record the alternative evidence instead of asking merely because an exception category applies.

### `verification-before-completion`

Keep and rewrite.

Use before making a completion or correctness claim. Match each material claim to fresh evidence, run the relevant checks, inspect their exit status and output, and report failures accurately. Verification depth must be proportional to the change and repository conventions. Avoid universal demands for unrelated full-suite checks.

### `commit`

Keep and rewrite.

Use only when the user asks to commit. Inspect the exact staged and unstaged scope, follow repository commit conventions with gitmoji as this repository's fallback, run relevant validation, and confirm the proposed message and file set before creating the commit. Never push, amend, bypass hooks, or broaden the staged set without authorization.

### `finishing-a-development-branch`

Keep and rewrite.

Use when the user wants to integrate, publish, retain, or discard completed branch work. Validate branch identity and worktree state, collect fresh verification evidence, present available outcomes, and execute the selected action. Require confirmation for pushing, opening a pull request, deleting work, or other consequential external or destructive operations.

## Removed skills and supporting files

Delete the following skill directories after their useful guidance is incorporated:

- `brainstorming`
- `dispatching-parallel-agents`
- `receiving-code-review`
- `requesting-code-review`
- `simplify`
- `subagent-driven-development`
- `writing-plans`

Delete their adjacent prompt templates and examples with the directories. The installed `pi-subagents` skill remains the source of truth for subagent tool syntax, execution modes, worktree isolation, and orchestration controls.

## Prompt structure

Each surviving `SKILL.md` will use a compact structure:

1. YAML frontmatter with a precise, trigger-oriented description.
2. A direct statement of the desired outcome.
3. A short workflow containing only decisions or checks that materially affect correctness.
4. Approval boundaries where the skill can cause durable, external, destructive, or scope-expanding effects.
5. Completion criteria and required evidence.
6. Tool examples only where exact syntax is part of the contract.

Skills will avoid announcements, flowcharts, fake dialogues, repeated anti-pattern lists, unsupported performance claims, and repeated references to the universal verification rule.

## Workflow relationships

- `planning` is optional for clear implementation requests and required only when the user requests planning or consequential decisions remain unresolved.
- Normal coding work does not require a repository-specific execution skill. The main coding agent implements directly and may invoke the installed `pi-subagents` skill when delegation is useful.
- `systematic-debugging` may use `test-driven-development` once a supported fault hypothesis exists.
- `code-review` may fix findings when the request authorizes changes, then routes through `verification-before-completion` before reporting completion.
- `commit` and `finishing-a-development-branch` remain explicit because they perform durable repository actions or can cross external/destructive boundaries.
- Every result-producing workflow applies `verification-before-completion` before asserting success, without duplicating its full instructions.

## README changes

Update the `## Skills` table alphabetically so every surviving directory has exactly one row and every deleted directory has none. Rewrite the dependency graph around the smaller library and remove extension dependencies that no surviving repository skill requires. Keep `@fgladisch/pi-user-select` as a required dependency of `commit` and `finishing-a-development-branch` because both workflows confirm consequential repository actions through `user_select`. Retain `pi-subagents` as an optional companion for delegated work rather than a repository-skill dependency.

## Validation

The implementation is complete when:

1. `skills/` contains exactly the seven designed directories.
2. Every directory contains one valid `SKILL.md` with matching `name` frontmatter.
3. README skill rows match the directory inventory exactly and their descriptions agree with skill frontmatter.
4. No surviving file references a deleted skill, template, or path.
5. Markdown formatting checks pass using the repository's configured formatter.
6. A repository-wide search confirms that deleted skill names, `HARD-GATE`, `Iron Law`, `NO PRODUCTION CODE`, `MUST use`, and `REQUIRED SUB-SKILL` no longer appear in surviving skills or README.
7. The final diff preserves the explicit safety boundaries for commits, external writes, destructive actions, and completion claims.

## Non-goals

- Adding model selection or API parameter guidance to skills. These skills govern coding-agent behavior rather than direct Responses API configuration.
- Recreating the `pi-subagents` tool documentation locally.
- Preserving compatibility with deleted `/skill:<name>` invocations.
- Adding a generic implementation skill for behavior already covered by the coding agent's base instructions.
