import subprocess as sp
from pathlib import Path
import shutil


def bake_images(folder):
    for f in folder.glob("*.pdf"):
        print(f)
        infile = f.name
        outfile = f"{f.stem}_emb.pdf"

        cmd = f"gs -dNOPAUSE -dBATCH -sDEVICE=pdfwrite -dPDFSETTINGS=/prepress -dEmbedAllFonts=true -sOutputFile={outfile} -f {infile}"
        sp.run(cmd.split(), cwd=folder)
        shutil.copy(folder / outfile, folder / infile)
        (folder / outfile).unlink()


for folder in [Path("img/plot/gk"), Path("img/reps")]:
    bake_images(folder)
