from tbx import *

data = {i: load(gknet / f"training_data/{i}.nc") for i in [4, 3, 8, 7]}

fig, ax = fig_and_ax(figsize=(0.95 * marginwidth, 1.5 * marginheight))


def plot_with_rolling_mean(ax, data, window, label, **kwargs):
    data.plot(ax=ax, alpha=0.5, label=nolabel, **kwargs)
    data.rolling(time=window, center=True).mean().plot(
        ax=ax, alpha=1.0, label=label, **kwargs
    )


for count, i_d in enumerate(data.items()):
    i, d = i_d

    if count == 0:
        plot_with_rolling_mean(
            ax, d.temperature.isel(time=slice(0, 2000)), 25, "Train", color=black
        )
        plot_with_rolling_mean(
            ax, d.temperature.isel(time=slice(2000, 2500)), 25, "Validation", color=red
        )
    else:
        plot_with_rolling_mean(
            ax, d.temperature.isel(time=slice(0, 2000)), 25, nolabel, color=black
        )
        plot_with_rolling_mean(
            ax, d.temperature.isel(time=slice(2000, 2500)), 25, nolabel, color=red
        )

scale_labels(ax, 1000)

ax.set_xlabel("Simulation time in ps")
ax.set_ylabel("Temperature in K")

ax.set_xlim(0, 10e3)
ax.set_ylim(0, 3450)

ax.legend(loc="upper left")

savefig(fig, "preview.png")
savefig(fig, img / "gk/zro_training_data.pdf")
