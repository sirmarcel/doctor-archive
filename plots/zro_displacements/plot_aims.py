from tbx import *

data = load(gknet / "displacements/aims.nc")

fig, axs = plt.subplots(2, figsize=(0.95 * textwidth, 8), sharex=True)


colors = {
    750: black,
    1500: red,
    2250: orange,
    3000: teal,
}

skipped = [2250, 3000]

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
    scale_labels(ax, 1e3)
    ax.set_xlabel("Time in ps")
    ax.set_ylabel("Max. displacement in Å")
    ax.set_title(None)
    ax.set_xlim(0, 10e3)

    ax.axvline(8e3, color=black)


axs[0].text(6.55e3, 7.0, "Training")
axs[0].text(8.2e3, 6.99, "Validation")

axs[1].text(6.55e3, 1.5, "Training")
axs[1].text(8.2e3, 1.495, "Validation")

axs[0].set_ylim(0.1, 7.5)
# minor_ticks_every(axs[0], 1, direction="y")
axs[0].legend(loc="upper left", frameon=True)

axs[1].set_ylim(0.1, 1.6)
# minor_ticks_every(axs[1], 0.5, direction="y")
axs[1].legend(loc="upper left", frameon=True)

savefig(fig, "preview_aims.png")
savefig(fig, img / "gk/zro_displacements_aims.pdf")
