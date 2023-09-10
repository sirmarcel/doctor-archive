import numpy as np
from scipy.signal import find_peaks
from scipy.integrate import trapz


def plot_vdos(ax, vdos, color="black", offset=0.0, label="__nolabel__", linewidth=3, **kwargs):
    integral = trapz(np.asarray(vdos.fillna(0.0)), dx=0.01)

    vdos /= integral
    vdos *= 8

    if offset is None:
        offset = -vdos.min()

    (vdos + offset).plot(ax=ax, color=color, label=label, linewidth=linewidth, **kwargs)


def plot_peaks(ax, vdos, color="black", prominence=0.08):
    peaks, _ = find_peaks(vdos, prominence=prominence)
    for p in peaks:
        ax.axvline(vdos.omega.isel(omega=p), color=color, alpha=0.4, linewidth=1)
