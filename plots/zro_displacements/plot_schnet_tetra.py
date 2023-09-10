from tbx import *

data = load(gknet / "displacements/schnet_tetragonal.nc")

fig, axs = plt.subplots(2, figsize=(0.95 * textwidth, 8), sharex=True)


colors = {
    1400: black,
    1500: red,
    1650: orange,
    1800: teal,
}

skipped = [1650, 1800]

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

axs[0].set_ylim(0.5, 9)
minor_ticks_every(axs[0], 1, direction="y")
axs[0].legend(loc="upper left", frameon=True)

axs[1].set_ylim(0.75, 1.65)
minor_ticks_every(axs[1], 0.5, direction="y")
axs[1].legend(loc="upper left", frameon=True)

savefig(fig, "preview_tetra.png")
savefig(fig, img / "gk/zro_displacements_schnet_tetra.pdf")
