---
name: code-review
description: Use when inspecting a change for defects, evaluating incoming review feedback, or cleaning up a scoped diff before completion or integration.
---

# Code Review

Find material defects in a defined change, evaluate claims against repository evidence, and apply in-scope fixes when requested.

## Shared review principles

Establish the intended behavior, repository conventions, and exact diff or feedback items. Load authoritative `pr://` or `issue://` context when available, and inspect the current code and tests instead of relying on summaries. If required scope cannot be inferred, ask for the smallest missing fact.

Choose the mode from the requested outcome: findings for a change review, evidence-backed dispositions for incoming feedback, or an improved diff for cleanup. When a request combines outcomes, satisfy each without repeating the same inspection.

Review and evaluation requests authorize inspection and reporting only. Requests to address, fix, or clean up a change authorize in-scope local edits and non-destructive validation. Confirm before external writes, destructive actions, changing the intended public contract, or materially expanding scope.

## Delegate proportionally

Review small, scoped changes directly. Delegate to one or more `reviewer` agents when independent judgment, breadth, or risk materially improves coverage. Batch reviewers only for genuinely independent angles.

Add a `security-reviewer` when the change crosses a trust boundary or materially affects authentication, authorization, secrets, cryptography, or handling of untrusted input. Give every agent the exact scope, intended behavior, relevant repository constraints, and a distinct review angle.

Agent reports are candidate findings. Confirm each reported location, failure mechanism, severity, and applicability against the current files. Drop unsupported findings and synthesize one deduplicated result.

## Review a change

Use this mode when the user asks to inspect a diff, pull request, commit, or set of files for defects.

Prioritize defects affecting correctness, security, data integrity, compatibility, performance, and maintainability. Check for missing requirements, regressions, unhandled boundaries, duplicated behavior, unnecessary complexity, and tests that do not defend the changed contract.

Report findings in severity order:

- **P0** — immediate, broad, or irreversible harm;
- **P1** — release-blocking defect in normal use;
- **P2** — real defect with limited impact or a practical workaround;
- **P3** — worthwhile but non-blocking correction.

Each finding must include the exact file and location, failure scenario, repository evidence, specific correction, and confidence. Do not inflate style preferences into defects. If no material finding exists, say so and identify any validation gap.

## Evaluate incoming feedback

Use this mode when the user provides existing review comments and asks whether they are correct or asks to address them.

For each comment:

1. Verify the technical claim against current code, requirements, and supported environments.
2. Accept, reject, or request clarification with evidence.
3. Check whether the proposed correction expands scope or adds unused behavior.

Push back directly on incorrect or out-of-scope advice.

## Clean up a scoped diff

Use this mode when the user asks to improve an existing diff before completion or integration. Inspect only the defined change for material correctness, maintainability, performance, and test-quality problems. Fix defects within that change directly while preserving its intended contract.

## Validate

Apply `verification-before-completion` before reporting review conclusions or accepted fixes.
