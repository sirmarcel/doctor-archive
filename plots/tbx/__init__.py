import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import xarray as xr
from matplotlib import pyplot as plt

from .literals import *
from .stats import *

plt.style.use("/Users/marcel/base/desk/phd/dada/dada-plot/dada.mlpstyle")

gknet = Path("/Users/marcel/base/desk/phd/projects/gknet/gknet-results/data")
gknet_train = Path("/Users/marcel/base/desk/phd/projects/gknet/gknet/experiments/")
glp = Path("/Users/marcel/base/desk/phd/projects/glp/glp-results/data")
glp_work = Path("/Users/marcel/base/desk/phd/projects/glp/glp-work/experiments")
img = Path("../../dada-tex/img/plot")
tables = Path("../../dada-tex/table")


def load(file):
    file = Path(file)
    if file.suffix == ".nc":
        return xr.open_dataset(str(file))
    elif file.suffix == ".npz":
        return np.load(file, allow_pickle=True)
    else:
        raise IOError(f"cannot open file {file}")


def savetab(tab, file):
    with open(file, "w") as f:
        f.write(tab)


def savefig(fig, file):
    fig.savefig(file, bbox_inches="tight", pad_inches=0.05)


def fig_and_ax(figsize=None):
    if figsize:
        fig = plt.figure(figsize=figsize, dpi=200)
    else:
        fig = plt.figure(figsize=(16, 10), dpi=200)
    ax = plt.axes()
    return fig, ax


def minor_ticks_every(ax, spacing, direction="x"):
    from matplotlib.ticker import MultipleLocator

    if direction == "x":
        ax.xaxis.set_minor_locator(MultipleLocator(spacing))
    else:
        ax.yaxis.set_minor_locator(MultipleLocator(spacing))


def major_ticks_every(ax, spacing, direction="x"):
    from matplotlib.ticker import MultipleLocator

    if direction == "x":
        ax.xaxis.set_major_locator(MultipleLocator(spacing))
    else:
        ax.yaxis.set_major_locator(MultipleLocator(spacing))


def scale_labels(ax, scale, direction="x"):
    from matplotlib.ticker import FuncFormatter

    ticks = FuncFormatter(lambda x, pos: "{0:g}".format(x / scale))

    if direction == "x":
        ax.xaxis.set_major_formatter(ticks)
    else:
        ax.yaxis.set_major_formatter(ticks)


def reversed_legend(ax, **kwargs):
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(reversed(handles), reversed(labels), **kwargs)


def no_ticks(ax, direction="x"):
    if direction == "x":
        ax.xaxis.set_major_locator(plt.NullLocator())
    else:
        ax.yaxis.set_major_locator(plt.NullLocator())


cm = 1 / 2.54
textwidth = 10.7 * cm * 2
textheight = 5 * cm * 2
marginwidth = 4.5 * cm * 2
marginheight = 3 * cm * 2


def round_up_to_digits(x, digits=2):
    return np.ceil(x * 10**digits) / 10**digits
