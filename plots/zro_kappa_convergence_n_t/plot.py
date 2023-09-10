from tbx import *
from tbx.gk import *


def get_data(thermo):
    return load(gknet / f"kappa_convergence_N_t/{thermo}.nc")


settings = {
    "m_300": {"ylim": (2, 8.4)},
    "m_600": {"ylim": (1.0, 4.5)},
    "m_1400": {"ylim": (1.0, 2.5)},
    "t_1400": {"ylim": (1.0, 2.5)},
}

production = (1500, 250000)
semi = (768, 125000)
unconverged = (96, 25000)
ultra = (4116, 500000)


def show_single_point(ax, data, choice, highlight=False, **kwargs):
    n, m = choice
    d = data.sel(n_atoms=n, maxsteps=m)
    k = d.kappa_mean
    e = d.kappa_stderr

    base_position = ls[list(ns).index(n)]
    position = base_position - start + distance * list(maxstepss).index(m)
    _, _, bars = ax.errorbar(
        position,
        [k.data],
        linewidth=0,
        markeredgecolor=black,
        **kwargs,
    )
    if highlight:
        ax.fill_between(
            [0, 50], [k - e] * 2, [k + e] * 2, alpha=0.35, color=kwargs["color"]
        )


for thermo, s in settings.items():
    data = get_data(thermo)

    ns = data.n_atoms.data
    ls = ns ** (1 / 3)
    maxstepss = data.maxsteps.data

    distance = 0.1  # distance between labels
    start = ((len(maxstepss) - 1) * distance) / 2

    fig, ax = fig_and_ax(figsize=(0.95 * (textwidth + marginwidth), 4))

    for i_n, n in enumerate(ns):
        base_position = ls[i_n]

        d = data.sel(n_atoms=n)
        k = d.kappa_mean
        e = d.kappa_stderr

        _, _, bars = ax.errorbar(
            (base_position - start) + distance * np.arange(len(maxstepss)),
            k.data,
            yerr=e.data,
            color=black,
            elinewidth=2.0,
            linewidth=3,
            label=nolabel,
        )

        for bar in bars:
            bar.set_alpha(0.4)

    show_single_point(
        ax,
        data,
        production,
        highlight=True,
        color=red,
        marker=bigdot,
        markersize=11,
        label="Production",
    )
    show_single_point(
        ax,
        data,
        semi,
        highlight=False,
        color=teal,
        marker=thiamond,
        markersize=11,
        label="Light",
    )
    show_single_point(
        ax,
        data,
        unconverged,
        highlight=False,
        color=orange,
        marker=star,
        markersize=14,
        label="Unconverged",
    )
    show_single_point(
        ax,
        data,
        ultra,
        highlight=False,
        color=blue,
        marker=plus,
        markersize=14,
        label="Tight",
    )

    ax.set_xticks(ls)
    ax.set_xticklabels(list(map(str, ns)))
    ax.set_xlabel("Number of atoms ($N^{1/3}$) (offset for simulation time $t$)")
    ax.set_xlim(3.0, 17.5)

    ax.set_ylabel(kappa_label())
    ax.set_ylim(s["ylim"])

    ax.legend(loc="lower right", ncols=2)

    savefig(fig, f"{thermo}.png")
    savefig(fig, img / f"gk/zro_kc_nt_{thermo}.pdf")
