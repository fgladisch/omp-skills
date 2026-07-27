# Streamlined Subagent Review Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use subagent-driven-development to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace per-task review loops with one post-plan review stage containing two parallel, narrowly scoped reviewers.

**Architecture:** Workers continue implementing plan tasks sequentially with self-review and task verification. After all tasks, `simplify` reviews the complete plan diff, cleanup changes are committed, and one parallel stage runs a whole-plan spec/integration reviewer beside a whole-branch code-quality reviewer. One fixer worker handles accepted blockers, followed by verification without an automatic reviewer rerun.

**Tech Stack:** Markdown skill definitions, pi `subagent` orchestration examples, Git and ripgrep verification.

**Source spec:** `docs/pi/specs/2026-07-27-streamlined-subagent-review-design.md`

---

## File Map

- Modify `skills/simplify/SKILL.md`: accept an explicit Git comparison range while preserving working-tree defaults.
- Modify `skills/subagent-driven-development/SKILL.md`: define the sequential implementation and single parallel review-stage workflow.
- Create `skills/subagent-driven-development/final-reviewer-prompt.md`: whole-plan compliance and cross-task integration review contract.
- Modify `skills/subagent-driven-development/code-quality-reviewer-prompt.md`: whole-branch implementation-quality review contract.
- Delete `skills/subagent-driven-development/spec-reviewer-prompt.md`: remove the obsolete per-task compliance prompt.
- Modify `skills/requesting-code-review/SKILL.md`: align review timing with the post-plan parallel stage.
- Modify `skills/writing-plans/SKILL.md`: update the execution handoff and related-skill description.
- Modify `skills/finishing-a-development-branch/SKILL.md`: clarify that subagent-driven development hands off after simplify, formal review, fixes, and verification.
- Verify `README.md`: keep unchanged unless its skill index or descriptions no longer match frontmatter.

### Task 1: Add explicit comparison ranges to `simplify`

**Files:**
- Modify: `skills/simplify/SKILL.md:8-16`

- [ ] **Step 1: Document the optional range input before Phase 1**

Add this contract after the overview:

```markdown
## Optional Comparison Range

A caller may provide an explicit Git comparison range such as
`<base-sha>..<head-sha>`. When supplied, review that committed range instead
of the working tree. This is required for workflows whose changes were already
committed, including `subagent-driven-development`.
```

- [ ] **Step 2: Replace Phase 1 diff selection with deterministic precedence**

Use this behavior:

```markdown
## Phase 1: Identify Changes

Choose the review diff in this order:

1. If the caller supplied a comparison range, run `git diff <base>..<head>`.
2. Otherwise, run `git diff` (or `git diff HEAD` for staged changes).
3. If the selected diff is empty, review the recently modified files named by
   the user or changed earlier in the conversation.

Record the selected range or working-tree scope so all three reviewers inspect
exactly the same diff.
```

Do not change the three review angles or their parallel dispatch behavior.

- [ ] **Step 3: Verify the range contract and unchanged default**

Run:

```bash
rg -n 'Optional Comparison Range|caller supplied a comparison range|git diff <base>\.\.<head>|Otherwise, run `git diff`' skills/simplify/SKILL.md
git diff --check -- skills/simplify/SKILL.md
```

Expected: `rg` prints the new range and fallback rules; `git diff --check` exits 0.

- [ ] **Step 4: Commit**

```bash
git add skills/simplify/SKILL.md
git commit -m "📝 docs: support ranged simplify reviews"
```

Expected: one commit containing only `skills/simplify/SKILL.md`.

### Task 2: Define the two final reviewer contracts

**Files:**
- Create: `skills/subagent-driven-development/final-reviewer-prompt.md`
- Modify: `skills/subagent-driven-development/code-quality-reviewer-prompt.md`
- Delete: `skills/subagent-driven-development/spec-reviewer-prompt.md`

- [ ] **Step 1: Create the whole-plan final reviewer prompt**

Create `final-reviewer-prompt.md` with these sections and responsibilities:

```markdown
# Final Reviewer Prompt Template

This file's content is the `task` string for the whole-plan specification and
integration reviewer. Dispatch it in parallel with
`./code-quality-reviewer-prompt.md` after all plan tasks and `simplify` are
complete.

## CRITICAL: Read Only. Do Not Edit.

Report findings only. Inspect the repository directly and do not trust worker
summaries.

## Inputs

Plan: [absolute plan path]
Working directory: [absolute path]
Branch: [branch]
Base SHA: [SHA before plan implementation]
Head SHA: [SHA after simplify cleanup commit]
Implementation summary: [all worker summaries]
Verification commands: [commands required by the plan]

## Scope

Check only:
- Every plan requirement and acceptance criterion is implemented.
- No unrequested behavior or scope was added.
- Requirements spanning tasks work together coherently.
- Cross-task interfaces, data flow, and integration agree.
- Verification evidence exercises the completed result.

Do not assess general naming, style, decomposition, maintainability,
performance, or security unless the plan explicitly requires them. The
parallel code-quality reviewer owns those concerns.

Inspect `git diff <base>..<head>`, resulting files at HEAD, and relevant tests.

## Report Format

Strengths:
  - <evidence-backed strength>
Issues:
  Critical:
    - <plan or integration blocker with file:line>
  Important:
    - <material mismatch with file:line>
  Minor:
    - <non-blocking observation with file:line>
Assessment: APPROVED | NEEDS CHANGES

APPROVED means no Critical or Important findings. Do not request or assume a
re-review. The controller owns finding disposition and verification.
```

Keep the prompt concise and preserve the responsibility boundary from the design spec.

- [ ] **Step 2: Rewrite the code-quality prompt for the whole branch**

Change its title and dispatch context from a second per-task pass to a parallel whole-branch pass. Its inputs must be:

```markdown
Plan: [absolute plan path, context only]
Working directory: [absolute path]
Branch: [branch]
Base SHA: [SHA before plan implementation]
Head SHA: [SHA after simplify cleanup commit]
Implementation summary: [all worker summaries]
Verification commands: [commands required by the plan]
```

Its scope must include implementation-detail correctness risks, meaningful test coverage, maintainability, naming, decomposition, project conventions, security, error handling, concurrency, performance, dead code, and boundary leaks. Add this exclusion explicitly:

```markdown
Do not perform line-by-line plan compliance or report missing/extra product
requirements. The parallel final reviewer owns specification and cross-task
integration compliance.
```

Keep the `Strengths / Issues / Assessment` format and add:

```markdown
Do not request or assume a re-review. The controller owns finding disposition
and verification after fixes.
```

- [ ] **Step 3: Remove the obsolete per-task spec prompt**

```bash
rm skills/subagent-driven-development/spec-reviewer-prompt.md
```

Expected: the file no longer exists; its whole-plan responsibilities now live in `final-reviewer-prompt.md`.

- [ ] **Step 4: Verify both scopes are separate and the old prompt is gone**

Run:

```bash
test -f skills/subagent-driven-development/final-reviewer-prompt.md
test -f skills/subagent-driven-development/code-quality-reviewer-prompt.md
test ! -e skills/subagent-driven-development/spec-reviewer-prompt.md
rg -n 'whole-plan|Cross-task|Do not assess general naming' skills/subagent-driven-development/final-reviewer-prompt.md
rg -n 'whole branch|Do not perform line-by-line plan compliance|Do not request or assume a re-review' skills/subagent-driven-development/code-quality-reviewer-prompt.md
git diff --check -- skills/subagent-driven-development
```

Expected: all commands exit 0 and each `rg` reports only its intended scope.

- [ ] **Step 5: Commit**

```bash
git add skills/subagent-driven-development/final-reviewer-prompt.md skills/subagent-driven-development/code-quality-reviewer-prompt.md skills/subagent-driven-development/spec-reviewer-prompt.md
git commit -m "📝 docs: define plan-level review scopes"
```

Expected: one commit containing the new final prompt, rewritten quality prompt, and deleted spec prompt.

### Task 3: Rewrite the subagent-driven development workflow

**Files:**
- Modify: `skills/subagent-driven-development/SKILL.md`

- [ ] **Step 1: Replace the opening review contract**

State the workflow as:

```markdown
Execute a plan by dispatching one fresh worker per task, then run `simplify`
once and gate the completed plan on one parallel review stage: whole-plan
specification/integration review plus whole-branch code-quality review.

**Core principle:** Fresh worker per task + one bounded post-plan review stage = focused implementation without review loops.
```

Remove every claim that review happens after each task or that spec review must precede code-quality review.

- [ ] **Step 2: Replace the role table and process diagram**

The role table must contain:

| Role | Builtin agent | Timing |
|------|---------------|--------|
| Implementer | `worker` | Once per plan task, sequentially |
| Simplify reviewers | `reviewer` | Once after all tasks, three parallel cleanup angles |
| Final spec/integration reviewer | `reviewer` | In the single formal parallel review stage |
| Code-quality reviewer | `reviewer` | In the same formal parallel review stage |
| Fixer | `worker` | At most once when accepted blockers exist |

Use this process ordering in the DOT graph:

```dot
"Read plan, capture base SHA, create todo list"
  -> "Dispatch fresh worker for next task"
  -> "Worker implements, tests, commits, self-reviews"
  -> "Worker status acceptable?"
  -> "More tasks remain?"
  -> "Run simplify on base SHA..HEAD"
  -> "Verify and commit simplify cleanup"
  -> "Capture shared review head SHA"
  -> "Dispatch final + code-quality reviewers in parallel"
  -> "Aggregate and disposition findings"
  -> "Blocking findings?"
  -> "Dispatch one fixer worker"
  -> "Run full-plan verification and inspect final diff"
  -> "Use finishing-a-development-branch";
```

Include status-resolution edges for worker questions, `NEEDS_CONTEXT`, `DONE_WITH_CONCERNS`, and `BLOCKED`. The fixer path returns directly to full-plan verification, never to reviewers.

- [ ] **Step 3: Replace reviewer dispatch instructions with one parallel call**

Document that `baseSha` is captured before Task 1, `reviewHeadSha` is captured after the simplify cleanup commit, and both prompts are filled with the same range. Show this call:

```typescript
subagent({
  tasks: [
    {
      agent: "reviewer",
      task: "<filled ./final-reviewer-prompt.md>",
      output: "<temp-dir>/final-review.md"
    },
    {
      agent: "reviewer",
      task: "<filled ./code-quality-reviewer-prompt.md>",
      output: "<temp-dir>/code-quality-review.md"
    }
  ],
  context: "fresh",
  concurrency: 2
})
```

Require an OS temp directory for distinct report files. Both reviewers must be read-only and inspect `baseSha..reviewHeadSha`.

- [ ] **Step 4: Define finding synthesis and the single fixer dispatch**

Document these rules exactly:

```markdown
- Critical and Important findings block handoff.
- Minor findings are deferred when no fixer is needed.
- Reject duplicates, false positives, out-of-scope suggestions, and findings
  contradicted by repository evidence.
- When blockers remain, dispatch one fresh fixer worker with all accepted
  blockers and any cheap, safe, in-scope Minor findings.
- The fixer runs complete plan verification and commits once.
- Do not automatically re-run either reviewer. A further focused review needs
  an explicit, concrete risk decision from the controller or user.
```

The fixer prompt must include the plan path, base/head range, both reports, accepted findings, constraints, verification commands, and the required worker report format.

- [ ] **Step 5: Update worker status, async, worktree, example, and red-flag sections**

Preserve the existing worker status handling and sequential write safety. Update review-specific content so:

- `DONE` advances to the next task after the controller verifies the report and task evidence.
- Async remains optional for long workers; the parallel final review stage is one coordinated call.
- Worktree guidance does not introduce parallel writes in the active worktree.
- The example implements at least two tasks without intermediate reviewers, runs ranged `simplify`, commits cleanup, dispatches both reviewers together, synthesizes findings, runs at most one fixer, and finishes with verification.
- Red flags prohibit per-task reviewer dispatches, sequential final reviewer dispatch, automatic re-review, moving formal review before simplify, and capturing review HEAD before cleanup is committed.

- [ ] **Step 6: Update prompt and integration references**

The prompt list must contain only:

```markdown
- `./implementer-prompt.md`
- `./final-reviewer-prompt.md`
- `./code-quality-reviewer-prompt.md`
```

The integration section must describe `simplify` before formal review, `requesting-code-review` as the basis for the quality prompt, and `finishing-a-development-branch` after findings, fixes, and verification are complete.

- [ ] **Step 7: Verify stale per-task review language is gone**

Run:

```bash
! rg -n 'two-stage review|review after each task|spec compliance first|re-dispatch.*reviewer|loop until.*approv|spec-reviewer-prompt' skills/subagent-driven-development/SKILL.md
rg -n 'simplify.*base|parallel review|final-reviewer-prompt|code-quality-reviewer-prompt|one fixer|Do not automatically' skills/subagent-driven-development/SKILL.md
git diff --check -- skills/subagent-driven-development/SKILL.md
```

Expected: the negative search exits 0, the positive search reports the new workflow, and diff checking exits 0.

- [ ] **Step 8: Commit**

```bash
git add skills/subagent-driven-development/SKILL.md
git commit -m "♻️ refactor: streamline subagent review workflow"
```

Expected: one commit containing only the workflow skill rewrite.

### Task 4: Align dependent skill guidance

**Files:**
- Modify: `skills/requesting-code-review/SKILL.md:10-75`
- Modify: `skills/writing-plans/SKILL.md:145-159`
- Modify: `skills/finishing-a-development-branch/SKILL.md:193-200`

- [ ] **Step 1: Update requesting-code-review timing and integration**

Replace the subagent-driven-development-specific rules with:

```markdown
**Mandatory:**
- After the complete implementation plan in subagent-driven development
- After completing a major feature
- Before merge to main when no equivalent final review has already run

**Subagent-Driven Development:**
- Review once after the complete plan and `simplify` cleanup are committed.
- Dispatch the final spec/integration reviewer and code-quality reviewer in
  parallel as one formal review stage.
- Synthesize findings before sending accepted blockers to one fixer worker.
- Do not create an automatic re-review loop.
```

Keep ad-hoc review instructions and the standard code-review template available.

- [ ] **Step 2: Update writing-plans execution handoff**

Replace the stale handoff with:

```markdown
Plan complete and saved to `docs/pi/plans/<filename>.md`.

If you want, I can execute it now with subagent-driven-development: fresh
worker per task, then one parallel plan-level review stage after implementation
and simplify. Want me to start?
```

Update the two following bullets to use the same wording and remove all references to two-stage per-task review.

- [ ] **Step 3: Clarify the finishing handoff**

Change the `subagent-driven-development` integration line to:

```markdown
- **subagent-driven-development** - After all tasks, simplify cleanup, the
  parallel formal review stage, accepted fixes, and full-plan verification.
```

Do not make `finishing-a-development-branch` run simplify again when the current diff range has already been simplified.

- [ ] **Step 4: Verify cross-skill consistency**

Run:

```bash
! rg -n 'review after EACH task|After each task in subagent-driven development|fresh subagent per task plus two-stage review|Fresh subagent per task \+ two-stage review|fresh workers and two-stage review' skills/requesting-code-review/SKILL.md skills/writing-plans/SKILL.md
rg -n 'complete implementation plan|parallel.*review|automatic re-review' skills/requesting-code-review/SKILL.md
rg -n 'parallel plan-level review stage' skills/writing-plans/SKILL.md
rg -n 'parallel formal review stage|full-plan verification' skills/finishing-a-development-branch/SKILL.md
git diff --check -- skills/requesting-code-review/SKILL.md skills/writing-plans/SKILL.md skills/finishing-a-development-branch/SKILL.md
```

Expected: stale searches return no matches; new workflow searches match; diff checking exits 0.

- [ ] **Step 5: Commit**

```bash
git add skills/requesting-code-review/SKILL.md skills/writing-plans/SKILL.md skills/finishing-a-development-branch/SKILL.md
git commit -m "📝 docs: align plan-level review guidance"
```

Expected: one commit containing the three dependent skill updates.

### Task 5: Run repository-wide workflow verification

**Files:**
- Verify: `README.md`
- Verify: `skills/*/SKILL.md`
- Verify: `skills/subagent-driven-development/*.md`

- [ ] **Step 1: Search the repository for obsolete workflow claims**

Run:

```bash
! rg -n 'two-stage review|review after EACH task|After each task in subagent-driven development|spec-reviewer-prompt|spec compliance first|review loop hard to follow' README.md skills
```

Expected: no matches.

- [ ] **Step 2: Verify prompt references and files**

Run:

```bash
test -f skills/subagent-driven-development/implementer-prompt.md
test -f skills/subagent-driven-development/final-reviewer-prompt.md
test -f skills/subagent-driven-development/code-quality-reviewer-prompt.md
test ! -e skills/subagent-driven-development/spec-reviewer-prompt.md
rg -n 'implementer-prompt\.md|final-reviewer-prompt\.md|code-quality-reviewer-prompt\.md' skills/subagent-driven-development/SKILL.md
```

Expected: all file assertions pass and all three active templates are referenced.

- [ ] **Step 3: Verify README skill-directory synchronization**

Run:

```bash
ls -1 skills | grep -v '^\.'
rg '^\| `[^`]+`' README.md
```

Compare the outputs manually. Expected: every skill directory has exactly one alphabetically ordered README row, every row points to an existing directory, and each “When to use” description remains consistent with the corresponding frontmatter description.

- [ ] **Step 4: Verify the final diff and Markdown hygiene**

Run:

```bash
first_impl_sha=$(git log --format='%H' --fixed-strings --grep='📝 docs: support ranged simplify reviews' -1)
implementation_base_sha=$(git rev-parse "${first_impl_sha}^")
git diff --check "${implementation_base_sha}..HEAD"
git status --short
git log --oneline "${implementation_base_sha}..HEAD"
```

Expected: `git diff --check` exits 0; status contains no unexpected files; the log shows the four implementation commits from Tasks 1-4. The pre-existing `.gitignore` change for `.pi-subagents/` may remain unless it was committed separately with user approval.

- [ ] **Step 5: Inspect the complete workflow against the source spec**

Read:

```text
docs/pi/specs/2026-07-27-streamlined-subagent-review-design.md
skills/subagent-driven-development/SKILL.md
skills/subagent-driven-development/final-reviewer-prompt.md
skills/subagent-driven-development/code-quality-reviewer-prompt.md
```

Expected: implementation uses one formal post-plan stage with two parallel reviewers, one optional fixer worker, and no automatic re-review.
