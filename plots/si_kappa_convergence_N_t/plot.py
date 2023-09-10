from tbx import *

data = xr.open_dataset(glp / "si_kappa_convergence_N_t/production_1_l2_cu5.0_ef_1_400.nc")


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

    ax.axhline(k.data, color=kwargs.get("color", black))

    if highlight:
        ax.fill_between(
            [0, 50], [k - e] * 2, [k + e] * 2, alpha=0.35, color=kwargs["color"]
        )


struggle = (4096, 10_000_000)

fig, ax = fig_and_ax(figsize=(0.95 * textwidth, 4))

ns = data.n_atoms.data
ls = ns ** (1 / 3)
maxstepss = data.maxsteps.data[1::2]

distance = 0.1  # distance between labels
start = ((len(maxstepss) - 1) * distance) / 2

for i_n, n in enumerate(ns):
    base_position = ls[i_n]

    d = data.sel(n_atoms=n).sel(maxsteps=maxstepss)
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
    (struggle),
    highlight=True,
    color=red,
    marker=star,
    markersize=11,
    label="Production",
)

ax.set_xticks(ls)
ax.set_xticklabels(list(map(str, ns)))
ax.set_xlabel("Number of atoms ($N^{1/3}$) (offset for simulation time)")
ax.set_xlim(6.0, 18.5)


ax.set_ylabel(kappa_label())
ax.set_ylim(30, 65)

minor_ticks_every(ax, 1, direction="y")

# ax.legend(loc="lower right", ncol=2)
# ax.set_title(render_temp(temp))

# plt.subplots_adjust(hspace=0.40)
savefig(fig, "preview.png")
savefig(fig, img / "gk/si_kappa_convergence_N_t.pdf")
