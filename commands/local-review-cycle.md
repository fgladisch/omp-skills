---
description: Review local changes and apply fixes until LGTM
---

Run a local review cycle over the complete intended change using the `code-review` skill. Do not create or use a pull request for review.

For each cycle:

1. Review the complete current local change, including every intended tracked and untracked file.
2. Evaluate every finding. Apply each accepted fix, validate the affected behavior, and record rejected findings with their rationale.
3. Maintain a review history containing prior findings, decisions, rationale, fixes, and validation evidence. Give that history to every review agent in each subsequent cycle. Treat it as context rather than authority: agents must inspect the current code and may raise a previously settled issue only when current evidence invalidates the earlier decision.
4. Repeat the local review and fix cycle until the review reports no material findings and no unresolved coverage gaps.

Report LGTM only after a complete cycle satisfies the final condition. Leave the resulting changes local; do not commit, push, post comments, or create a pull request unless separately requested.
