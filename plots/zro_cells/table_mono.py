from tbx import *
from tbx.tables import *

rounder_lattice = rounder(3)
rounder_angle = rounder(2)

params = {
    300: [5.147, 5.209, 5.311, 99.3],
    350: [5.150, 5.209, 5.315, 99.28],
    400: [5.152, 5.211, 5.318, 99.27],
    450: [5.154, 5.211, 5.322, 99.26],
    600: [5.161, 5.213, 5.330, 99.166],
    750: [5.165, 5.213, 5.340, 99.073],
    900: [5.172, 5.215, 5.349, 98.99],
    1050: [5.179, 5.216, 5.356, 98.86],
    1200: [5.193, 5.237, 5.386, 98.74],
    1400: [5.196, 5.219, 5.388, 98.687],
}

table = []
for key, value in params.items():
    table.append(
        [
            to_num(str(key)),
            to_num(rounder_lattice(value[0])),
            to_num(rounder_lattice(value[1])),
            to_num(rounder_lattice(value[2])),
            to_num(rounder_angle(value[3])),
        ]
    )

tab = make_tabular(
    [
        "Temperature in K",
        r"$a$ in \unit{\angstrom}",
        r"$b$ in \unit{\angstrom}",
        r"$c$ in \unit{\angstrom}",
        r"$\beta$ in \unit{\degree}",
    ],
    table,
    layout="l|rrrr",
)

print(tab)
savetab(tab, tables / "gk/zro_cells_mono.tex")
