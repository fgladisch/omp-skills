---
name: worksheet-answers-pdf
description: Build post-class review worksheet + answer-key PDFs from annotated notes and lecture recordings. Use after class when verified handwriting md and 녹음.md exist.
---

# Worksheet + Answers PDF (수업 후: 복습 학습지)

Position in pipeline: 수업 필기/형광펜 + 강의 녹음 → skill 3 (검증 .md) → **본 스킬(복습 PDF)**.

## Inputs (assistant gathers; all must exist)

- ① 검증된 수업 필기 .md (skill 3 output: pen memos corrected, highlighter junk excluded)
- ② 강의 녹음.md (class transcript: explanations, anecdotes, exam hints not in the slides)
- ③ 수업용 강의노트 (skill 2 output: base structure + page refs)
- 녹음에만 있는 내용(교수 멘트·시험 힌트)은 해당 단원 개념 카드에 녹여내고 출처를 `(녹음)`으로 표기한다.

One builder script produces both PDFs (see `lecture-notes-pdf` for profile, Chrome printing, and the exFAT unlink gotcha; full example there).

## Structure: 개념서 + 문제집

Each Unit runs ① 내 필기 되살리기 → ② 개념 정리 → ③ 개념 확인 문제. Proven framework: 48 questions, 400 points, 210 recommended minutes:

| Part | Type | Count | Points | Format |
|---|---|---|---|---|
| A | O/X | 12 | 60 | `.q .no .tag .ox` |
| B | 빈칸 | 10 | 40 | `.q` inline blanks |
| C | 단답 | 10 | 80 | `.q` + `.write` |
| D | 서술 | 8 | 120 | `.q` + `.write tall` |
| E | 도표·연표 | 4 | 60 | `.q` + `.write tall` |
| F | 시나리오 적용 | 4 | 40 | `.q` + `.write tall` |
| G | 백지복습 | 2~3 | 별도 또는 포함 | 주제 프롬프트만 + `.write tall` 대형 쓰기칸 |

Plus a time-table cover card, per-unit ranges + question numbers, a 종합 section, and a 검산 (review) card. Answer key mirrors worksheet numbering exactly with 채점 포인트 + partial-credit rules.

## Content rules

- Pen memos as corrected TEXT in tip boxes (`✎ 내 필기 되살리기`, 판독문 quotes). Never embed ink-crop images.
- 백지복습(G)은 문제 없이 주제 프롬프트만 주고 백지에 재구성시킨다. 해답은 서술이 아니라 모범 구조의 키워드 체크리스트로 만든다.
- Never present highlighter-OCR junk as handwriting. Units without pen notes say so explicitly and point at the concept card instead.
- Every question carries its source page (e.g. `(p.14)`); every figure group title carries its pages.
- Keep worksheet/answer numbering in lockstep; tags show type + points (e.g. `서술 · 15점`).

## Verification

- `.no` sequence is exactly 1..N with no gaps; every referenced figure file exists
- pypdf: all pages non-empty; corrected memos present; raw/junk strings absent
- Question-per-unit distribution matches the cover table
- Render spot-check: content bounds clear of page edges
