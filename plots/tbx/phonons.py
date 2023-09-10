def setup(ax, ref_phonons, lim_bs=(-0.5, 10), lim_dos=(0, 15)):
    setup_bandstructure(ax[0], ref_phonons, lim=lim_bs)
    setup_dos(ax[1], lim=lim_dos)


def setup_bandstructure(ax, phonons, lim=(-0.5, 10)):
    all_distances = phonons["bs_all_distances"]
    labels = phonons["bs_labels"]

    special_points = phonons["bs_special_points"]

    ax.axhline(y=0, linestyle=":", linewidth=0.5, color="black")

    ax.xaxis.set_ticks_position("both")
    ax.yaxis.set_ticks_position("both")
    ax.xaxis.set_tick_params(which="both", direction="in")
    ax.yaxis.set_tick_params(which="both", direction="in")

    ax.set_ylabel("Frequency in THz")
    ax.set_xlabel("Wave vector")

    ax.set_xticks(special_points)
    ax.set_xticklabels(labels, rotation=35)

    ax.set_xlim(0, all_distances[-1][-1])
    ax.set_ylim(lim)


def setup_dos(ax, lim=(0, 15)):
    ax.xaxis.set_ticks_position("both")
    ax.yaxis.set_ticks_position("both")
    ax.xaxis.set_tick_params(which="both", direction="in")
    ax.yaxis.set_tick_params(which="both", direction="in")

    ax.set_xlabel("Density of states")
    # ax.set_ylabel("Frequency")

    ax.grid(True)
    ax.set_xlim(lim)


def plot(ax, phonons, **kwargs):
    plot_bandstructure(ax[0], phonons, **kwargs)
    plot_dos(ax[1], phonons, **kwargs)


def plot_bandstructure(ax, phonons, **kwargs):
    if "label" in kwargs:
        label = kwargs.pop("label")

    all_distances = phonons["bs_all_distances"]
    all_frequencies = phonons["bs_all_frequencies"]

    for i, df in enumerate(zip(all_distances, all_frequencies)):
        distances, frequencies = df
        for j, freqs in enumerate(frequencies.T):
            if i == 0 and j == 0:
                ax.plot(distances, freqs, label=label, **kwargs)
            else:
                ax.plot(distances, freqs, **kwargs)


def plot_dos(ax, phonons, **kwargs):
    if "label" in kwargs:
        label = kwargs.pop("label")
    
    frequency_points = phonons["dos_frequency_points"]
    total_dos = phonons["dos_total_dos"]

    ax.plot(total_dos, frequency_points, **kwargs)
