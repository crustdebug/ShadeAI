# ShadeAI Final Year Project Report

This folder contains the complete LaTeX source files for the ShadeAI final year project report.

## Report Structure

The report is organized according to JSS Academy of Technical Education and AKTU guidelines:

### Main Files
- `main.tex` - Main document file that includes all chapters
- `aktu.cls` - Custom document class for AKTU thesis format

### Front Matter
- `cover.tex` - Title page
- `VM.tex` - Vision and Mission
- `POPSO.tex` - Program Outcomes and Program Specific Outcomes
- `CO-PO_PSO.tex` - Course Outcomes mapping
- `declar&cert.tex` - Declaration, Certificate, and Acknowledgement
- `abstract.tex` - Abstract
- `FT.tex` - List of Figures and Tables
- `sa.tex` - List of Symbols and Abbreviations
- `contents.tex` - Table of Contents

### Main Chapters
- `chapter1.tex` - Introduction (Problem Statement, Motivation, Objectives, Scope)
- `chapter2.tex` - Literature Review
- `chapter3.tex` - System Design and Methodology
- `chapter4.tex` - Implementation and Results
- `chapter5.tex` - Conclusion and Future Scope
- `chapter6.tex` - Additional Information

### Back Matter
- `references.tex` - References and Bibliography
- `appa.tex` - Appendix A: List of Papers
- `appb.tex` - Appendix B: Plagiarism and AI Content Report

## Compilation Instructions

### Prerequisites
1. Install a LaTeX distribution:
   - **Windows**: MiKTeX (https://miktex.org/)
   - **macOS**: MacTeX (https://www.tug.org/mactex/)
   - **Linux**: TeX Live (`sudo apt-get install texlive-full`)

2. Install required LaTeX packages (usually included in full distributions):
   - times, fontenc, titlesec, geometry, setspace
   - graphicx, comment, titletoc
   - listings, xcolor, amsmath
   - algorithm, algpseudocode
   - booktabs, multirow, longtable
   - hyperref

### Compilation Steps

#### Method 1: Using Command Line

```bash
# Navigate to the Created_Report directory
cd Created_Report

# Compile (run multiple times for references)
pdflatex main.tex
pdflatex main.tex
pdflatex main.tex
```

#### Method 2: Using LaTeX Editor

1. Open `main.tex` in your LaTeX editor (TeXstudio, Overleaf, etc.)
2. Click "Build" or "Compile"
3. The editor will automatically run pdflatex multiple times

#### Method 3: Using Overleaf (Online)

1. Create a new project on Overleaf (https://www.overleaf.com/)
2. Upload all `.tex` files and `aktu.cls`
3. Set `main.tex` as the main document
4. Click "Recompile"

### Expected Output

The compilation will generate:
- `main.pdf` - The complete report (80+ pages)
- `main.aux`, `main.log`, `main.toc` - Auxiliary files

## Customization

### Before Compilation, Update:

1. **cover.tex**:
   - Replace "Student Name 1-4" with actual names
   - Replace "Roll No. XXXXXXXX" with actual roll numbers
   - Replace "Dr. Supervisor Name" with actual supervisor name
   - Add JSS.png logo file to the directory

2. **declar&cert.tex**:
   - Update student names and roll numbers
   - Update supervisor name
   - Update HOD name
   - Update Director name
   - Update dates

3. **abstract.tex**:
   - Review and customize if needed

4. **appa.tex** (Appendix A):
   - Add actual paper titles if published
   - Update publication status
   - Add conference/journal names

5. **appb.tex** (Appendix B):
   - Add actual plagiarism report percentages
   - Add actual AI content detection results
   - Attach actual reports from detection tools

## Report Statistics

- **Total Pages**: 80+ pages
- **Chapters**: 6 main chapters
- **Appendices**: 2
- **Figures**: Multiple (tables, diagrams, code listings)
- **References**: 50+ citations
- **Word Count**: ~25,000 words

## Content Overview

### Chapter 1: Introduction (8-10 pages)
- Problem Statement
- Motivation
- Project Objectives
- Scope of the Project
- Organization of the Report

### Chapter 2: Literature Review (12-15 pages)
- Skin Tone Classification Systems
- Color Science and Color Spaces
- Computer Vision Techniques
- Existing Systems
- Research Gap

### Chapter 3: System Design and Methodology (15-18 pages)
- System Overview
- System Architecture
- Pipeline Modules (6 modules)
- Foundation Database
- Photo Quality Assessment
- User Interfaces

### Chapter 4: Implementation and Results (18-20 pages)
- Implementation Details
- Software/Hardware Requirements
- Test Cases
- Performance Evaluation
- Comparison with State-of-the-Art

### Chapter 5: Conclusion and Future Scope (10-12 pages)
- Achievement of Objectives
- Key Contributions
- Lessons Learned
- Future Enhancements (Short, Medium, Long-term)

### Chapter 6: Additional Information (5-7 pages)
- System Requirements
- Installation Guide
- Usage Examples
- Troubleshooting

## Troubleshooting

### Common Issues

1. **Missing JSS.png**:
   - Add the JSS Academy logo file to the directory
   - Or comment out the `\includegraphics` line in cover.tex

2. **Package Not Found**:
   - Install missing packages using your LaTeX distribution's package manager
   - For MiKTeX: Packages install automatically on first use
   - For TeX Live: `sudo tlmgr install <package-name>`

3. **Compilation Errors**:
   - Check the `.log` file for detailed error messages
   - Ensure all `.tex` files are in the same directory
   - Run pdflatex multiple times (3x) for references

4. **Formatting Issues**:
   - Check that `aktu.cls` is in the same directory
   - Verify all `\include` statements in main.tex

## Quality Checklist

Before final submission, verify:

- [ ] All student names and roll numbers updated
- [ ] Supervisor and HOD names updated
- [ ] All dates updated to current
- [ ] JSS logo added
- [ ] Plagiarism report attached
- [ ] AI content report attached
- [ ] All references properly formatted
- [ ] Page numbers correct
- [ ] Table of contents generated
- [ ] List of figures and tables generated
- [ ] No compilation errors
- [ ] PDF opens correctly
- [ ] All chapters present
- [ ] Minimum 80 pages achieved

## File Size

Expected PDF size: 2-5 MB (depending on images)

## Printing Guidelines

For final submission:
- **Paper**: A4 size, 80 GSM
- **Printing**: Double-sided (if allowed) or single-sided
- **Binding**: Spiral or hard binding as per university guidelines
- **Copies**: As required by university (typically 3-4 copies)
- **Color**: Black and white acceptable, color preferred for figures

## Support

For issues or questions:
1. Check the LaTeX log file for errors
2. Consult LaTeX documentation
3. Contact project team members
4. Refer to university thesis guidelines

## License

This report template follows JSS Academy and AKTU formatting guidelines.
The content is original work by the project team.

## Acknowledgments

- JSS Academy of Technical Education for the format guidelines
- AKTU for thesis specifications
- LaTeX community for excellent documentation

---

**Last Updated**: May 2026
**Version**: 1.0
**Status**: Ready for Compilation
