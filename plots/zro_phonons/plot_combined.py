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


datadir = gknet / "phonons"

styles = {
    4.0: {"color": teal, "linestyle": dashdot},
    5.0: {"color": blue, "linestyle": finedot},
    6.0: {"color": red, "linestyle": finedash},
}

n = 324
for t in [1, 2]:
    aims_tetra = load(datadir / f"tetra_aims_n{n}.npz")
    aims_mono = load(datadir / f"mono_aims_n{n}.npz")

    fig_tetra, ax_tetra = plt.subplots(
        nrows=1,
        ncols=2,
        gridspec_kw={"width_ratios": [3, 1]},
        sharey=True,
        figsize=(textwidth * 0.95, 3.5),
        dpi=200,
    )
    setup(ax_tetra, aims_tetra, lim_bs=(-2, 25), lim_dos=(0, 4))
    plot(ax_tetra, aims_tetra, color=black, linestyle=solid, label="FHI-aims")
    

    fig_mono, ax_mono = plt.subplots(
        nrows=1,
        ncols=2,
        gridspec_kw={"width_ratios": [3, 1]},
        sharey=True,
        figsize=(textwidth * 0.95, 3.5),
        dpi=200,
    )

    setup(ax_mono, aims_mono, lim_bs=(-2, 25), lim_dos=(0, 4))
    plot(ax_mono, aims_mono, color=black, linestyle=solid, label="FHI-aims")
    

    for cutoff in [4.0, 5.0, 6.0]:
        schnet_tetra = load(datadir / f"tetra_schnet_{cutoff:.1f}_n{t}_n{n}.npz")
        schnet_mono = load(datadir / f"mono_schnet_{cutoff:.1f}_n{t}_n{n}.npz")

        plot(
            ax_tetra,
            schnet_tetra,
            label=r"$r_\text{c}=" + f"{cutoff:.0f}$Å",
            alpha=0.6,
            **styles[cutoff]
        )
        plot(
            ax_mono,
            schnet_mono,
            label=r"$r_\text{c}=" + f"{cutoff:.0f}$Å",
            alpha=0.6,
            **styles[cutoff]
        )

    fig_tetra.legend(loc="upper center", ncol=4)
    fig_mono.legend(loc="upper center", ncol=4)

    savefig(fig_tetra, f"preview_combined_m{t}_tetra.png")
    savefig(fig_mono, f"preview_combined_m{t}_mono.png")
    
    savefig(fig_mono, img / f"gk/si-zro_phonons_mono_m{t}.pdf")
    savefig(fig_tetra, img / f"gk/si-zro_phonons_tetra_m{t}.pdf")
