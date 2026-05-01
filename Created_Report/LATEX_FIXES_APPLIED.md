# LaTeX Compilation Fixes Applied

## Date: May 1, 2026

### Issues Fixed:

1. **main.tex - Line 26: Removed invalid `\setsecheadstyle` command**
   - This command does not exist in LaTeX
   - Removed the line entirely

2. **cover.tex - Lines 5-8: Removed duplicate font size command definitions**
   - Commands `\normal`, `\size`, `\bigsize`, `\bigbigsize` are already defined in aktu.cls
   - Removed duplicate definitions from cover.tex

3. **cover.tex - Line 49: Fixed double backslash**
   - Changed `\\\\` to single line break
   - Removed standalone `\\` that caused "no line here to end" errors

4. **cover.tex - Added \title and \author commands**
   - Added `\title` and `\author` commands for abstractpage environment
   - These are required by the abstractpage environment

5. **abstract.tex - Replaced all Unicode Delta (Δ) characters**
   - Changed all `ΔE` to `$\Delta E$` for proper LaTeX rendering
   - Fixed 5 occurrences in abstract.tex

6. **All .tex files - Replaced Unicode Delta characters**
   - Used PowerShell to replace all `ΔE` with `$\Delta E$` across all files
   - Fixed occurrences in:
     * chapter4.tex (multiple occurrences)
     * chapter5.tex (multiple occurrences)
     * chapter6.tex (multiple occurrences)
     * sa.tex (1 occurrence in abbreviations)

7. **declar&cert.tex - Removed standalone backslashes**
   - Removed `\\` after `\end{center}` in DECLARATION section
   - Removed `\\` after `\end{center}` in CERTIFICATE section
   - Removed `\\` before `\begin{flushleft}` in CERTIFICATE section
   - Removed `\\` before `\begin{flushright}` in ACKNOWLEDGEMENT section
   - Removed `\\` at end of file after `\restoregeometry`
   - These caused "There's no line here to end" errors

8. **aktu.cls - Added abstractpage environment definition**
   - Added `\def\abstractpage{...}` definition from template
   - Added `\newcounter{savepage}` for abstract page numbering
   - This fixes "Environment abstractpage undefined" error

9. **chapter3.tex - Replaced Unicode box-drawing characters**
   - Changed Unicode tree characters (├─│└) to ASCII equivalents (|--+)
   - These were causing "Unicode character not set up for use with LaTeX" errors
   - Changed in the project structure diagram

### Files Modified:
- Created_Report/main.tex
- Created_Report/cover.tex
- Created_Report/abstract.tex
- Created_Report/declar&cert.tex
- Created_Report/aktu.cls
- Created_Report/chapter3.tex
- Created_Report/chapter4.tex
- Created_Report/chapter5.tex
- Created_Report/chapter6.tex (note: this file should not be included per template)
- Created_Report/sa.tex

### Remaining Issues to Check:
1. "Entered in horizontal mode" errors from titlesec package
   - These may be caused by improper section usage
   - Need to verify section/subsection placement

2. Verify chapter6.tex is not included in main.tex
   - Template only has 5 chapters
   - Already removed from main.tex in previous fixes

### Compilation Status:
Ready for compilation test. All major syntax errors have been addressed.

### Next Steps:
1. Compile the document to verify all fixes
2. Check for any remaining warnings
3. Verify page count meets 80+ page requirement
4. Update roll numbers (22CSAIML0XX) with actual values
