from tbx import *
from tbx.tables import *

rounder_lattice = rounder(3)

params = {
    1400: (5.149175824175825, 5.277747252747253),
    1500: (5.154807692307693, 5.2839285714285715),
    1650: (5.164774458619983, 5.2948019774984845),
    1800: (5.174038461538462, 5.3052197802197805),
}


table = []
for key, value in params.items():
    table.append(
        [
            to_num(str(key)),
            to_num(rounder_lattice(value[0])),
            to_num(rounder_lattice(value[1])),
        ]
    )

tab = make_tabular(
    [
        "Temperature in K",
        r"$a$ in \unit{\angstrom}",
        r"$b$ in \unit{\angstrom}",
    ],
    table,
    layout="l|rr",
)

print(tab)
savetab(tab, tables / "gk/zro_cells_tetra.tex")