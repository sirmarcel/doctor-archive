from tbx import *

develop = False

# otherwise things are very slow
if develop:
    import matplotlib as mpl

    mpl.rcParams["text.usetex"] = False


t = "temperature"
k = "kappa"
e = "error"

raghavan = load(gknet / "kappa_reference/result_raghavan.npz")
mevrel = load(gknet / "kappa_reference/result_mevrel.npz")
bisson = load(gknet / "kappa_reference/result_bisson.npz")
verdi = load(gknet / "kappa_reference/result_verdi.npz")
cc = load(gknet / "kappa_reference/result_cc.npz")
momenzadeh = load(gknet / "kappa_reference/result_momenzadeh.npz")


cu5_n2_mono_exp = load(gknet / "kappa_monoclinic_experiment/result_cu5_n2.nc")
cu5_n2_tetra_exp = load(gknet / "kappa_tetragonal_experiment/result_cu5_n2.nc")

fig, ax = fig_and_ax(figsize=(0.95 * (textwidth + marginwidth), 4.5))



ax.scatter(
    raghavan[t],
    raghavan[k],
    color=black,
    marker=bigdot,
    alpha=0.7,
    label="Raghavan et al. (exp.) (m)",
    # markersize=12,
)

ax.errorbar(
    mevrel[t],
    mevrel[k],
    color=black,
    marker=cross,
    alpha=0.7,
    yerr=mevrel[e],
    linestyle="none",
    elinewidth=1,
    label="Mévrel et al. (exp.) (m)",
    markersize=9,
)



ax.errorbar(
    bisson[t],
    bisson[k],
    yerr=bisson[e],
    color=black,
    marker=diamond,
    alpha=0.7,
    label="Bisson et al. (exp.) (m)",
    elinewidth=1,
    linestyle="none",
    markersize=9,
)


ax.errorbar(
    cc[t],
    cc[k],
    color=orange,
    marker=plus,
    alpha=0.7,
    yerr=cc[e],
    linestyle="none",
    elinewidth=1,
    label="Carbogno et al. (DFT) (t)",
    markersize=10,
    markeredgecolor=black,
)




ax.errorbar(
    verdi[t],
    verdi[k],
    color=teal,
    marker=square,
    alpha=0.7,
    yerr=verdi[e],
    linestyle="none",
    elinewidth=1,
    label="Verdi et al. (MLP) (m,t)",
    markersize=10,
    markeredgecolor=black,
)


ax.errorbar(
    cu5_n2_mono_exp[t],
    cu5_n2_mono_exp["kappa_mean"],
    yerr=cu5_n2_mono_exp["kappa_stderr"],
    color=red,
    marker=thiamond,
    elinewidth=1,
    linestyle="none",
    alpha=0.9,
    label="This work (MLP) (m)",
    markersize=13,
    markeredgecolor=black,
)

ax.errorbar(
    cu5_n2_tetra_exp[t],
    cu5_n2_tetra_exp["kappa_mean"],
    yerr=cu5_n2_tetra_exp["kappa_stderr"],
    color=red,
    marker=dot,
    elinewidth=1,
    linestyle="none",
    alpha=0.9,
    label="This work (MLP) (t)",
    markersize=19,
    markeredgecolor=black,
)


ax.scatter(
    momenzadeh[t][2:],
    momenzadeh[k][2:],
    color=blue,
    marker=star,
    alpha=0.7,
    label="Momenzadeh et al. (FF) (m)",
    s=100,
)

# from IPython import embed

# embed()

handles, labels = ax.get_legend_handles_labels()

# 0['Raghavan et al. (exp.) (m)',
# 1 'Momenzadeh et al. (FF) (m)',
# 2 'Mévrel et al. (exp.) (m)',
# 3 'Bisson et al. (exp.) (m)',
# 4 'Carbogno et al. (DFT) (t)',
# 5 'Verdi et al. (MLP) (m,t)',
# 6 'This work (MLP) (m)',
# 7 'This work (MLP) (t)']

handles = [handles[6], handles[7], handles[5], handles[1], handles[4], handles[3], handles[2], handles[0]]
labels = [labels[6], labels[7], labels[5], labels[1], labels[4], labels[3], labels[2], labels[0]]

# we want tetragonal to be plotted on top, but
# want the legend to be in the opposite order :clown:
# handles[-2], handles[-1] = handles[-1], handles[-2]
# labels[-2], labels[-1] = labels[-1], labels[-2]

ax.legend(handles, labels, loc="upper right", markerfirst=False)

# ax.set_ylim(1, 9.5)
ax.set_ylim(0, 10.5)
ax.set_xlim(200, 1850)

ax.set_xlabel("Temperature in K")
if develop:
    ax.set_ylabel(r"$\kappa$ in W/mK")
else:
    ax.set_ylabel(r"$\kappa$ in \unit{W\per(m.K)}")

minor_ticks_every(ax, 50)
major_ticks_every(ax, 150)

# minor_ticks_every(ax, 50, direction="y")
major_ticks_every(ax, 1, direction="y")


savefig(fig, "preview.png")
savefig(fig, img / "gk/zro_kappa_vs_temperature.pdf")
