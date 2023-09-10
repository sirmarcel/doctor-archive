from tbx import *
from tbx.vdos import *

aims = load(glp / "snse_vdos/aims.nc")
sokrates_l1 = load(glp / "snse_vdos/default_L1.nc")
sokrates_l2 = load(glp / "snse_vdos/default_L2.nc")
sokrates_l3 = load(glp / "snse_vdos/default_L3.nc")


fig, ax = fig_and_ax(figsize=(0.95 * textwidth, 3))

prominence = 18

plot_peaks(ax, aims.fourier_transform, color=black, prominence=prominence)
plot_vdos(ax, aims.fourier_transform, label="FHI-aims", color=black)

# plot_peaks(ax, sokrates_l2.fourier_transform, color=red, prominence=prominence)
plot_vdos(
    ax,
    sokrates_l1.fourier_transform,
    color=teal,
    linestyle=dashdot,
    offset=0,
    label=r"$M{=}1$",
    alpha=0.8,
)
plot_vdos(
    ax,
    sokrates_l2.fourier_transform,
    color=blue,
    linestyle=finedot,
    offset=0,
    label=r"$M{=}2$",
    alpha=0.8,
)
plot_vdos(
    ax,
    sokrates_l3.fourier_transform,
    color=red,
    linestyle=finedash,
    offset=0,
    label=r"$M{=}3$",
    alpha=0.8,
)

ax.set_xlim(0, 7)
ax.set_ylim(0, 4.5)
ax.set_ylabel("Intensity")
ax.set_xlabel("Frequency in THz")

ax.yaxis.set_major_locator(plt.NullLocator())

major_ticks_every(ax, 1)



fig.legend(loc="upper center", ncol=4, handlelength=3.5)

savefig(fig, "preview.png")
savefig(fig, img / "gk/snse_vdos.pdf")
