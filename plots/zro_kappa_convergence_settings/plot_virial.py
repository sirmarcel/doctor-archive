from tbx import *
from tbx.gk import *


def get_data(thermo):
    return load(gknet / f"kappa_convergence_settings/virial_{thermo}.nc")


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
        "ylim": (0, 6.8),
    },
    "m_600": {
        "xlim": 40e3,
        "ylim": (0, 3.8),
    },
    "m_1400": {
        "xlim": 4e3,
        "ylim": (0, 4.2),
    },
    "t_1400": {
        "xlim": 4e3,
        "ylim": (0, 4.2),
    },
}

for thermo, s in settings.items():
    data = get_data(thermo)

    fig, ax = fig_and_ax(figsize=(0.95 * textwidth, 4))

    k_oneshot = isotropic(data[kkm])
    k_virials = isotropic(data[kkm + "_virials"])

    k_oneshot.plot(ax=ax, color=black, label="Virials with Supercell")
    k_virials.plot(
        ax=ax, color=red, linestyle=dotted, label="Virials from Trajectory Mean"
    )

    setup_ax(ax, **s)
    ax.legend(loc="lower right")

    savefig(fig, f"virial/{thermo}.png")
    savefig(fig, img / f"gk/si-zro_gkc_virial_{thermo}.pdf")
