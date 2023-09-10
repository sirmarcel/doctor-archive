from pathlib import Path
from vibes.trajectory import reader

base = Path("/talos/scratch/mlang/gknet/raw/ccl_zro_t96")

to_process = [4, 3, 8, 7]
to_keep = ["temperature", "cell"]

def process(i):
    traj = reader(base / f"inpt_{i}.son")
    data = traj.dataset
    keys = list(data.keys())

    for key in keys:
        if key not in to_keep:
            del data[key]

    return data

for i in to_process:
    data = process(i)
    data.to_netcdf(f"{i}.nc")
