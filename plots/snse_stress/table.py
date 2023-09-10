from shared import *
from tbx.tables import *

settings = {
    "32": {
        "fd": 1e-3,
        "dtype": np.float32,
    },
    "64": {
        "fd": 1e-4,
        "dtype": np.float64,
    },
}

for suffix, s in settings.items():
    print(f"#### {suffix} bits")

    names = {
        # "atom_pair_textbook_mic": "",
        "strain_system": r"\ref{eq:glp_stress_strain_direct}",
        "strain_graph": r"\ref{eq:glp_stress_strain_edges}",
        "unfolded_strain_unfolded": r"\ref{eq:glp_stress_strain_unf}",
        "strain_direct": r"\ref{eq:glp_stress_sc_basis}",
        "atom_pair_direct": r"\ref{eq:glp_stress_edges}",
        "unfolded_direct_unfolded": r"\ref{eq:glp_stress_bulk}",
    }

    titles = [
        "Equation",
        r"\acs{mae} in \unit{eV}",
        r"\acs{maxae} in \unit{eV}",
        r"\acs{mape} in \unit{\percent}",
        r"\acs{maxape} in \unit{\percent}",
    ]

    stress = []

    for key, name in names.items():
        true, pred = get(suffix, key, prop="stress", L=2)
        if "finite_differences" not in key:
            assert pred.dtype == s["dtype"]

        formatter = rounder(2, typ="e")
        losses = [
            r"\num{X}".replace("X", formatter(mae(true, pred))),
            r"\num{X}".replace("X", formatter(maxae(true, pred))),
            r"\num{X}".replace("X", formatter(mape(true, pred))),
            r"\num{X}".replace("X", formatter(maxape(true, pred))),
        ]

        stress.append([name, *losses])

    tab = make_tabular(titles, stress, layout="l | r r r r")
    savetab(tab, tables / f"gk/snse_stress_error_{suffix}.tex")
