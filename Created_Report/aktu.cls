\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{aktu}[2026/04/28]

\def\mystretch{1.5}
\DeclareOption{doublespace}{}
\DeclareOption{singlespace}{
    \typeout{Single spaced}
    \def\mystretch{1}}	

\newcount\vithesis
\DeclareOption{vi}{\typeout{Course VI/VIII thesis style.}\advance\vithesis by1}
\vithesis=0

\DeclareOption{upcase}{\typeout{Uppercase cover page.}
	\gdef\choosecase#1{\uppercase\expandafter{#1}}}
\def\choosecase#1{#1}

\newif\if@leftblank \@leftblankfalse
\DeclareOption{leftblank}{\typeout{Intentionally Leaving Pages Blank}
\@leftblanktrue}

\DeclareOption*{\PassOptionsToClass{\CurrentOption}{report}}
\ProcessOptions
\LoadClass{report}

\usepackage{setspace}

\def\baselinestretch{\mystretch}

\setlength{\oddsidemargin}{0.25in}
\setlength{\evensidemargin}{0.25in}
\setlength{\topmargin}{0.0in}
\setlength{\textwidth}{6.0in}
\setlength{\textheight}{9in}
\addtolength{\topmargin}{-\headheight}
\addtolength{\topmargin}{-\headsep}

\def\pulldownheader{
    \addtolength{\topmargin}{\headheight}	
    \addtolength{\topmargin}{\headsep}	
    \addtolength{\textheight}{-\headheight}
    \addtolength{\textheight}{-\headsep}
}

\def\pullupfooter{
    \addtolength{\textheight}{-\footskip}
}

\newcommand{\draftrmark}{**DRAFT**} 
\newcommand{\draftlmark}{**DRAFT**}
\newcommand{\drmark}[1]{\renewcommand{\draftrmark}{#1}}
\newcommand{\dlmark}[1]{\renewcommand{\draftlmark}{#1}}
\newcommand{\dmark}[1]{\drmark{#1}\dlmark{#1}}

\bgroup
\catcode`@=11
\gdef\getfontsize{\f@size pt}
\egroup
\newcommand{\normal}{\fontsize{12pt}{16pt}\selectfont}
\newcommand{\size}{\fontsize{14pt}{18pt}\selectfont}
\newcommand{\bigsize}{\fontsize{16pt}{20pt}\selectfont}
\newcommand{\bigbigsize}{\fontsize{20pt}{24pt}\selectfont}

\def\prevdegrees#1{\gdef\@prevdegrees{#1}}
\def\@prevdegrees{}
\def\department#1{\gdef\@department{#1}}
\def\degree#1{\setbox0\hbox{#1}
  \gdef\@degree{#1}}
\def\and{\gdef\@degreeword{degrees} \par and \par}
\def\@degreeword{degree}

\long\def\copyrightnoticetext#1{\gdef\@copyrightnotice{#1}}
\def\@copyrightnotice{}

\def\thesisdate#1{\gdef\@thesisdate{#1}}
\def\degreemonth#1{\gdef\@degreemonth{#1}}
\def\degreeyear#1{\gdef\@degreeyear{#1}}

\newbox\@titlesupervisor \newbox\@abstractsupervisor

\def\supervisor#1#2{\setbox\@titlesupervisor\vbox
  {\unvbox\@titlesupervisor \vskip 10pt
  \def\baselinestretch{1}\large}}

\def\chairman#1#2{\gdef\@chairmanname{#1}\gdef\@chairmantitle{#2}}

\def\titlepage{\cleardoublepage\centering
  \thispagestyle{}
  \parindent 0pt \parskip 10pt plus 1fil minus 1fil
  \def\baselinestretch{1}\@normalsize\vbox to \vsize\bgroup\vbox to 9in\bgroup}

\def\endtitlepage{\par\kern 0pt\egroup\vss\egroup\newpage}

\def\abstract{\section*{\size ABSTRACT}\small\def\baselinestretch{1}\@normalsize}
\def\endabstract{\par}

\endinput
