from tbx import *
from tbx.gk import *


kkt = kk + "_total"
kkft = kkf + "_total"
kkmt = kkm + "_total"
kkfmt = kkfm + "_total"
kkfst = kkfs + "_total"

setting_to_name = {
    "converged": r"($1500,\qty{1}{ns})$ \textit{Prod.}",
    # "converged": r"Production",
    "converged_short": r"($1500,\qty{0.1}{ns})$",
    "semi": r"($768,\qty{0.5}{ns})$ \textit{Light}",
    "unconverged": r"($96,\qty{0.1}{ns})$ \textit{Unconv.}",
    "unconverged_long": r"($96,\qty{1}{ns})$",
    "ultra": r"($4116,\qty{2}{ns})$ \textit{Tight}",
}

# setting_to_name = {
#     "unconverged": "A",
#     "unconverged_long": "A+",
#     "semi": "B",
#     "converged": "C",
#     "converged_short": "C-",
#     "ultra": "D",
# }


def get_data(thermo, setting):
    return load(
        gknet / f"kappa_convergence_settings/overview_{thermo}_{setting}.nc"
    )


def plot_vs_total(ax, thermo, setting, linestyle, color):
    label = setting_to_name[setting]
    data = get_data(thermo, setting)
    isotropic(data[kkmt]).plot(
        ax=ax, linestyle=linestyle, color=color, alpha=0.5, label=nolabel
    )
    isotropic(data[kkfm]).plot(
        ax=ax, linestyle=linestyle, color=color, alpha=1.0, label=label
    )


def plot(ax, thermo, skip_ultra=False):
    plot_vs_total(ax, thermo, "converged", solid, red)
    if not skip_ultra:
        plot_vs_total(ax, thermo, "ultra", solid, blue)
    plot_vs_total(ax, thermo, "semi", dashdot, teal)
    plot_vs_total(ax, thermo, "converged_short", loosedot, cyan)
    plot_vs_total(ax, thermo, "unconverged_long", finedash, magenta)
    plot_vs_total(ax, thermo, "unconverged", dotted, orange)


def setup_ax(ax, ylim=(-1, 10), xlim=30e3):
    ax.set_xlabel("Integration time in ps")
    ax.set_ylabel(kappa_label())
    minor_ticks_every(ax, 1000)
    scale_labels(ax, 1000)
    ax.set_xlim(0, xlim)
    ax.set_ylim(ylim)
    ax.legend(loc="lower left", frameon=True, ncols=3, handlelength=1.5)


thermo = "m_300"
fig, ax = fig_and_ax(figsize=(0.95 * textwidth, 4))
plot(ax, thermo)
setup_ax(ax, ylim=(-1, 9.6), xlim=40e3)
savefig(fig, f"overview/preview_{thermo}.png")
savefig(fig, img / f"gk/zro_kc_overview_{thermo}.pdf")


thermo = "m_600"
fig, ax = fig_and_ax(figsize=(0.95 * textwidth, 4))
plot(ax, thermo)
setup_ax(ax, ylim=(-1, 4.5), xlim=30e3)
savefig(fig, f"overview/preview_{thermo}.png")
savefig(fig, img / f"gk/zro_kc_overview_{thermo}.pdf")

thermo = "m_1400"
fig, ax = fig_and_ax(figsize=(0.95 * textwidth, 4))
plot(ax, thermo)
setup_ax(ax, ylim=(0, 2.75), xlim=8e3)
savefig(fig, f"overview/preview_{thermo}.png")
savefig(fig, img / f"gk/zro_kc_overview_{thermo}.pdf")

thermo = "t_1400"
fig, ax = fig_and_ax(figsize=(0.95 * textwidth, 4))
plot(ax, thermo, skip_ultra=False)
setup_ax(ax, ylim=(0, 2.75), xlim=8e3)
savefig(fig, f"overview/preview_{thermo}.png")
savefig(fig, img / f"gk/zro_kc_overview_{thermo}.pdf")
