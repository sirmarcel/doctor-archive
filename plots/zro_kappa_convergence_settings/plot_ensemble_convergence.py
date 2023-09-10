from tbx import *
from tbx.gk import *

import seaborn as sns

colors = list(reversed([black] + sns.color_palette("flare_r", 5)))
sizes = [1, 3, 5, 7, 9, 11]


def get_data(thermo, setting):
    return load(
        gknet / f"kappa_convergence_settings/overview_{thermo}_{setting}.nc"
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
            "ylim": (0, 8.5),
        },
        # "semi": {
        #     "xlim": 20e3,
        #     "ylim": (0, 9.5),
        # },
        # "unconverged": {
        #     "xlim": 20e3,
        #     "ylim": (0, 4.5),
        # },
    },
    "m_1400": {
        "converged": {
            "xlim": 8e3,
            "ylim": (0, 2.2),
        },
        # "semi": {
        #     "xlim": 8e3,
        #     "ylim": (0, 3.8),
        # },
    },
    "t_1400": {
        "converged": {
            "xlim": 8e3,
            "ylim": (0, 2.2),
        },
        # "semi": {
        #     "xlim": 8e3,
        #     "ylim": (0, 3.8),
        # },
    },
}

for thermo, other in settings.items():
    for name, s in other.items():
        xlim = s["xlim"]
        ylim = s["ylim"]

        fig, ax = fig_and_ax(figsize=(0.95 * textwidth, 3.5))

        data = get_data(thermo, name)

        kappa = isotropic(data[kkf])
        hfacf = isotropic(data[khfacff])

        label_offset = 0.055 * ylim[1]
        x = np.linspace(0.1 * xlim, 0.7 * xlim, len(sizes))

        for ii, i in enumerate(sizes):
            mean_kappa = kappa.isel(trajectory=slice(0, i)).mean(dim="trajectory")
            mean_kappa.plot(ax=ax, color=colors[ii], label=f"{i}")

            mean_hfacf = hfacf.isel(trajectory=slice(0, i)).mean(dim="trajectory")
            cutoff = mean_hfacf.time[mean_hfacf < 0].min()
            k = mean_kappa.sel(time=cutoff).data
            ax.axhline(
                k,
                color=colors[ii],
                # linestyle=linestyles[key],
                # linewidth=3,
            )

            # t = ax.text(x[ii], k - label_offset, str(i))
            # t.set_bbox(
            #     {"facecolor": "white", "alpha": 0.8, "edgecolor": None, "boxstyle": "Round"}
            # )

        setup_ax(ax, xlim=xlim, ylim=ylim)

        ax.legend(loc="lower right")

        savefig(fig, f"ensemble_convergence/{thermo}_{name}.png")
        savefig(fig, img / f"gk/zro_kc_ens_conv_{thermo}_{name}.pdf")
