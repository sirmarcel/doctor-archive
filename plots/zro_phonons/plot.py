from tbx import *
from tbx.phonons import *

develop = False

# otherwise things are very slow
if develop:
    import matplotlib as mpl

    mpl.rcParams["text.usetex"] = False


def name(cutoff, t):
    if not develop:
        return r"$T=Y$, $r_{\text{c}}=\SI{X}{\angstrom}$".replace(
            "X", f"{cutoff:.1f}"
        ).replace("Y", str(t))
    else:
        return f"$T = {t}$, $r_c = {cutoff:.1f}$Å"


datadir = gknet / "verdi_phonons"


for n in [96, 324]:
    aims = load(datadir / f"tetra_aims_n{n}.npz")
    schnet = load(datadir / f"tetra_schnet_n{n}.npz")

    fig, ax = plt.subplots(
        nrows=1,
        ncols=2,
        gridspec_kw={"width_ratios": [3, 1]},
        sharey=True,
        figsize=(textwidth * 0.95, 4),
        dpi=200,
    )

    ax1, ax2 = ax
    setup(ax, aims, lim_bs=(-2, 25), lim_dos=(0, 4))
    plot(ax, aims, color=black, linestyle=solid, label="FHI-aims")
    plot(ax, schnet, color=red, linestyle=solid, label="SchNet")
    fig.legend(loc="upper center", ncol=3)

    savefig(fig, f"preview_tetra_{n}_5.0_n2.png")

    aims = load(datadir / f"mono_aims_n{n}.npz")
    schnet = load(datadir / f"mono_schnet_n{n}.npz")

    fig, ax = plt.subplots(
        nrows=1,
        ncols=2,
        gridspec_kw={"width_ratios": [3, 1]},
        sharey=True,
        figsize=(textwidth * 0.95, 3.5),
        dpi=200,
    )

    ax1, ax2 = ax
    setup(ax, aims, lim_bs=(-2, 25), lim_dos=(0, 4))
    plot(ax, aims, color=black, linestyle=solid, label="FHI-aims")
    plot(ax, schnet, color=red, linestyle=solid, label="SchNet")
    fig.legend(loc="upper center", ncol=3)

    savefig(fig, f"preview_mono_{n}_5.0_n2.png")

n = 324

for cutoff in [4.0, 5.0, 6.0]:
    for t in [1, 2]:
        if cutoff == 5.0 and t == 2:
            continue

        aims = load(datadir / f"tetra_aims_n{n}.npz")
        schnet = load(datadir / f"tetra_schnet_{cutoff:.1f}_n{t}_n{n}.npz")

        fig, ax = plt.subplots(
            nrows=1,
            ncols=2,
            gridspec_kw={"width_ratios": [3, 1]},
            sharey=True,
            figsize=(textwidth * 0.95, 3.5),
            dpi=200,
        )

        ax1, ax2 = ax
        setup(ax, aims, lim_bs=(-2, 25), lim_dos=(0, 4))
        plot(ax, aims, color=black, linestyle=solid, label="FHI-aims")
        plot(ax, schnet, color=red, linestyle=solid, label="SchNet")
        fig.legend(loc="upper center", ncol=3)

        savefig(fig, f"preview_tetra_{n}_{cutoff:.1f}_n{t}.png")
        savefig(fig, img / f"gk/si-zro_phonons_tetra_{n}_{cutoff:.1f}_n{t}.pdf")

        aims = load(datadir / f"mono_aims_n{n}.npz")
        schnet = load(datadir / f"mono_schnet_{cutoff:.1f}_n{t}_n{n}.npz")

        fig, ax = plt.subplots(
            nrows=1,
            ncols=2,
            gridspec_kw={"width_ratios": [3, 1]},
            sharey=True,
            figsize=(textwidth * 0.95, 3.5),
            dpi=200,
        )

        ax1, ax2 = ax
        setup(ax, aims, lim_bs=(-2, 25), lim_dos=(0, 4))
        plot(ax, aims, color=black, linestyle=solid, label="FHI-aims")
        plot(ax, schnet, color=red, linestyle=solid, label="SchNet")
        fig.legend(loc="upper center", ncol=3)

        savefig(fig, f"preview_mono_{n}_{cutoff:.1f}_n{t}.png")
        savefig(fig, img / f"gk/si-zro_phonons_mono_{n}_{cutoff:.1f}_n{t}.pdf")


aims = load(datadir / f"tetra_aims_n{n}.npz")
schnet = load(datadir / f"tetra_schnet_n{n}.npz")

fig, ax = plt.subplots(
    nrows=1,
    ncols=2,
    gridspec_kw={"width_ratios": [3, 1]},
    sharey=True,
    figsize=(textwidth * 0.95, 3.5),
    dpi=200,
)


ax1, ax2 = ax
setup(ax, aims, lim_bs=(-2, 25), lim_dos=(0, 4))
plot(ax, aims, color=black, linestyle=solid, label="FHI-aims")
plot(ax, schnet, color=red, linestyle=solid, label="SchNet")
fig.legend(loc="upper center", ncol=3)

savefig(fig, img / "gk/zro_phonons_tetra.pdf")


aims = load(datadir / f"mono_aims_n{n}.npz")
schnet = load(datadir / f"mono_schnet_n{n}.npz")

fig, ax = plt.subplots(
    nrows=1,
    ncols=2,
    gridspec_kw={"width_ratios": [3, 1]},
    sharey=True,
    figsize=(textwidth * 0.95, 3.5),
    dpi=200,
)


ax1, ax2 = ax
setup(ax, aims, lim_bs=(-2, 25), lim_dos=(0, 4))
plot(ax, aims, color=black, linestyle=solid, label="FHI-aims")
plot(ax, schnet, color=red, linestyle=solid, label="SchNet")
fig.legend(loc="upper center", ncol=3)

savefig(fig, img / "gk/zro_phonons_mono.pdf")
