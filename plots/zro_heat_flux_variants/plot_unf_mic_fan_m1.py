from tbx import *
from tbx.gk import *


def get_data(thermo):
    return load(
        gknet / f"kappa_convergence_settings/hfs_m1_{thermo}.nc"
    )


def delta_kappa(value):
    k = render_kappa(value, develop=False)
    return r"$\sim$ X".replace("X", k)



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


def plot_difference(ax, a, b):
    cu_a, ke_a = plot_cutoff(ax, a, cutoff=False, kappa=False)
    cu_b, ke_b = plot_cutoff(ax, b, cutoff=False, kappa=False)

    # print(a.time)
    loc = cu_a
    k_a = ke_a[0]
    k_b = ke_b[0]

    lower = min(k_a, k_b)
    upper = max(k_a, k_b)
    padding = max(0.03 * upper, 0.08)
    diff = np.abs(k_b - k_a)
    percentage = (diff / upper) * 100
    print(f"Difference in %: {percentage:.0f}")

    ax.plot([loc, loc], [lower + padding, upper - padding], color=black, linewidth=1)
    ax.text(loc * 1.05, 0.5 * (k_a + k_b) - 0.1, delta_kappa(np.abs(k_b - k_a)))


settings = {
    "m_300": {
        "xlim": 40e3,
        "ylim": (0, 8.2),
    },
    # "m_600": {
    #     "xlim": 40e3,
    #     "ylim": (0, 4.4),
    # },
    # "t_1400": {
    #     "xlim": 8e3,
    #     "ylim": (0, 2.2),
    # },
    # "m_1400": {
    #     "xlim": 8e3,
    #     "ylim": (0, 2.2),
    # },
}

# jfan_mpnn
# jfan
# jhardy
# junf

js = ["jhardy", "junf", "jfan"]
labels = {
    "jfan_mpnn": render_j(upper="semi-local"),
    "jfan": render_j(upper="local"),
    "jhardy": render_j(upper="mic"),
    "junf": render_j(upper="unfolded"),
}

styles = {
    "jhardy": {"color": red, "linestyle": solid, "linewidth": 2},
    "junf": {"color": black, "linestyle": (0, (1, 3.5)), "linewidth": 6},
    "jfan": {"color": teal, "linestyle": dotted, "linewidth": 2},
    "jfan_mpnn": {"color": orange, "linestyle": (0, (0.25, 2.25)), "linewidth": 4},
}


for thermo, s in settings.items():
    data = get_data(thermo)

    fig, ax = fig_and_ax(figsize=(0.95 * textwidth, 3.5))

    kappas = {j: data.sel(heat_flux=j) for j in js}

    for j, kappa in kappas.items():
        plot_mean_kappa(ax, kappa, key=kkf, label=labels[j], alpha_err=0.1, total=True, **styles[j])

    # plot_difference(ax, kappas["junf"], kappas["jfan"])

    setup_ax(ax, **s)
    ax.legend(loc="lower right", handlelength=5)

    savefig(fig, f"mic/unf_mic_fan_m1_{thermo}.png")
    savefig(fig, img / f"gk/zro_hfs_unf_mic_fan_m1_{thermo}.pdf")
