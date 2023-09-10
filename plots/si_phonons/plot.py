from tbx import *
from tbx.phonons import *

datadir = glp / "si_phonons"


n = 216

aims = load(datadir / f"aims_{n}.npz")
sokrates_l1 = load(datadir / f"production_1_l1_cu5.0_ef_1.npz")
sokrates_l2 = load(datadir / f"production_1_l2_cu5.0_ef_1.npz")
sokrates_l3 = load(datadir / f"production_1_l3_cu5.0_ef_1.npz")

fig, ax = plt.subplots(
    nrows=1,
    ncols=2,
    gridspec_kw={"width_ratios": [3, 1]},
    sharey=True,
    figsize=(0.95 * textwidth, textheight),
    dpi=200,
)
# fig, ax = fig_and_ax(figsize=(0.7 * textwidth, textheight))

setup(ax, aims, lim_dos=(-0.1, 3), lim_bs=(0, 16))
plot(ax, aims, color=black, linestyle=solid, label="FHI-aims")
plot(
    ax,
    sokrates_l1,
    color=teal,
    linestyle=dashdot,
    label=r"$M{=}1$",
    alpha=0.75,
    linewidth=2,
)
plot(
    ax,
    sokrates_l2,
    color=blue,
    linestyle=finedot,
    label=r"$M{=}2$",
    alpha=0.75,
    linewidth=2,
)
plot(
    ax,
    sokrates_l3,
    color=red,
    linestyle=finedash,
    label=r"$M{=}3$",
    alpha=0.75,
    linewidth=2,
)


for label in ax[0].get_xticklabels():
    if "|" in label.get_text():
        label.set_rotation(90)
    else:
        label.set_rotation(0)


fig.legend(loc="upper center", ncol=4, handlelength=3.5)

savefig(fig, "preview.png")
savefig(fig, img / "gk/si_phonons.pdf")
