from tbx import *
from tbx.gk import *


def get_data_mic(thermo):
    return load(gknet / f"kappa_convergence_settings/hfs_mic_{thermo}.nc")


def get_data_edges(thermo):
    return load(
        gknet / f"kappa_convergence_settings/hfs_edges_{thermo}_semi.nc"
    )


def get_data_m1(thermo):
    return load(gknet / f"kappa_convergence_settings/hfs_m1_{thermo}.nc")


def setup_ax(ax, ylim=(0, 10), xlim=30e3):
    minor_ticks_every(ax, 1000)
    scale_labels(ax, 1000)
    ax.set_xlabel("Integration time in ps")
    ax.set_xlim(0, xlim)

    major_ticks_every(ax, 1, direction="y")

    if ylim[1] >= 5:
        minor_ticks_every(ax, 0.5, direction="y")
    else:
        minor_ticks_every(ax, 0.1, direction="y")

    ax.set_ylabel(kappa_label())
    ax.set_ylim(ylim)

    ax.set_title(None)


settings = {
    "m_300": {
        "xlim": 40e3,
        "ylim": (0, 8.2),
    },
    "m_600": {
        "xlim": 40e3,
        "ylim": (0, 4.4),
    },
    # "t_1400": {
    #     "xlim": 8e3,
    #     "ylim": (0, 2.2),
    # },
    # "m_1400": {
    #     "xlim": 8e3,
    #     "ylim": (0, 2.2),
    # },
}

# jfan_mpnn
# jfan
# jhardy
# junf

js = ["jhardy", "jfan_mpnn", "junf", "jfan", "jedges"]
labels = {
    "jfan_mpnn": render_j(upper="semi-local"),
    "jfan": render_j(upper="local"),
    "jhardy": render_j(upper="mic"),
    "junf": render_j(upper="unfolded"),
    "jedges": render_j(upper="edges"),
}

styles = {
    "jhardy": {"color": red, "linestyle": solid, "linewidth": 2},
    "junf": {"color": black, "linestyle": dotted, "linewidth": 2},
    "jfan": {"color": teal, "linestyle": dotted, "linewidth": 2},
    "jedges": {"color": cyan, "linestyle": dashed, "linewidth": 2},
}

thermo = "m_300"
s = settings[thermo]


data = get_data_m1(thermo)

fig, ax = fig_and_ax(figsize=(0.55 * textwidth, 4))

kappas = {j: data.sel(heat_flux=j) for j in js}

for j, kappa in kappas.items():
    if j == "jhardy":
        plot_mean_kappa(ax, kappa, key=kkf, label=labels[j], alpha_err=0.1, total=False, **styles[j])

setup_ax(ax, **s)
ax.legend(loc="lower right", handlelength=5, ncols=3)

savefig(fig, f"present_dada/m1_hardy.pdf")

fig, ax = fig_and_ax(figsize=(0.55 * textwidth, 4))
for j, kappa in kappas.items():
    if j in ["jhardy", "jedges"]:
        plot_mean_kappa(ax, kappa, key=kkf, label=labels[j], alpha_err=0.1, total=False, **styles[j])

setup_ax(ax, **s)
ax.legend(loc="lower right", handlelength=5, ncols=3)

savefig(fig, f"present_dada/m1_hardy_and_edges.pdf")

# savefig(fig, img / f"gk/zro_hfs_all_{thermo}.pdf")


data = get_data_mic(thermo)

kappas = {j: data.sel(heat_flux=j) for j in ["jhardy", "jfan_mpnn", "junf", "jfan"]}
kappas["jedges"] = get_data_edges(thermo).sel(heat_flux="jedges")

fig, ax = fig_and_ax(figsize=(0.55 * textwidth, 4))
for j, kappa in kappas.items():
    if j in ["jhardy", "jedges", "jfan"]:
        plot_mean_kappa(ax, kappa, key=kkf, label=labels[j], alpha_err=0.1, total=True, **styles[j])


setup_ax(ax, **s)
ax.legend(loc="lower right", handlelength=5, ncols=2)

savefig(fig, f"present_dada/hardy_edges_local.pdf")


fig, ax = fig_and_ax(figsize=(0.55 * textwidth, 4))
for j, kappa in kappas.items():
    if j in ["jhardy", "jedges"]:
        plot_mean_kappa(ax, kappa, key=kkf, label=labels[j], alpha_err=0.1, total=True, **styles[j])


setup_ax(ax, **s)
ax.legend(loc="lower right", handlelength=5, ncols=2)

savefig(fig, f"present_dada/hardy_edges.pdf")


fig, ax = fig_and_ax(figsize=(0.55 * textwidth, 4))
for j, kappa in kappas.items():
    if j in ["jhardy", "jfan"]:
        plot_mean_kappa(ax, kappa, key=kkf, label=labels[j], alpha_err=0.1, total=True, **styles[j])


setup_ax(ax, **s)
ax.legend(loc="lower right", handlelength=5, ncols=3)

savefig(fig, f"present_dada/hardy_local.pdf")


fig, ax = fig_and_ax(figsize=(0.55 * textwidth, 4))
for j, kappa in kappas.items():
    if j in ["jhardy", "junf"]:
        plot_mean_kappa(ax, kappa, key=kkf, label=labels[j], alpha_err=0.1, total=True, **styles[j])


setup_ax(ax, **s)
ax.legend(loc="lower right", handlelength=5, ncols=3)

savefig(fig, f"present_dada/hardy_unf.pdf")



fig, ax = fig_and_ax(figsize=(0.55 * textwidth, 4))
for j, kappa in kappas.items():
    if j in ["jhardy"]:
        plot_mean_kappa(ax, kappa, key=kkf, label=labels[j], alpha_err=0.1, total=True, **styles[j])


setup_ax(ax, **s)
ax.legend(loc="lower right", handlelength=5, ncols=3)

savefig(fig, f"present_dada/hardy.pdf")



# setup_ax(ax, **s)
# ax.legend(loc="lower right", handlelength=5, ncols=3)

# savefig(fig, f"present_data/m1_hardy.png")
# savefig(fig, img / f"gk/zro_hfs_all_{thermo}.pdf")
