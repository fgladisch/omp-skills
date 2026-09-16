---
name: lecture-md-convert
description: Convert a lecture or GoodNotes PDF to lecture.md with local Chandra OCR 2 ink separation. Use when the user uploads a lecture PDF after class.
---

# Lecture MD Convert

Position in pipeline: 교수 강의자료 PDF → **본 스킬(원본 .md)** → Deeptutor 예습 → skill 2 (수업용 병합).

## Environment

- Repo: `/tmp/noteitmarkdown` (src layout, run from repo root, `.venv/bin/python`)
- Model snapshot: `/tmp/chandra-ocr-2` (full snapshot with `model.safetensors`)
- Requires Apple MPS (`torch.backends.mps`). Transformers `processor.__call__` warnings are harmless.

## Workflow

1. Confirm input PDF path and a non-existing output dir (pipeline refuses existing dirs).
2. Run from repo root:
   ```
   .venv/bin/python -m noteitmarkdown convert "<INPUT.pdf>" --output "<OUT_DIR>" --model-dir /tmp/chandra-ocr-2
   ```
   Defaults: `--dpi 300 --ink-dpi 600 --ink-cluster-gap-pt 18 --ink-padding-pt 12`.
3. Expect ~40 min for a 35-page PDF on M5 Pro (background the call, wait for delivery).

## Outputs (`OUT_DIR/`)

- `lecture.md` — frontmatter (`source/pages/ink_clusters/reviews`) + `## Page N` sections
- `lecture.review.md` — per-block records (`- page N kind [bbox] ... source ... id:...`) + errors
- `pages/` canonical renders, `figures/` base-figure crops, `ink/` handwriting crops

## Conventions

- Base blocks (`chandra-base`) carry slide text; ink blocks (`chandra-ink`) carry handwriting OCR (confidence always 0.0 = uncalibrated, needs human/LLM review).
- Yellow highlighter (`/Ink` with `/C [1,1,0]`) is excluded from OCR by `ink.py`; see `handwritten-pdf-to-md` for marking + correction.
- Publish is atomic via staging dir; `work/` is removed before publish.

## Verification

- `pages/page-*.png` count == frontmatter `pages`
- `ink_clusters` == files in `ink/`
- Full suite: `.venv/bin/python -m pytest -q` (2 known pre-existing failures: `test_chandra_backend` heading kinds, `test_pipeline` page-001 link — both predate highlight work)
