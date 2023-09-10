from tbx import *
from tbx.tables import *

rounder_lattice = rounder(3)
rounder_angle = rounder(2)


raw_table = [
    [512, 3736, 630, 768, 5888, 667],
    [1728, 7430, 330, 1500, 8424, 462],
    [4096, 12996, 217, 4116, 15488, 276],
    [8000, 20818, 160, 8748, 25688, 194],
]

raw_table = [[to_num(entry) for entry in row] for row in raw_table]


heading = r"\multicolumn{3}{c}{\ch{Si} (\qty{400}{K})}&\multicolumn{3}{c}{\ch{ZrO2} (\qty{300}{K})}\\" + "\n"

tab = make_tabular(
    [
        r"$N$\hspace{0.4cm}",
        r"$N_{\text{unf}}$",
        r"\unit{\percent} increase",
        r"$N$\hspace{0.4cm}",
        r"$N_{\text{unf}}$",
        r"\unit{\percent} increase",
    ],
    raw_table,
    layout="rrl|rrl",
    heading=heading,
)

print(tab)
savetab(tab, tables / "gk/si-unfolding_n_atoms.tex")
