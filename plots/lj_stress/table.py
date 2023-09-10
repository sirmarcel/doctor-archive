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

    data = get_data(suffix=suffix)

    fd = s["fd"]

    names = {
        "atom_pair_textbook_mic": r"\acs{mic} (offset)",
        "atom_pair_fractional_mic": r"\acs{mic} (frac.)",
        # "direct_strain_system": r"\ref{eq:glp_stress_strain_direct}",
        # "direct_strain_graph": r"\ref{eq:glp_stress_strain_edges}",
        # "direct_strain_direct": r"\ref{eq:glp_stress_sc_basis}",
        # "unfolded_system": "",
        "unfolded_direct_unfolded": r"Unfolded",
        # f"finite_differences_{fd:.0e}": "Fin. diff.",
    }

    energy = []

    for key, name in names.items():
        if "finite_differences" in key:
            continue

        true, pred = get(data, key, prop="energy")
        if "finite_differences" not in key:
            assert pred.dtype == s["dtype"]

        formatter = rounder(2, typ="e")
        losses = [
            r"\num{X}".replace("X", formatter(mae(true, pred))),
            r"\num{X}".replace("X", formatter(maxae(true, pred))),
            r"\num{X}".replace("X", formatter(mape(true, pred))),
            r"\num{X}".replace("X", formatter(maxape(true, pred))),
        ]

        energy.append([name, *losses])

    titles = [
        "Comment",
        r"\acs{mae} in \unit{eV}",
        r"\acs{maxae} in \unit{eV}",
        r"\acs{mape} in \unit{\percent}",
        r"\acs{maxape} in \unit{\percent}",
    ]

    tab = make_tabular(titles, energy, layout="l | r r r r")

    # print(table_to_string(energy, width=24))
    savetab(tab, tables / f"gk/si-lj_energy_error_{suffix}.tex")


    names = {
        "atom_pair_textbook_mic": (r"\acs{mic} (offset)", r"edges"),
        "atom_pair_fractional_mic": (r"\acs{mic} (frac.)", r"edges"),
        "strain_system": (r"\acs{mic} (offset)", r"direct"),
        "strain_graph": (r"\acs{mic} (frac.)", r"direct"),
        # "direct_strain_direct": r"\ref{eq:glp_stress_sc_basis}",
        # "unfolded_system": "",
        "unfolded_direct_unfolded": (r"Unfolded", r"direct"),
        # f"finite_differences_{fd:.0e}": "Fin. diff.",
    }

    forces = []

    for key, name in names.items():
        if "finite_differences" in key:
            continue

        true, pred = get(data, key, prop="forces")
        if "finite_differences" not in key:
            assert pred.dtype == s["dtype"]

        formatter = rounder(2, typ="e")
        losses = [
            r"\num{X}".replace("X", formatter(mae(true, pred))),
            r"\num{X}".replace("X", formatter(maxae(true, pred))),
            # r"\num{X}".replace("X", formatter(mape(true, pred))),
            # r"\num{X}".replace("X", formatter(maxape(true, pred))),
        ]

        forces.append([name[0], name[1], *losses])


    titles = [
        "Comment",
        "Grads",
        r"\acs{mae} in \unit{eV\per\angstrom}",
        r"\acs{maxae} in \unit{eV\per\angstrom}",
        # r"\acs{mape} in \unit{eV\per\angstrom}",
        # r"\acs{maxape} in \unit{eV\per\angstrom}",
    ]


    tab = make_tabular(titles, forces, layout="l l | r r")
    savetab(tab, tables / f"gk/si-lj_forces_error_{suffix}.tex")

    names = {
        # "atom_pair_textbook_mic": "",
        f"finite_differences_{fd:.0e}": "Fin. diff.",
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
        true, pred = get(data, key, prop="stress")
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
    savetab(tab, tables / f"gk/si-lj_stress_error_{suffix}.tex")
