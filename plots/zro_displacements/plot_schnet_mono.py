from tbx import *

data = load(gknet / "displacements/schnet_monoclinic.nc")

fig, axs = plt.subplots(2, figsize=(0.95 * textwidth, 8), sharex=True)


colors = {
    300: black,
    600: red,
    900: orange,
    1200: teal,
    1400: blue,
}

skipped = [1400]

for temp, color in reversed(colors.items()):
    data.sel(temperature=temp).positions.plot(
        ax=axs[0], color=color, label=render_temp(temp)
    )

for temp, color in reversed(colors.items()):
    if temp in skipped:
        continue
    data.sel(temperature=temp).positions.plot(
        ax=axs[1], color=color, label=render_temp(temp)
    )


for ax in axs:
    scale_labels(ax, 1e6)
    ax.set_xlabel("Time in ns")
    ax.set_ylabel("Max. displacement in Å")
    ax.set_title(None)
    ax.set_xlim(0, 1e6)

axs[0].set_ylim(0.2, 3.9)
minor_ticks_every(axs[0], 1, direction="y")
axs[0].legend(loc="upper left", frameon=True)

axs[1].set_ylim(0.2, 1.1)
minor_ticks_every(axs[1], 0.5, direction="y")
axs[1].legend(loc="upper left", frameon=True)

savefig(fig, "preview_mono.png")
savefig(fig, img / "gk/zro_displacements_schnet_mono.pdf")
