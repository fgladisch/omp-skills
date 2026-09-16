---
name: handwritten-pdf-to-md
description: Turn handwriting in a converted lecture.md into verified text: highlighter exclusion, ==highlight== mapping, and LLM correction by the assistant. Use when lecture.md contains ink OCR.
---

# Handwritten PDF to MD

Position in pipeline: 수업 필기된 GoodNotes PDF → **본 스킬(검증 .md)** → skill 4 (복습 PDF). Skill 1이 같은 convert를 쓰지만 본 스킬은 필기 검증까지 포함한다.

## Automatic: highlighter → `== ==` marking

- `ink.extract_highlights(pdf)` collects yellow regions (never OCR).
- Pipeline converts them to render-pixel boxes and passes `highlights=` to `generate_lecture_md`, which wraps only intersecting text lines in Obsidian `==highlight==` (formulas/visuals never).
- For outputs made before this feature: `markdown.rewrap_lecture_md_with_highlights(lecture_md, review_md, highlights)` replays the line layout against review bboxes. Gate: empty highlights must reproduce the input byte-identically.
- Limits (state honestly): line boxes are even vertical splits of Chandra block boxes, so multi-item single-line lists highlight block-wide. Verify hits geometrically (known case: p.10 last list line, p.14 title + first list line).

## Manual: LLM correction (the assistant is the model)

No cloud call, no separate model step. The assistant corrects ink texts in-session:

1. Read ink-derived lines in `lecture.md` with page context from `lecture.review.md` (text + bbox only, minimal scope).
2. Correct minimally, never change intent; if unsure, leave as-is. Reconstructed tails must be flagged.
3. Replace in every `lecture.md` copy; append originals to `lecture.review.md`:
   ```
   ## LLM handwriting corrections (assistant as model)
   - page 6: "→ 대북분 PPT 기반" -> "→ 대부분 PPT 기반" (대북분은 대부분 오독, 문맥상 확정)
   ```
4. Sync corrected strings into PDF builder memo boxes and rebuild the 3 PDFs.

## Known ground truth (인터넷과 메타버스 1주차)

- Genuine pen exists only on p.6/10/11/20. Everything else previously labeled handwriting was highlighter-over-print OCR junk — never present such lines as handwriting.
- Corrected memos: p.6 "→ 대부분 PPT 기반" · p.10 "⇒ 도서관은 상징적인 의미로 변할" (no change) · p.11 "~ 1990년대까지 유지" (spacing) · p.20 "이미지 정보를 쉽게 읽을 수 있게 됨" (reconstructed tail, flagged).

## Verification

- `extract_highlights` on the real PDF finds exactly the yellow annots; extraction count drops by that number (observed: 140 → 125)
- `==` count matches geometric expectation; corrected strings present, raw strings absent in md + PDFs
- Full pytest green except the 2 known pre-existing failures (see `lecture-md-convert`)
