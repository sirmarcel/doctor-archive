from tbx import *

data = load(gknet / "training_process/cu5_n2.nc")

fig, ax = fig_and_ax(figsize=(0.86 * marginwidth, 1.4 * marginheight))

data.mae_energy.plot(ax=ax)
data.mae_forces.plot(ax=ax, color=red)
data.mae_stress.plot(ax=ax, color=black)

lr = data.lr.data
changes = np.where(np.roll(lr,1)!=lr)[0]
for idx in changes:
    ax.axvline(idx, color=red, linewidth=0.5)

# ax.set_xlim(-10, 2000)

ax.set_yscale("log")
ax.set_xscale("log")

savefig(fig, "preview.png")
# savefig(fig, img / "gk/zro_training_data.pdf")
