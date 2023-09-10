cd ..

mkdir plots
cd plots

rsync -rL --exclude "__pycache__/" --exclude ".git" --exclude ".gitignore" --exclude "archive" --exclude ".envrc" --exclude ".gitattributes" --exclude "gaas*" --exclude "present" --exclude ".direnv" ../../dada-plot/* .