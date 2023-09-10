from tbx import *
from tbx.gk import *


def get_data(thermo):
    return load(
        gknet / f"kappa_convergence_settings/hfs_mic_{thermo}.nc"
    )


def setup_ax(ax, ylim=(0, 10), xlim=30e3):
    minor_ticks_every(ax, 1000)
    scale_labels(ax, 1000)
    ax.set_xlabel("Integration time in ps")
    ax.set_xlim(0, xlim)

    major_ticks_every(ax, 1, direction="y")

    if ylim[1] >= 5:
        minor_ticks_every(ax, 0.5, direction="y")
    else:
        minor_ticks_every(ax, 0.1, direction="y")

    ax.set_ylabel(kappa_label())
    ax.set_ylim(ylim)

    ax.set_title(None)


settings = {
    "m_300": {
        "xlim": 40e3,
        "ylim": (0, 8.2),
    },
    "m_600": {
        "xlim": 40e3,
        "ylim": (0, 4.4),
    },
    "t_1400": {
        "xlim": 8e3,
        "ylim": (0, 2.2),
    },
    # "m_1400": {
    #     "xlim": 8e3,
    #     "ylim": (0, 2.2),
    # },
}

# jfan_mpnn
# jfan
# jhardy
# junf

js = ["jhardy", "jfan_mpnn", "junf", "jfan"]
labels = {
    "jfan_mpnn": render_j(upper="semi-local"),
    "jfan": render_j(upper="local"),
    "jhardy": render_j(upper="mic"),
    "junf": render_j(upper="unfolded"),
}

styles = {
    "jhardy": {"color": red, "linestyle": solid, "linewidth": 2},
    "junf": {"color": black, "linestyle": (0, (1, 3.5)), "linewidth": 6},
    "jfan": {"color": teal, "linestyle": solid, "linewidth": 2},
    "jfan_mpnn": {"color": orange, "linestyle": (0, (0.25, 2.25)), "linewidth": 4},
}


for thermo, s in settings.items():
    data = get_data(thermo)

    fig, ax = fig_and_ax(figsize=(0.95 * textwidth, 4))

    kappas = {j: data.sel(heat_flux=j) for j in js}

    for j, kappa in kappas.items():
        plot_mean_kappa(ax, kappa, key=kkf, label=labels[j], alpha_err=0.1, **styles[j])

    setup_ax(ax, **s)
    ax.legend(loc="lower right", handlelength=5)

    savefig(fig, f"mic/all_{thermo}.png")
    # savefig(fig, img / f"gk/zro_kc_convective_{thermo}_converged.pdf")
