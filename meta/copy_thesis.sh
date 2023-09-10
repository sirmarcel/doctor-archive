cd ..

mkdir thesis
cd thesis

rsync -rL \
	--exclude "__pycache__/" \
	--exclude "outtakes/" \
	--exclude "*.ist" \
	--exclude "*.aux" \
	--exclude "*.lof" \
	--exclude "*.log" \
	--exclude "*.lot" \
	--exclude "*.fls" \
	--exclude "*.out" \
	--exclude "*.toc" \
	--exclude "*.fmt" \
	--exclude "*.fot" \
	--exclude "*.cb" \
	--exclude "*.cb2" \
	--exclude ".*.lb" \
	--exclude "*.dvi" \
	--exclude "*.xdv" \
	--exclude "*-converted-to.*" \
	--exclude "*.bcf" \
	--exclude "*.blg" \
	--exclude "*-blx.aux" \
	--exclude "*-blx.bib" \
	--exclude "*.run.xml" \
	--exclude "*.fdb_latexmk" \
	--exclude "*.synctex" \
	--exclude "*.synctex(busy)" \
	--exclude "*.synctex.gz" \
	--exclude "*.synctex.gz(busy)" \
	--exclude "*.pdfsync" \
	--exclude "*.bbl" \
	--exclude "*.glg" \
	--exclude "*.glo" \
	--exclude "*.gls" \
	--exclude "*.xmpi" \
	--exclude "get_bib.sh" \
	../../dada-tex/* .
