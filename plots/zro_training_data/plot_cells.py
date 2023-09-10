from tbx import *

runs = [4, 8, 3, 7]
data = {i: load(gknet / f"training_data/{i}.nc") for i in runs}

fig, axs = plt.subplots(4, figsize=(0.83 * textwidth, 4 * textheight), sharex=True)


def plot_with_rolling_mean(ax, data, window, label, **kwargs):
    data.plot(ax=ax, alpha=0.5, label=nolabel, **kwargs)
    data.rolling(time=window, center=True).mean().plot(
        ax=ax, alpha=1.0, label=label, **kwargs
    )


def vector_norm(x, dim, ord=None):
    return xr.apply_ufunc(
        np.linalg.norm,
        x,
        input_core_dims=[[dim]],
        kwargs={"ord": ord, "axis": -1},
        dask="parallelized",
    )


def get_lattice_length(data, a):
    vector = data.cell.isel(a=a)
    return vector_norm(vector, "b")


colors = [black, red, teal]

names = {
    4: render_temp(3000),
    8: render_temp(2250),
    3: render_temp(1500),
    7: render_temp(750),
}

# direction_names = {}

for count, i_d in enumerate(data.items()):
    i, d = i_d
    for a in reversed([0, 1, 2]):
        plot_with_rolling_mean(
            axs[count],
            get_lattice_length(d, a),
            25,
            r"$|\boldsymbol{b}_{X}|$".replace("X", str(a + 1)),
            color=colors[a],
            linestyle=solid,
        )
        # plot_with_rolling_mean(
        #     axs[count],
        #     get_lattice_length(d, a).isel(time=slice(2000, 2500)),
        #     25,
        #     nolabel,
        #     color=colors[a],
        #     linestyle=dashed,
        # )


for i, ax in enumerate(axs):
    scale_labels(ax, 1000)
    ax.set_xlabel("Simulation time in ps")
    ax.set_ylabel(r"Lattice vector length in \unit{\angstrom}")

    # ax.set_xlim(0, 10e3)
    # ax.set_ylim(0, 3450)

    ax.legend(loc="upper left")
    ax.set_ylim(10.1, 10.85)

    ax.axvline(8e3, color=black)

    ax.text(6.55e3, 10.15, "Training")
    ax.text(8.2e3, 10.148, "Validation")

    ax.set_title(names[runs[i]])

savefig(fig, "preview_cell.png")
savefig(fig, img / "gk/si-zro_training_data_cells.pdf")
