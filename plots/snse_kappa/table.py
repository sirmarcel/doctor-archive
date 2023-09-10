from tbx import *
from tbx.tables import *
from tbx import gk

plot_cutoff = gk.plot_cutoff


def format_kappa(kappa, err=None):
    kappa = rounder(2)(kappa)
    if err is not None:
        err = round_up_to_digits(err, 2)
        err = rounder(2)(err)
        return with_stderr(kappa, err)
    else:
        return with_stderr(kappa)


reference = load(glp / "snse_kappa/reference.npz")


table_us = []
for L in [1, 2, 3]:
    data = load(glp / f"snse_kappa/sokrates_L{L}_prod.nc")

    _, k_e = plot_cutoff(None, data, kappa=False, cutoff=False, a=None, eps=0)
    kappa_isotropic, kappa_isotropic_stderr = k_e

    kappas = []
    kappas_stderr = []
    for a in [0, 1, 2]:
        _, k_e = plot_cutoff(None, data, kappa=False, cutoff=False, a=a, eps=0)
        kappas.append(k_e[0])
        kappas_stderr.append(k_e[1])

    components = [format_kappa(k, e) for k, e in zip(kappas, kappas_stderr)]

    if L == 1:
        this = "This work"
    else:
        this = r"\hspace{0.5cm}\textquotedbl"

    table_us.append(
        [
            this,
            r"\sok, $\interactions{=}X$".replace("X", str(L)),
            format_kappa(kappa_isotropic, kappa_isotropic_stderr),
            *components,
        ]
    )

table = []

components_brorsson = [format_kappa(k, None) for k in reference["brorsson"]]
table.append(
    [
        r"Brorsson~\etal~\cite{bhke2021t}",
        r"\acs{fcp}",
        format_kappa(reference["brorsson"].mean(), None),
        *components_brorsson,
    ]
)

components_li = [
    format_kappa(k, e) for k, e in zip(reference["liu"], reference["liu_errors"])
]
table.append(
    [
        r"Liu~\etal~\cite{lqzg2021q}",
        r"\acs{mlp}",
        format_kappa(reference["liu"].mean(), reference["liu_errors"].mean()),
        *components_li,
    ]
)

components_empty = ["--"] * 3

table.append(
    [
        r"Knoop~\etal~\cite{kpsc2023t}",
        r"\acs{dft} (extrapolated)",
        format_kappa(reference["knoop"].mean(), reference["knoop_errors"].mean()),
        *components_empty,
    ]
)
# table.append(
#     [
#         "Zhao et al.",
#         "Exp. (single)",
#         format_kappa(reference["zhao"], None),
#     ]
# )
table.append(
    [
        r"Review by Wei~\etal~\cite{wbcr2016t}",
        "Experiments",
        r"\num{0.45} to \num{1.9}",
        *components_empty,
    ]
)

tab = make_tabular(
    [
        "Source",
        "Method",
        kappa_label(),
        r"$\kappa_{\text{x}}$",
        r"$\kappa_{\text{y}}$",
        r"$\kappa_{\text{z}}$",
    ],
    None,
    layout="llr|rrr",
    tables=[table_us, table]
)

print(tab)
savetab(tab, tables / "gk/snse_kappa.tex")
