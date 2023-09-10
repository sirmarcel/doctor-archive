from tbx import *

data = np.loadtxt("stats.csv", delimiter=",", skiprows=1)
fig, ax = fig_and_ax(figsize=(marginwidth, marginheight))

x = list(range(data.shape[0]))
xlabels = []
for year, month in data[:, 0:2]:
    # x.append(year-2021+month)
    # xlabels.append(f"{int(year)}-{int(month):02d}")
    xlabels.append(f"{int(month)}")

ax.plot(x, data[:, 2]+data[:, 3], label="QM+MD", color=black, linestyle=solid)
ax.plot(x, data[:, 2], label="QM", color=black, linestyle=dashed)
ax.plot(x, data[:, 3], label="MD", color=red, linestyle=dotted)

ax.set_xticks(x)
ax.set_xticklabels(xlabels)

major_ticks_every(ax, 10, "y")

# ax.set_ylabel("Usage in \%")
# ax.set_xlabel("Month")

ax.set_ylim(0, 77)

ax.legend(loc="best", frameon=False)
savefig(fig, "preview.png")
savefig(fig, img / "front/archer_usage.pdf")
