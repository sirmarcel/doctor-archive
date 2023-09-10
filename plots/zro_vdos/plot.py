from tbx import *
from scipy.signal import find_peaks
from scipy.integrate import trapz
from itertools import cycle

develop = False

# otherwise things are very slow
if develop:
    import matplotlib as mpl

    mpl.rcParams["text.usetex"] = False


def rc(cutoff):
    if not develop:
        return r"$r_{\text{c}}=\SI{X}{\angstrom}$".replace("X", f"{cutoff:.1f}")
    else:
        return f"$r_c = {cutoff:.1f}$Å"


data = load(gknet / "vdos/result_300.nc")


def plot_vdos(ax, vdos, color=black, offset=0.0, label="__nolabel__"):
    integral = trapz(np.asarray(vdos.mean(dim="trajectory").fillna(0.0)), dx=0.01)

    vdos /= integral
    vdos *= 8
    mean = vdos.mean(dim="trajectory")
    mx = vdos.max(dim="trajectory")
    mi = vdos.min(dim="trajectory")

    (mean + offset).plot(ax=ax, color=color, label=label, linewidth=3)
    ax.fill_between(mean.omega, mi + offset, mx + offset, color=color, alpha=0.2)

    ax.text(24.2, offset + 0.18, label, fontsize="medium")


def plot_peaks(ax, vdos, color=black, prominence=0.08):
    peaks, _ = find_peaks(vdos, prominence=prominence)
    for p in peaks:
        ax.axvline(vdos.omega.isel(omega=p), color=color, alpha=0.4, linewidth=1)


for t in [1, 2]:
    fig, ax = fig_and_ax(figsize=(textwidth, 4))

    if t == 1:
        prominence = 5
    else:
        prominence = 0.08

    plot_peaks(
        ax, data["aims"].mean(dim="trajectory"), color=teal, prominence=prominence
    )
    plot_vdos(ax, data["aims"], label="FHI-aims", color=teal)

    # colors = cycle(tol_vibrant[1:])
    for i, cutoff in reversed(list(enumerate(np.arange(4.5, 6.51, 0.5)))):
        name = f"cu{cutoff:.1f}_n{t}"
        if cutoff == 5.0:
            color = red
        else:
            color = black

        plot_vdos(ax, data[name], color=color, offset=0.8 * (i + 1), label=rc(cutoff))

    ax.set_xlim(0, 29)
    ax.set_ylabel("Intensity (offset for visibility)")
    ax.set_xlabel("Frequency in THz")

    ax.yaxis.set_major_locator(plt.NullLocator())
    minor_ticks_every(ax, 1)
    savefig(fig, f"preview_t{t}.png")
    savefig(fig, img / f"gk/zro_vdos_t{t}.pdf")
