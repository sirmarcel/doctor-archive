from tbx import *

develop = False

# otherwise things are very slow
if develop:
    import matplotlib as mpl

    mpl.rcParams["text.usetex"] = False


data = load(gknet / "test_set_errors/nomad.nc").forces * 1e3

fig, ax = fig_and_ax(figsize=(textwidth * 0.95, 4.0))

ts = [1, 2, 3]
width = 0.03
offset = 0.04
start = ((len(ts) - 1) * width + (len(ts) - 1) * offset) / 2

colors = [orange, red, teal, orange]
markers = [thiamond, diamond, square, bigdot]

for i, t in enumerate(ts):
    bp = ax.boxplot(
        data.sel(t=t).T,
        positions=data.cutoff - start + i * (width + offset),
        widths=width,
        whis=1e6,
        #         meanline=True,
        showmeans=False,
        manage_ticks=False,
        # medianprops={
        #     "marker": markers[i],
        #     "markeredgecolor": black,
        #     "markerfacecolor": colors[i],
        #     "markersize": 8,
        #     "label": f"$T={t}$",
        # },
        # notch=False,
    )

    for element in ["boxes", "whiskers", "fliers", "medians", "caps"]:
        plt.setp(bp[element], color="black", alpha=0.6)

    plt.setp(bp["medians"], alpha=1.0)

    ax.plot(
        data.cutoff - start + i * (width + offset),
        data.sel(t=t).mean(dim="sample"),
        marker=markers[i],
        markerfacecolor=colors[i],
        label=r"$M{=}X$".replace("X", str(t)),
        alpha=1.0,
        markeredgecolor=black,
        lw=0,
        markersize=10,
    )


ax.legend(loc="upper right", ncol=3)

ax.set_xlabel(f"Cutoff radius in Å (offset for visibility)")
ax.set_ylabel("AE Forces in meV/Å")

y_std = 1.3708777 * 1000
secax = ax.twinx()
secax.set_ylim(
    (
        100.0 * ax.get_ylim()[0] / y_std,
        100.0 * ax.get_ylim()[1] / y_std,
    )
)
if develop:
    secax.set_ylabel("Relative AE Forces in %")
else:
    secax.set_ylabel(r"Relative AE Forces in \si{\percent}")

ax.set_xticks(data.cutoff)

ax.set_ylim(25, 425)

savefig(fig, "preview.png")
savefig(fig, img / f"gk/zro_test_set_errors.pdf")
