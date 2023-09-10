from tbx import *
from tbx.gk import *
import seaborn as sns

colors = [black] + sns.color_palette("flare_r", 9)


def get_data(thermo, setting):
    return load(
        gknet / f"kappa_convergence_settings/spacing_{thermo}_{setting}.nc"
    )


def get_label(spacing):
    return str(spacing)


def plot_spacing(ax, data, spacing, style, label_offset=0.0, label_position=0.0):
    color, linestyle = style
    plot_mean_kappa(
        ax,
        data.sel(spacing=spacing).dropna(dim="time"),
        color=color,
        alpha_err=0.0,
        label=get_label(spacing),
        linestyle=linestyle,
    )
    cu, kk = plot_cutoff(
        ax,
        data.sel(spacing=spacing),
        color=color,
        kappa=True,
        cutoff=False,
        linestyle=linestyle,
        alpha_err=0,
    )

    k, kerr = kk
    t = ax.text(label_position, k - label_offset, get_label(spacing))
    t.set_bbox(
        {"facecolor": "white", "alpha": 0.8, "edgecolor": None, "boxstyle": "Round"}
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
        "semi": {
            "xlim": 20e3,
            "ylim": (0, 9.5),
        },
        "unconverged": {
            "xlim": 20e3,
            "ylim": (0, 4.5),
        },
    },
    "m_1400": {
        "converged": {
            "xlim": 8e3,
            "ylim": (0, 3.8),
        },
        "semi": {
            "xlim": 8e3,
            "ylim": (0, 3.8),
        },
    },
    "t_1400": {
        "converged": {
            "xlim": 8e3,
            "ylim": (0, 3.8),
        },
        "semi": {
            "xlim": 8e3,
            "ylim": (0, 3.8),
        },
    },
}


for thermo, other in settings.items():
    for name, s in other.items():
        data = get_data(thermo, name)

        fig, ax = fig_and_ax(figsize=(0.95 * textwidth, 4))

        x = np.linspace(0.1 * s["xlim"], 0.7 * s["xlim"], 11)

        for i, spacing in reversed(list(enumerate(range(1, 11)))):
            plot_spacing(
                ax,
                data,
                spacing,
                (colors[i], solid),
                label_position=x[i],
                label_offset=0.055 * s["ylim"][1],
            )

        setup_ax(ax, ylim=s["ylim"], xlim=s["xlim"])

        savefig(fig, f"spacing/{thermo}_{name}.png")
        savefig(fig, img / f"gk/zro_kc_spacing_{thermo}_{name}.pdf")
