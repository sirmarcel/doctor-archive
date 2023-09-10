from tbx import *
from tbx.gk import *


def get_data(thermo, setting):
    return load(
        gknet / f"kappa_convergence_settings/freq_{thermo}_{setting}.nc"
    )


def get_label(freq):
    return r"$\qty{X}{THz}$".replace("X", f"{freq:.1f}")


def plot_freq(ax, data, freq, style):
    color, linestyle = style
    plot_mean_kappa(
        ax,
        data.sel(freq=freq).dropna(dim="time"),
        color=color,
        alpha_err=0.1,
        label=get_label(freq),
        linestyle=linestyle,
    )
    cu, kk = plot_cutoff(
        ax,
        data.sel(freq=freq),
        color=color,
        kappa=True,
        cutoff=False,
        linestyle=linestyle,
        alpha_err=0,
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
        "converged": {
            "xlim": 40e3,
            "ylim": (0, 9.5),
        },
        "unconverged": {
            "xlim": 20e3,
            "ylim": (0, 3.5),
        },
        "semi": {
            "xlim": 20e3,
            "ylim": (0, 7.5),
        },
    },
    "m_1400": {
        "converged": {
            "xlim": 8e3,
            "ylim": (0, 2.7),
        },
        "semi": {
            "xlim": 8e3,
            "ylim": (0, 2.7),
        },
        "unconverged": {
            "xlim": 8e3,
            "ylim": (0, 1.5),
        },
    },
    "t_1400": {
        "converged": {
            "xlim": 8e3,
            "ylim": (0, 2.7),
        },
        "semi": {
            "xlim": 8e3,
            "ylim": (0, 2.7),
        },
        "unconverged": {
            "xlim": 8e3,
            "ylim": (0, 1.5),
        },
    },
}


for thermo, other in settings.items():
    for name, s in other.items():
        data = get_data(thermo, name)

        fig, ax = fig_and_ax(figsize=(0.95 * textwidth, 3.5))

        freqs = {
            0.3: (red, solid),
            0.5: (orange, solid),
            1.0: (black, solid),
            2.0: (blue, solid),
            3.0: (teal, solid),
            # 5.0: (blue, dashdot),
            # 30.0: (blue, loosedot)
        }

        for freq, style in reversed(list(freqs.items())):
            plot_freq(ax, data, freq, style)

        setup_ax(ax, ylim=s["ylim"], xlim=s["xlim"])

        ax.legend(loc="lower right")

        savefig(fig, f"freq/{thermo}_{name}.png")
        savefig(fig, img / f"gk/zro_kc_freq_{thermo}_{name}.pdf")
