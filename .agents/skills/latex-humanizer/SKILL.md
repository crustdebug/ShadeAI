---
name: latex-humanizer
description: Scans and refines multi-file LaTeX reports to ensure high originality, zero plagiarism, and human-like readability (high perplexity/burstiness) while strictly preserving LaTeX syntax. Use when finalizing technical reports.
---

# LaTeX Originality & Humanizer

## When to use this skill
- Use this when the user asks to make their LaTeX report "AI free," "plagiarism free," or to "humanize" the text.
- This is required for multi-file LaTeX projects where text is spread across `\input{}` or `\include{}` files.

## Execution Rules & Constraints

### 1. LaTeX Syntax Preservation (CRITICAL)
- **NEVER** alter LaTeX commands, environments, or macros.
- Strict preservation of all mathematical notations, algorithms, and co-author data. 
- Do not modify `\cite{}`, `\ref{}`, `\label{}`, or bibliography files (`.bib`).

### 2. Plagiarism Elimination
- Identify generic, repetitive, or widely used academic phrasing.
- Restructure sentences to use active voice and unique, domain-specific vocabulary (e.g., utilize specific AI/ML, computer vision, or system architecture terms relevant to the surrounding text).
- Ensure technical claims are phrased originally rather than parroting standard textbook definitions.

### 3. AI Detection Bypass (Humanization)
- **Optimize Burstiness:** Vary sentence length dramatically. Human writing naturally mixes short, punchy sentences with longer, complex analytical ones. AI defaults to uniform, monotonous sentence lengths.
- **Optimize Perplexity:** Avoid highly predictable word sequences. Strip out standard AI transitional crutches ("Furthermore," "In conclusion," "It is important to note," "Delving into").
- **Tone Alignment:** Maintain a formal but authentic engineering/research tone.

### 4. Workflow
- Read `main.tex` to map out the document tree.
- Process each `.tex` file individually.
- Present a standardized code diff for review before executing the file write.