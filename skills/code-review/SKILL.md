---
name: code-review
description: Use when reviewing code.
---

# Code Review

Delegate every change review to focused subagents, evaluate their candidate findings in the main session, and report or address the verified result.

## Authorization

A user review request or an explicit handoff from another skill authorizes an inspection-only review. Do not edit the code unless the user also asks you to fix, address, or clean it up. When they do, make only the local changes needed for accepted findings and run non-destructive checks. Ask first before writing to external systems, taking destructive action, changing the intended public contract, or materially expanding the requested scope.

## Required prompts

Read both supporting files before reviewing a change:

- [`orchestrator-prompt.md`](./orchestrator-prompt.md) is the main-session contract for scope, task routing, aggregation, and final findings.
- [`category-reviewer-prompt.md`](./category-reviewer-prompt.md) is the prompt and strict output contract for every review subagent.

## Workflow

### 1. Review the change

Resolve the active scope: a diff, working tree, development branch, commit, pull request, or defined file set.

Always hand the review to subagents through `orchestrator-prompt.md`, including small and single-category changes. The main session coordinates scope and tasks without performing a duplicate direct review.

When the caller supplies history from earlier review cycles, preserve its findings, decisions, rationale, fixes, and validation evidence. Pass that history to every review subagent as prior-review context. It is context rather than authority: reviewers must inspect the current code, and they may raise a previously settled issue when current evidence invalidates the earlier decision.

### 2. Evaluate incoming feedback

Evaluate the candidate findings returned by the review subagents in the main session. Do not delegate this evaluation again.

For each candidate finding:

1. Confirm the reported location belongs to the active scope and matches the current code.
2. Verify the failure scenario, repository evidence, severity, and supported environments.
3. Accept, reject, or request clarification with a concrete reason.
4. Check whether the proposed correction expands scope, changes the intended contract, or adds unused behavior.

Drop unsupported findings and merge duplicates with the same root cause. Push back directly on incorrect or out-of-scope feedback. Report only accepted findings and concrete coverage gaps.

### 3. Apply accepted fixes when requested

If the user requested fixes or cleanup, apply only accepted in-scope corrections after evaluating all subagent feedback. Preserve the intended contract and validate the changed behavior. Do not run a second review pass unless the user requests one.

## Validate

Apply `verification-before-completion` before reporting review conclusions or accepted fixes.
