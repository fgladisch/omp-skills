---
name: code-review
description: Use when reviewing code.
---

# Code Review

Delegate every change review to focused subagents, evaluate their candidate findings in the main session, and report or address the verified result.

## Authorization

Review and evaluation requests authorize inspection and reporting only. Requests to address, fix, or clean up a change authorize in-scope local edits and non-destructive validation. Confirm before external writes, destructive actions, changing the intended public contract, or materially expanding scope.

## Required prompts

Read both supporting files before reviewing a change:

- [`orchestrator-prompt.md`](./orchestrator-prompt.md) is the main-session contract for scope, task routing, aggregation, and final findings.
- [`category-reviewer-prompt.md`](./category-reviewer-prompt.md) is the prompt and strict output contract for every review subagent.

## Review a change

Use this mode for a diff, working tree, development branch, commit, pull request, or defined file set.

Always hand the review to subagents through the workflow in `orchestrator-prompt.md`. Delegate even a small or single-category change. The main session coordinates scope and tasks; it does not perform a second direct review.

## Evaluate incoming feedback

Use this mode to evaluate candidate findings returned by review subagents. Do not delegate this evaluation again.

For each candidate finding:

1. Confirm the reported location belongs to the active scope and matches the current code.
2. Verify the failure scenario, repository evidence, severity, and supported environments.
3. Accept, reject, or request clarification with a concrete reason.
4. Check whether the proposed correction expands scope, changes the intended contract, or adds unused behavior.

Drop unsupported findings and merge duplicates with the same root cause. Push back directly on incorrect or out-of-scope feedback. The main session reports only accepted findings and concrete coverage gaps.

## Clean up a scoped diff

Use this mode when the user asks to improve a change before completion or integration. Run the delegated review first, evaluate the returned feedback, then apply only accepted in-scope fixes. Preserve the intended contract and validate the changed behavior without re-running a second review pass unless the user requests one.

## Validate

Apply `verification-before-completion` before reporting review conclusions or accepted fixes.
