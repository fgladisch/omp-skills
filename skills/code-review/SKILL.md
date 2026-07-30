---
name: code-review
description: Use when reviewing a change, evaluating code-review feedback, or cleaning up a scoped diff before completion or integration.
---

# Code Review

Find material defects in a defined change, evaluate findings against repository evidence, and fix accepted issues when the request authorizes edits.

## Establish scope

Determine:

- the diff, files, commit range, or feedback items under review;
- the intended behavior and relevant project conventions;
- whether the request authorizes review only or also authorizes local fixes.

Inspect the code and tests instead of relying on summaries. If the scope is unclear and cannot be inferred, ask before reviewing the wrong change.

## Review

Prioritize findings that affect correctness, security, data integrity, compatibility, or maintainability. Check for missing requirements and tests, regressions, duplicated existing behavior, unnecessary complexity, and avoidable performance costs.

Each finding must include:

- severity;
- exact file and location;
- the concrete failure or risk;
- supporting evidence;
- a specific correction.

Return findings in severity order. Do not inflate stylistic preferences into defects. If no material findings exist, say so and name any validation gap.

## Use subagents selectively

Review directly by default. Use one fresh, read-only subagent when independent judgment or task shape materially improves confidence. Use parallel reviewers only when a broad or high-risk diff has distinct review angles that justify the extra cost. Give every subagent the same explicit scope and ask for findings only. The parent validates and synthesizes their reports.

## Evaluate incoming feedback

For each review comment:

1. Restate the technical claim when clarification is useful.
2. Verify it against the current code, requirements, and supported environments.
3. Accept, reject, or ask about the finding with evidence.
4. Check whether the proposed change expands scope or adds unused behavior.

Implement accepted findings when edits are authorized. Push back directly on incorrect or out-of-scope advice. Avoid performative agreement.

## Fix and validate

Keep fixes scoped to accepted findings. Run focused checks for the changed behavior, then broader validation proportional to regression risk. Apply `verification-before-completion` before claiming the review or fixes are complete.
