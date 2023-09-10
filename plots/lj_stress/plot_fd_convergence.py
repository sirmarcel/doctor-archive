from shared import *

fig, ax = fig_and_ax(figsize=(0.95 * textwidth, 4))
for suffix in ["32", "64"]:
    if suffix == "32":
        linestyle = solid
        color = black
        label = "Single"
    else:
        linestyle = dashed
        color = red
        label = "Double"

    data = get_data(suffix=suffix)

    ds = np.logspace(-6, -2, num=5 + 2 * 4, base=10)

    y = [mae(*get(data, f"finite_differences_{d:.0e}", prop="stress")) for d in ds]

    ax.plot(ds, y, marker=star, color=color, markersize=15, linestyle=linestyle, label=label)

    m = np.argmin(y)
    ax.plot(ds[m], y[m], color=color, marker=bigdot, markersize=18)

ax.legend(loc="center left")

ax.set_ylabel("MAE in eV")
ax.set_xlabel(r"Step size in \unit{\angstrom}")

ax.set_xscale("log", base=10)

ax.set_xticks(ds)
ax.set_xticklabels([f"{d:.0e}" for d in ds])

ax.set_yscale("log", base=10)
ax.set_xlim(0.9e-6, 1.1e-2)

savefig(fig, f"fd/convergence.png")
savefig(fig, img / f"gk/si-lj_stress_fd_convergence.pdf")
