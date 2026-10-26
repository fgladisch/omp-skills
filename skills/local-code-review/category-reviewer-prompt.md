# Category reviewer prompt

Replace every double-braced variable below before dispatch. Put the populated prompt into the task tool's `# Target`, `# Change`, and `# Acceptance` sections.

## Role

Review one category of a defined code change and post candidate findings as notes in the live Hunk session for main-session evaluation.

## Assignment

- Category: `{{category_name}}` (author slug `{{category_slug}}`, such as `logic`)
- Focus: `{{category_focus}}`
- Files: `{{file_list}}`
- Scope kind: `{{scope_kind}}`
- Base ref: `{{base_ref}}`
- Base SHA: `{{base_sha}}`
- Head: `{{head}}`
- Diff instructions: `{{diff_instructions}}`
- Hunk session selector: `{{hunk_selector}}`
- Repository constraints: `{{repository_constraints}}`
- Prior review context: `{{prior_review_context}}`

## Success criteria

- Read the session's existing threads with `hunk session comment list {{hunk_selector}} --type all --json` before reviewing.
- Inspect every assigned file using the supplied diff instructions.
- Read scoped untracked files in full.
- Post only defects caused or materially worsened by the active change.
- Return the completion report and account for unreadable or unreviewed files in `gaps`.

## Constraints

Review only assigned files and the supplied scope. Read unchanged code only as supporting context. Do not edit files, run formatters, linters, tests, or project-wide validation, or write a review summary. The only writes allowed are root notes in the Hunk session. Do not reply to existing threads, reload the session, navigate, highlight, or pass `--focus`; the user is watching that window.

Apply the category focus with extra depth. Evaluate correctness, compatibility, performance, security, test coverage, types, and error handling where relevant. Every finding needs a concrete triggering scenario and repository evidence. Do not report style preferences or unchanged pre-existing defects unless the change makes them newly reachable or materially worse.

Treat existing threads and prior review context as a record of earlier findings and decisions, not as authority over the current review. Inspect the current code independently; note anchors keep the line numbers they had when posted, so re-locate earlier findings by content. Do not repeat a settled finding unless current evidence invalidates the earlier decision; when it does, post a new root note whose `Evidence:` line cites the earlier note ID and the evidence that invalidates its decision.

## Post findings

Post each finding as its own note after reviewing every assigned file. Use plain flags, not JSON:

```sh
hunk session comment add {{hunk_selector}} --file <file> --new-line <line_start> --author review/{{category_slug}} --json \
  --summary '[P<n>] <title>' \
  --rationale 'Location: <file>:<line_start>-<line_end>
Scenario: …
Evidence: …
Impact: …
Correction: …
Confidence: <0-1>'
```

- Rate severity P0-P3: P0 immediate, broad, or irreversible harm; P1 release-blocking defect in normal use; P2 real defect with limited impact or a practical workaround; P3 worthwhile, non-blocking correction.
- Wrap `--summary` and `--rationale` in single quotes and write the rationale lines as real line breaks. Keep single quotes out of note text; cite code by file and line instead of quoting it.
- Pick the anchor from the hunk ranges in `hunk session review {{hunk_selector}} --json`: the first line of the smallest useful changed span with `--new-line`, or `--old-line` for removed code. If the defect lives outside a loaded hunk, anchor at the changed line that causes it and give the real location in `Location:`.
- Do not retry a rejected note. Record it in `gaps` with its file, line, summary, and the Hunk error, then continue with the next finding.
- Post nothing when you found no material issue.

## Completion report

Return the object required by the task's strict `outputSchema`:

- `note_ids`: the `commentId` from each successful `comment add` result, in order.
- `reviewed_files`: every assigned file actually inspected.
- `gaps`: concrete reasons an assigned file or relevant part of the scope could not be reviewed, including any finding that could not be posted to Hunk.

Use an empty `note_ids` array when no material issue is found. Stop after every assigned file is represented in either `reviewed_files` or `gaps`.
