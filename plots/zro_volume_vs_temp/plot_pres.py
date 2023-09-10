from tbx import *
from tbx.gk import *

develop = False

# otherwise things are very slow
if develop:
    import matplotlib as mpl

    mpl.rcParams["text.usetex"] = False

fig, ax = fig_and_ax(figsize=(0.95 * textwidth, 4))


schnet = load(gknet / "volume_vs_temp/cu5_n2.nc")

sokratess = {
    name: load(glp / f"zro_volume_vs_temp/{name}.nc")
    for name in [
        "verdi_1_l2_cu5.0_efs_1",
        "verdi_1_l2_cu5.0_efs_3",
        "inpt_96_l2_cu5.0_efs_3",
        "inpt_324_l2_cu5.0_efs_3",
    ]
}

ours_verdi = load(gknet / "volume_vs_temp/cu5_n2_verdi.nc")
ours_verdi_cont = load(gknet / "volume_vs_temp/cu5_n2_verdi_cont.nc")

verdi = load(gknet / "volume_vs_temp/verdi.nc")
kh98 = np.loadtxt("kh98.csv", delimiter=",")


def plot(ax, data, label, color, maxsteps=211000, linestyle=solid):
    window = 1000
    temp = (
        data.external_temperature.isel(time=slice(0, maxsteps))
        .to_series()
        .rolling(window=window)
        .mean()
        .to_numpy()
    )
    vol = (
        data.volume.isel(time=slice(0, maxsteps))
        .to_series()
        .rolling(window=window, center=True)
        .mean()
        .to_numpy()
    )
    ax.plot(temp, vol, color=color, label=label, linestyle=linestyle)


# plot(ax, ours_verdi, "SchNet (our data + verdi)", orange, maxsteps=230000)
# plot(ax, ours_verdi_cont, "SchNet (verdi only)", blue)
ax.plot(kh98[:, 0], kh98[:, 1], color=teal, label="Kisi et al. (exp.)")
ax.plot(verdi.external_temperature, verdi.volume, color=red, label="Verdi et al.")
plot(ax, schnet, "SchNet", black)

plot(
    ax,
    sokratess["inpt_96_l2_cu5.0_efs_3"],
    "So3krates (NPT Data)",
    magenta,
    maxsteps=300000,
    linestyle=finedot,
)

plot(
    ax,
    sokratess["verdi_1_l2_cu5.0_efs_3"],
    "So3krates (Verdi Data)",
    blue,
    maxsteps=256555,
    linestyle=finedash,
)

# ax.plot(temp, ours.volume, color=black, alpha=0.2)

ax.set_xlabel("Temperature in K")
ax.set_ylabel("Unit cell volume in Å$^3$")

transition = 1725
ax.axvline(transition, color=black, alpha=0.3, linestyle=dashed)
# ax.text(transition + 40, 150, render_temp(1700, develop=develop, approx=True))

transition = 1400
ax.axvline(transition, color=black, alpha=0.3, linestyle=dashed)
# ax.text(transition + 40, 151, render_temp(1400, develop=develop, approx=True))


handles, labels = ax.get_legend_handles_labels()
ax.legend(reversed(handles), reversed(labels), loc="upper left")

minor_ticks_every(ax, 100)
minor_ticks_every(ax, 1, direction="y")

ax.set_xlim(0, 2800)

savefig(fig, "present/preview.png")
savefig(fig, "present/preview.pdf")
# savefig(fig, img / "gk/zro_vol_vs_temp.pdf")
