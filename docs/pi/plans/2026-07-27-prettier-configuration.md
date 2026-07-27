# Prettier Configuration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use subagent-driven-development to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Configure deterministic Markdown formatting that preserves existing prose wrapping, aligns tables, and uses Prettier 3.9.6 in the local pre-commit hook.

**Architecture:** A tracked root Prettier configuration defines repository formatting behavior. The existing local pre-commit hook consumes that configuration through a pinned Prettier version, while the repository Markdown corpus is formatted once and verified for idempotence.

**Tech Stack:** Prettier 3.9.6, JSON, POSIX shell, Git

---

### Task 1: Add the repository Prettier configuration

**Files:**

- Create: `.prettierrc.json`

- [ ] **Step 1: Verify the configuration is absent**

Run:

```bash
test ! -e .prettierrc.json
```

Expected: exit 0, confirming the configuration has not been created yet.

- [ ] **Step 2: Write a failing configuration assertion**

Run:

```bash
test "$(node -p "require('./.prettierrc.json').proseWrap")" = preserve
```

Expected: FAIL because `.prettierrc.json` does not exist.

- [ ] **Step 3: Create the configuration**

Create `.prettierrc.json` with exactly:

```json
{
  "proseWrap": "preserve"
}
```

- [ ] **Step 4: Verify the configuration assertion passes**

Run:

```bash
test "$(node -p "require('./.prettierrc.json').proseWrap")" = preserve
```

Expected: exit 0.

### Task 2: Pin the local pre-commit hook to Prettier 3.9.6

**Files:**

- Modify: `.git/hooks/pre-commit:30`

- [ ] **Step 1: Verify the hook has not been updated yet**

Run:

```bash
if rg -q 'prettier@3\.9\.6' .git/hooks/pre-commit; then
  exit 1
fi
```

Expected: exit 0 because the hook still references Prettier 3.6.2.

- [ ] **Step 2: Update the hook version**

Replace:

```sh
xargs -0 npx --yes prettier@3.6.2 --write -- < "$staged_markdown"
```

with:

```sh
xargs -0 npx --yes prettier@3.9.6 --write -- < "$staged_markdown"
```

Do not change any other hook behavior. `.git/hooks/pre-commit` is local Git metadata and must remain outside the commit.

- [ ] **Step 3: Verify the hook version and syntax**

Run:

```bash
rg -n 'xargs -0 npx --yes prettier@3\.9\.6 --write --' .git/hooks/pre-commit
sh -n .git/hooks/pre-commit
```

Expected: one matching formatter line and exit 0 from the shell syntax check.

### Task 3: Format and verify the Markdown corpus

**Files:**

- Modify: tracked `*.md` files only when Prettier 3.9.6 changes their formatting
- Stage before formatting: `.prettierrc.json`
- Stage before formatting: `docs/pi/plans/2026-07-27-prettier-configuration.md`

- [ ] **Step 1: Add the new tracked files to the formatting corpus**

Run:

```bash
git add -- .prettierrc.json docs/pi/plans/2026-07-27-prettier-configuration.md
```

Expected: both paths appear in `git ls-files`.

- [ ] **Step 2: Format every tracked Markdown file**

Run:

```bash
git ls-files -z '*.md' | xargs -0 npx --yes prettier@3.9.6 --write --
```

Expected: Prettier completes with exit 0. Changes are formatting-only.

- [ ] **Step 3: Verify all tracked Markdown uses the configured style**

Run:

```bash
git ls-files -z '*.md' | xargs -0 npx --yes prettier@3.9.6 --check --
```

Expected: `All matched files use Prettier code style!`

- [ ] **Step 4: Verify formatting is idempotent**

Run:

```bash
before=$(mktemp)
after=$(mktemp)
trap 'rm -f "$before" "$after"' EXIT HUP INT TERM
git diff --binary HEAD -- > "$before"
git ls-files -z '*.md' | xargs -0 npx --yes prettier@3.9.6 --write --
git diff --binary HEAD -- > "$after"
cmp "$before" "$after"
```

Expected: `cmp` exits 0, proving a second formatter run made no changes.

- [ ] **Step 5: Verify tables remain aligned**

Run:

```bash
rg '^\| Skill[[:space:]]{2,}\|' README.md
```

Expected: the `README.md` skills table header matches with spacing before the closing separator.

### Task 4: Verify and amend the formatting commit

**Files:**

- Stage: `.prettierrc.json`
- Stage: `docs/pi/plans/2026-07-27-prettier-configuration.md`
- Stage: any tracked Markdown changed by Prettier 3.9.6
- Exclude: `.git/hooks/pre-commit`

- [ ] **Step 1: Run final verification**

Run:

```bash
test "$(node -p "require('./.prettierrc.json').proseWrap")" = preserve
rg -q 'prettier@3\.9\.6' .git/hooks/pre-commit
sh -n .git/hooks/pre-commit
git ls-files -z '*.md' | xargs -0 npx --yes prettier@3.9.6 --check --
git diff --check
```

Expected: every command exits 0 and Prettier reports all tracked Markdown formatted.

- [ ] **Step 2: Confirm scope and stage the complete tracked change**

Run `git status --short` first and stop if it shows any tracked Markdown change unrelated to this formatting work. Then run:

```bash
git add -- .prettierrc.json
git ls-files -z '*.md' | xargs -0 git add --
git status --short
```

Expected: `.prettierrc.json`, this plan, and any formatter-updated Markdown are staged. No unrelated path is staged.

- [ ] **Step 3: Amend the approved formatting commit**

Run:

```bash
git commit --amend --no-edit
```

Expected: the commit subject remains `📝 docs: normalize markdown formatting`, and the pre-commit hook runs Prettier 3.9.6 without producing further changes.

- [ ] **Step 4: Verify the amended result**

Run:

```bash
git status --short --branch
git show --stat --oneline --summary HEAD
npx --yes prettier@3.9.6 --check .prettierrc.json
git ls-files -z '*.md' | xargs -0 npx --yes prettier@3.9.6 --check --
```

Expected: the branch is one commit ahead of `origin/main`, the working tree is clean, `.prettierrc.json` is committed, and every formatting check passes.
