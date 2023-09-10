from tbx import *
from tbx.gk import *


kkt = kk + "_total"
kkft = kkf + "_total"
kkmt = kkm + "_total"
kkfmt = kkfm + "_total"
kkfst = kkfs + "_total"

khfacfmt = khfacfm + "_total"
khfacffmt = khfacffm + "_total"

suffixes = {
    "no_filter_no_gauge": "_mean_total",
    "no_filter_w_gauge": "_mean",
    "w_filter_no_gauge": "_filtered_mean_total",
    "w_filter_w_gauge": "_filtered_mean",
}

labels = {
    "no_filter_no_gauge": r"Filter $\times$ ~ Gauge $\times$",
    "w_filter_no_gauge": r"Filter \checkmark ~ Gauge $\times$",
    "no_filter_w_gauge": r"Filter $\times$ ~ Gauge \checkmark",
    "w_filter_w_gauge": r"Filter \checkmark ~ Gauge \checkmark",
}

colors = {
    "no_filter_no_gauge": red,
    "w_filter_no_gauge": teal,
    "no_filter_w_gauge": orange,
    "w_filter_w_gauge": black,
}

linestyles = {
    "no_filter_no_gauge": solid,
    "w_filter_no_gauge": solid,
    "no_filter_w_gauge": solid,
    "w_filter_w_gauge": dotted,
}


def get_data(thermo, setting):
    return load(
        gknet / f"kappa_convergence_settings/overview_{thermo}_{setting}.nc"
    )


def setup_ax_kappa(ax, ylim=(-1, 10), xlim=30e3):
    ax.set_xlabel(None)
    ax.set_ylabel(kappa_label())
    minor_ticks_every(ax, 1000)
    major_ticks_every(ax, 1, direction="y")
    scale_labels(ax, 1000)
    ax.set_xlim(0, xlim)
    ax.set_ylim(ylim)
    # ax.legend(loc="lower right")
    # reversed_legend(ax, loc="upper center", ncols=4, frameon=True)
    ax.legend(loc="upper center", ncols=4, frameon=True)


def setup_ax_hfacf(ax, ylim=(-0.5e-3, 1.5e-3), xlim=30e3):
    ax.set_xlabel("Time in ps")
    # ax.set_ylabel(kappa_label())

    no_ticks(ax, direction="y")
    ax.set_ylabel("HFACF (arb. units)")

    minor_ticks_every(ax, 1000)
    # major_ticks_every(ax, 1, direction="y")
    scale_labels(ax, 1000)
    ax.set_xlim(0, xlim)
    ax.set_ylim(ylim)
    ax.axhline(0, color=black)
    # ax.legend(loc="lower right")


settings = {
    "m_300": {
        "converged": {
            "inset_location": [0.25, 0.05, 0.7, 0.55],
            "xlim": 40e3,
            "kappa_ylim": (0, 9.5),
            "hfacf_ylim": (-0.5e-3, 1.5e-3),
            "inset_xlim": (19e3, 21e3),
            "inset_ylim": (6.8, 7.2),
        },
        "unconverged": {
            "inset_location": [0.25, 0.05, 0.7, 0.55],
            "xlim": 20e3,
            "kappa_ylim": (0, 3.5),
            "hfacf_ylim": (-0.15e-3, 0.5e-3),
            "inset_xlim": (1.75e3, 2.75e3),
            "inset_ylim": (2.3, 2.8),
        },
    },
    "m_1400": {
        "converged": {
            "inset_location": [0.25, 0.05, 0.7, 0.55],
            "xlim": 8e3,
            "kappa_ylim": (0, 2.7),
            "hfacf_ylim": (-0.25e-3, 1.0e-3),
            "inset_xlim": (3e3, 4e3),
            "inset_ylim": (1.8, 2.1),
        },
    },
}

for thermo, other in settings.items():
    for name, s in other.items():
        data = get_data(thermo, name)

        fig, axs = plt.subplots(
            2, figsize=(0.95 * (textwidth + marginwidth), 7), sharex=True
        )

        ks = {name: isotropic(data[kk + suffix]) for name, suffix in suffixes.items()}

        ax = axs[0]
        for key, k in ks.items():
            k.plot(
                ax=ax,
                color=colors[key],
                linestyle=linestyles[key],
                label=labels[key],
                linewidth=3,
            )

        setup_ax_kappa(ax, xlim=s["xlim"], ylim=s["kappa_ylim"])

        axins = ax.inset_axes(s["inset_location"])
        for key, k in ks.items():
            k.plot(
                ax=axins,
                color=colors[key],
                linestyle=linestyles[key],
                label=labels[key],
            )

        axins.set_xlim(*s["inset_xlim"])
        axins.set_ylim(*s["inset_ylim"])
        axins.set_xlabel(None)
        axins.set_ylabel(None)
        no_ticks(axins, direction="x")
        no_ticks(axins, direction="y")
        ax.indicate_inset_zoom(axins, edgecolor=black, alpha=1, linewidth=2)

        ax = axs[1]
        hfacfs = {
            name: isotropic(data[khfacf + suffix]) for name, suffix in suffixes.items()
        }

        for key, k in hfacfs.items():
            k.plot(
                ax=ax, color=colors[key], linestyle=linestyles[key], label=labels[key]
            )
            if key == "w_filter_w_gauge" or key == "w_filter_no_gauge":
                cutoff = k.time[k < 0].min()
                ax.axvline(
                    k.time.sel(time=cutoff),
                    color=colors[key],
                    linestyle=linestyles[key],
                    linewidth=3,
                )

        setup_ax_hfacf(ax, xlim=s["xlim"], ylim=s["hfacf_ylim"])

        savefig(fig, f"noise/parts_{thermo}_{name}.png")
        savefig(fig, img / f"gk/zro_kc_noise_parts_{thermo}_{name}.pdf")
