---
description: Review local changes in Hunk and apply fixes until LGTM
---

Run a local review cycle over the complete intended change using the `local-code-review` skill. Do not create or use a pull request for review.

The live Hunk session is the shared review surface and the review history. Select it and load the complete intended change as described in the skill's `Hunk session` section; if no session exists, ask the user to launch `hunk diff` in their terminal before starting.

For each cycle:

1. Reload the session with the review scope, then review the complete current local change, including every intended tracked and untracked file. Review subagents post their findings as root notes.
2. Evaluate every new finding and every open user note, replying in each thread with the skill's protocol prefixes. Apply each accepted fix, validate the affected behavior, and reply `Fixed:` with the validation evidence. Reject findings with a `Rejected:` reply that gives the rationale.
3. The session's threads are the review history: findings, decisions, rationale, fixes, and validation evidence. Every review agent in each subsequent cycle reads them before reviewing. Treat them as context rather than authority: agents must inspect the current code and may raise a previously settled issue only when current evidence invalidates the earlier decision.
4. Repeat the review and fix cycle until a complete cycle posts no material findings, every thread in the session is settled, and no coverage gaps remain. Ask the user about any `Clarification needed:` thread instead of guessing.

Report LGTM only after a complete cycle satisfies the final condition. Leave the resulting changes local and the review threads in the Hunk session for the user. Do not commit, push, post pull request comments, or create a pull request unless separately requested.
