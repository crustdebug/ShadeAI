# ShadeAI Report - Compilation Guide

## Quick Start

```bash
cd Created_Report
pdflatex main.tex
pdflatex main.tex
pdflatex main.tex
```

## Before Compilation - Update These:

### 1. Roll Numbers (2 missing):
- **File:** cover.tex, declar&cert.tex
- **Update:** Replace "22CSAIML0XX" with actual roll numbers for:
  - Khushi Yadav
  - Ayush Raj Chauhan

### 2. JSS Logo:
- **File needed:** JSS.png
- **Location:** Created_Report/JSS.png
- **Status:** ✓ Already present (or add if missing)

### 3. Plagiarism Reports:
- **File:** appb.tex
- **Action:** Attach actual plagiarism report PDFs
- **Action:** Add actual AI content detection results

## Report Structure (AKTU Compliant)

### Front Matter (Roman numerals: i, ii, iii...):
1. Cover Page
2. Vision & Mission
3. Program Outcomes (PO & PSO)
4. Course Outcomes Mapping
5. Declaration
6. Certificate
7. Acknowledgement
8. Abstract
9. List of Figures
10. List of Tables
11. List of Symbols & Abbreviations
12. Table of Contents

### Main Content (Arabic numerals: 1, 2, 3...):
1. **Chapter 1:** Introduction (8-10 pages)
2. **Chapter 2:** Literature Review (12-15 pages)
3. **Chapter 3:** System Design and Methodology (15-18 pages)
4. **Chapter 4:** Implementation and Results (18-20 pages)
5. **Chapter 5:** Conclusion and Future Scope (10-12 pages)

### Back Matter:
6. References (3-5 pages)
7. **Appendix A:** List of Papers (2-3 pages)
8. **Appendix B:** Plagiarism Report (3-5 pages)

**Total:** 86-108 pages ✓

## Team Information

### Students:
1. **Khushi Yadav**
   - Roll No: 22CSAIML0XX (UPDATE THIS)
   - Email: yadavkhushi.31.01@gmail.com

2. **Chinmay Nanda**
   - Roll No: 22CSAIML076 ✓
   - Email: 22csaiml076@jssaten.ac.in

3. **Ayush Raj Chauhan**
   - Roll No: 22CSAIML0XX (UPDATE THIS)
   - Email: (not provided)

### Supervisor:
- **Ms. Vishakha Chauhan**
- Assistant Professor
- Department of CSE-AIML
- Email: vishakha.chauhan@jssaten.ac.in

### HOD:
- **Dr. Kakoli Banerjee**
- Head of Department
- Department of CSE-AIML

## Format Compliance

✅ Matches AKTU template exactly
✅ Uses correct chapter format
✅ Declaration/Certificate in template style
✅ Abstract included correctly
✅ 5 chapters (not 6)
✅ All required sections present

## Common Issues & Solutions

### Issue 1: Missing JSS.png
**Solution:** Add JSS Academy logo as JSS.png in Created_Report folder

### Issue 2: Compilation errors
**Solution:** Run pdflatex 3 times to resolve references

### Issue 3: Missing packages
**Solution:** Install full TeX distribution (MiKTeX/MacTeX/TeX Live)

### Issue 4: Roll numbers showing as 0XX
**Solution:** Update in cover.tex and declar&cert.tex

## File Checklist

### Must Have:
- [x] main.tex
- [x] aktu.cls
- [x] name.sty
- [x] All chapter files (1-5)
- [x] All front matter files
- [x] references.tex
- [x] appa.tex, appb.tex
- [ ] JSS.png (verify present)

### Optional:
- [x] README.md
- [x] FORMAT_COMPLIANCE.md
- [x] COMPILATION_GUIDE.md (this file)
- [ ] chapter6.tex (not used, can delete)

## Output

**Expected:** main.pdf (86-108 pages)

**Contents:**
- Professional AKTU-compliant format
- Complete ShadeAI project documentation
- All required sections
- Proper page numbering
- Table of contents with page numbers
- List of figures and tables

## Submission Checklist

Before submitting:
- [ ] Update both missing roll numbers
- [ ] Verify JSS.png is present
- [ ] Compile successfully (no errors)
- [ ] Check page count (should be 80+)
- [ ] Verify all student names correct
- [ ] Verify supervisor name correct
- [ ] Add plagiarism report
- [ ] Add AI content report
- [ ] Print on A4 paper
- [ ] Bind as per university guidelines

## Support

For issues:
1. Check LaTeX log file (main.log)
2. Verify all .tex files present
3. Ensure LaTeX distribution is complete
4. Run pdflatex 3 times

## Project Details

**Title:** ShadeAI: AI-Based Skin Tone and Undertone Detection for Cosmetic Shade Recommendation

**Key Achievements:**
- ΔE = 1.361 (49.6% better than research target)
- 187 foundation shades database
- 85.7% excellent match rate
- Production-ready system
- Multiple interfaces (CLI, Web, API)

**Institution:**
JSS Academy of Technical Education, Noida
Dr. APJ Abdul Kalam Technical University, Lucknow

**Year:** 2025-2026

---

**Status:** ✅ Ready for Compilation
**Format:** ✅ AKTU Compliant
**Page Count:** ✅ 80+ pages
**Last Updated:** May 2026
