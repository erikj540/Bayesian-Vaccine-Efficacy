# Miscelleneous
- Overleaf's documentation is wonderful
- CTAN (Comprehensive TeX Archive Network) is central place for all kinds of materials around TeX and LaTeX including packages and classes
- 
- If you use cross-references and BibTeX for bibliography, you often have to run LaTeX more than once to compile correctly. `latexmk` helps avoid all that hassle. It is part of the `MacTeX` and `MikTeX`. 
- `latexmk`, `pdflatex`, `bibtex` are command line utitlies. 

- Difference between `usepackage` and `RequirePackage` is minimal. You can't use `usepackage` before declaring the document class

- See [here](https://www.overleaf.com/learn/latex/page_size_and_margins) for `geometry` package options. And for the [gory details](https://ctan.math.illinois.edu/macros/latex/contrib/geometry/geometry.pdf)

- `\def` vs `\newcommand`: `\def` is a TeX primitive while `\newcommand` is a LaTeX overlay on top of `\def`. Anything `\newcommand` does can be done by `\def` but it usually involves more trickery

- TeX vs LaTeX: TeX is both a program (which does the typesetting, `tex-core`) and format (a set of macros that the engine uses, `plain-tex`). Looked at in either way, TeX gives you the basics only. 

LaTeX is a generalised set of macros to let you do many things. Most people don't want to have to program TeX, especially to set up things like sections, title pages, bibliographies and so on. LaTeX provides all of that: these are the 'macros' that it is made up of.

# [Images](https://www.overleaf.com/learn/latex/Inserting_Images#Reference_guide)
- Units: `pt` = 0.3515mm, `mm`, `cm`, `in`, `\linewidth` (width of line in current environment), `\columnwidth`, `\columnsep`, `\textwidth`, etc.
```
\includegraphics[width=\textwidth]{universe}
OR 
\begin{figure}[h]
\includegraphics[width=0.5\textwidth, inner]{lion-logo}
\caption{Caption}
\label{fig:figure2}
\end{figure}
```
- [positioning](https://www.overleaf.com/learn/latex/Positioning_images_and_tables)

# [Environments](https://www.overleaf.com/learn/latex/Environments)
- Environments are used to format blocks of text. 
- Environments are delimited by an opening `\begin` tag and closing `\end`. Everything inside those tags will be formatted in particular manner. 
- You can define new environments using `\newenvironment` tag. Can also overwrite existing definition of an environment with `\renewenvironment`. 

# LaTeX in VS Code
- `settings.json` file is 
- using Latex Workshop extension
- to get preview to autoreload on save, in the `TEX` window click `View in VSCode`
- in `settings.json` in `"latex-workshop.latex.recipes"`, I moved the `"pdflatex ➞ bibtex ➞ pdflatex × 2"` entry to be the first one
- Preview in VS Code Tab wasn't as nice as I might like plus having the other tab open was annoying so I added the following to my `settings.json` to use the PDF viewer `Skim.app` as. Use `cmd+opt+j` to open Skim viewer
```
"latex-workshop.view.pdf.viewer": "external",
    "latex-workshop.view.pdf.external.viewer.command": "/Applications/Skim.app/Contents/SharedSupport/displayline",
    "latex-workshop.view.pdf.external.viewer.args": [ "0", "%PDF%" ],
    "latex-workshop.view.pdf.external.synctex.command": "/Applications/Skim.app/Contents/SharedSupport/displayline",
    "latex-workshop.view.pdf.external.synctex.args": [ "-r", "%LINE%", "%PDF%", "%TEX%" ],
    "files.exclude": {
        "**/_minted-*": true,
        "**/*.aux": true,
        "**/*.bbl": true,
        "**/*.blg": true,
        "**/*.lof": true,
        "**/*.log": true,
        "**/*.lol": true,
        "**/*.lot": true,
        "**/*.nav": true,
        "**/*.out": true,
        "**/*.snm": true,
        "**/*.swp": true,
        "**/*.toc": true,
        "**/*.vrb": true
    },
```

# Formatting
- Default formatting in LaTeX documents is determined by the **class** of the document. This default can be changed and more functionalities added by means of a package. Class files have `.cls` extension. Package files have the `.sty` extension.
- The basic rule is that if your file contains commands that control the look of the logical structure of a special type of document, then it's a class. Otherwise, if your file adds features that are independent of the document type, i.e. can be used in books, reports, articles and so on; then it's a package.
- See [here](https://www.overleaf.com/learn/latex/Writing_your_own_package) for writing a package

- For [here](https://www.overleaf.com/learn/latex/Management_in_a_large_project) for inputting files (e.g., `input` vs `include` vs `subfiles`)
