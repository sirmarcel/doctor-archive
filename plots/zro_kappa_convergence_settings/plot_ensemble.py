from tbx import *
from tbx.gk import *


kkt = kk + "_total"
kkft = kkf + "_total"
kkmt = kkm + "_total"
kkfmt = kkfm + "_total"
kkfst = kkfs + "_total"


def get_data(thermo, setting):
    return load(
        gknet / f"kappa_convergence_settings/overview_{thermo}_{setting}.nc"
    )

def setup_ax(ax, ylim=(-1, 10), xlim=30e3):
    ax.set_xlabel("Integration time in ps")
    ax.set_ylabel(kappa_label())
    minor_ticks_every(ax, 1000)
    major_ticks_every(ax, 1, direction="y")
    scale_labels(ax, 1000)
    ax.set_xlim(0, xlim)
    ax.set_ylim(ylim)
    ax.legend(loc="lower right")


def plot(ax, thermo):
    data = get_data(thermo, "converged")
    for i in range(11):
        k = isotropic(data[kkf].isel(trajectory=i))
        kt = isotropic(data[kkt].isel(trajectory=i))

        if i == 0:
            kt.plot(ax=ax, color=red, alpha=0.25, label=nolabel)
            k.plot(ax=ax, color=red, alpha=0.75, label="Single")
        else:
            kt.plot(ax=ax, color=red, alpha=0.25, label=nolabel)
            k.plot(ax=ax, color=red, alpha=0.75, label=nolabel)

    k = isotropic(data[kkfm])
    kt = isotropic(data[kkmt])

    kt.plot(ax=ax, color=black, alpha=0.5, label=nolabel)
    k.plot(ax=ax, color=black, alpha=1.00, label="Mean")

    ke = isotropic(data[kkfs])

    (k + ke).plot(
        ax=ax, color=black, alpha=1.00, linestyle=dashed, label="Standard Error"
    )
    (k - ke).plot(ax=ax, color=black, alpha=1.00, linestyle=dashed, label=nolabel)

    # plot_cutoff(ax, data, cutoff=True, alpha_err=0, kappa=True, color=grey)


thermo = "m_300"
fig, ax = fig_and_ax(figsize=(0.95 * textwidth, 4))
plot(ax, thermo)
setup_ax(ax, ylim=(0, 9.6), xlim=40e3)
savefig(fig, f"ensemble/preview_{thermo}.png")
savefig(fig, img / f"gk/zro_kc_ens_{thermo}.pdf")


thermo = "m_600"
fig, ax = fig_and_ax(figsize=(0.95 * textwidth, 4))
plot(ax, thermo)
setup_ax(ax, ylim=(0, 6.1), xlim=30e3)
savefig(fig, f"ensemble/preview_{thermo}.png")
savefig(fig, img / f"gk/zro_kc_ens_{thermo}.pdf")

thermo = "m_1400"
fig, ax = fig_and_ax(figsize=(0.95 * textwidth, 4))
plot(ax, thermo)
setup_ax(ax, ylim=(0, 2.75), xlim=10e3)
savefig(fig, f"ensemble/preview_{thermo}.png")
savefig(fig, img / f"gk/zro_kc_ens_{thermo}.pdf")

thermo = "t_1400"
fig, ax = fig_and_ax(figsize=(0.95 * textwidth, 4))
plot(ax, thermo)
setup_ax(ax, ylim=(0, 2.75), xlim=10e3)
savefig(fig, f"ensemble/preview_{thermo}.png")
savefig(fig, img / f"gk/zro_kc_ens_{thermo}.pdf")
