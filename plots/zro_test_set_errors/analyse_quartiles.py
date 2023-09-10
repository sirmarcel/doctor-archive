from tbx import *

data = load(gknet / "test_set_errors/nomad.nc").forces * 1e3

n = 35169
temps = np.array(range(300, 2401, 300))
n_per_temp = int(n / len(temps))

print(n_per_temp)

for t in data.t:
    for cu in data.cutoff:
        d = data.sel(t=t, cutoff=cu).data
        idx = np.argsort(d)
        upper = int(0.25 * n)

        print(np.unique(((idx[-upper:] // n_per_temp)+1)*300, return_counts=True))
