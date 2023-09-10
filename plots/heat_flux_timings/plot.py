from tbx import *

from scipy.optimize import curve_fit


develop = False

# otherwise things are very slow
if develop:
    import matplotlib as mpl

    mpl.rcParams["text.usetex"] = False


def fit_func(x, d, c):
    return d * x + c


def fit_curve(x, y, sigma=None):
    lx = np.log10(x)
    ly = np.log10(y)

    if sigma is None:
        popt, pcov = curve_fit(fit_func, lx, ly, p0=[2.0, 50.0])
    else:
        popt, pcov = curve_fit(fit_func, lx, ly, p0=[2.0, 50.0], sigma=sigma)

    return (
        x,
        10 ** fit_func(lx, *popt),
        popt,
        lambda x: 10 ** fit_func(np.log10(x), *popt),
    )


def fit(data, key, start=0):
    end = len(data.n_atoms)
    curve_y = data[key].mean(dim="trials").isel(n_atoms=slice(start, end)).data

    return fit_curve(data.isel(n_atoms=slice(start, end)).n_atoms.data, curve_y)


data_n1 = load(gknet / "heat_flux_timings/zro_schnet_n1.nc")
data_n2 = load(gknet / "heat_flux_timings/zro_schnet_n2.nc")

names = {
    "hardy": render_j(upper="mic"),
    "unfolded": render_j(upper="unfolded"),
    "virials": render_j(upper="edges"),
}



def plot(ax, data, key, color, linestyle=solid, label="", marker=bigdot, above=True):
    plot_x, plot_y, params, f = fit(data, key, start=3)

    if color == black:
        l = r"Fit $\propto N^x$" + label
    else:
        l = nolabel

    ax.plot(plot_x, plot_y, color=color, linestyle=linestyle, alpha=0.8, label=l)

    mean = data[key].mean(dim="trials")
    err = data[key].std(dim="trials")

    if color == black:
        l = "Data" + label
    else:
        l = nolabel

    ax.scatter(
        data.n_atoms,
        mean,
        # yerr=err,
        color=color,
        # linestyle="none",
        marker=marker,
        label=l,
    )

    name = names[key]

    if above:
        text_x = -40
        text_y = 15
        show_at = 2000
    else:
        show_at = 3000
        text_x = 15
        text_y = -15

    ax.annotate(
        r"name $\propto N^{X}$".replace("X", f"{params[0]:.1f}").replace("name", name),
        xy=(show_at, f(show_at)),
        xycoords="data",
        xytext=(text_x, text_y),
        textcoords="offset points",
        arrowprops=dict(arrowstyle="-"),
    )

    show_at = 0

    if above:
        y = plot_y[show_at] * 1.75
    else:
        y = plot_y[show_at] * 0.3

    # ax.text(
    #     plot_x[show_at],
    #     y,
    #     r"name, $\propto N^{X}$".replace("X", f"{params[0]:.1f}").replace("name", name),
    #     fontsize="large",
    #     rotation=label_rotations[key],  # can't get an automatic approach to work
    #     # rotation=angle*2.303,
    #     # transform_rotates_text=True,
    #     # rotation_mode="anchor"
    # )


fig, ax = fig_and_ax(figsize=(0.95 * textwidth, textheight))

plot(ax, data_n1, "unfolded", red, linestyle=dotted, marker=star, above=False)
plot(ax, data_n1, "virials", teal, linestyle=dotted, marker=star, above=False)
plot(
    ax,
    data_n1,
    "hardy",
    black,
    linestyle=dotted,
    label=r" ($M{=}1$)",
    marker=star,
    above=False,
)

plot(ax, data_n2, "unfolded", red, above=True)
plot(ax, data_n2, "hardy", black, label=r" ($M{=}2$)", above=True)

ax.set_yscale("log", base=10)
ax.set_xscale("log", base=10)
ax.set_ylim(5e-3, 9e2)

reversed_legend(ax, loc="upper left", markerfirst=False)

ax.set_xlabel("Number of atoms in simulation cell ($N$)")
ax.set_ylabel("Time in s")

ax.set_xticks(data_n1.n_atoms.data)
ax.set_xticklabels(list(map(str, data_n1.n_atoms.data)))
ax.set_xticks([], minor=True)

# disable the labelled (!!) minor ticks
from matplotlib.ticker import LogLocator

ax.xaxis.set_minor_locator(LogLocator(10, [0]))

savefig(fig, f"preview.png")
savefig(fig, img / "gk/zro_heat_flux_timings.pdf")
