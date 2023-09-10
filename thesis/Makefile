clean:
	- rm .DS_Store
	- rm parts/*/*.aux
	- rm *.aux
	- rm *.bbl
	- rm *.blg
	- rm *.brf
	- rm *.fdb_latexmk
	- rm *.fls
	- rm *.log
	- rm *.out
	- rm *.pdf
	- rm *.ptc
	- rm *.synctex.gz
	- rm *.aux
	- rm *.bbl
	- rm *.blg
	- rm *.bcf
	- rm *.xdv
	- rm *.run.xml
	- rm *.gls
	- rm *.glo
	- rm *.glg
	- rm *.ist
	- rm *.toc

thesis:
	$(MAKE) clean
	clear
	pdflatex da.tex
	biber da.bcf
	makeglossaries da
	pdflatex da.tex
	pdflatex da.tex # yes, you need to run it twice
	# now our page numbers in the glossary are wrong:
	# they don't count the glossary itself. so we redo it.
	makeglossaries da
	pdflatex da.tex
	pdflatex da.tex
