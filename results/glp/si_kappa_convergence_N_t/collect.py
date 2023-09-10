import sys

sys.path.insert(0, "../../")

import xarray as xr
import numpy as np
from tbx.load import ensemble
from tbx import gk, get_and_concatenate

from pathlib import Path

basedir = Path("/talos/scratch/mlang/glp-work/runs/si")

models = ["production_1_l2_cu5.0_ef_1"]
workflow = "gk_1_fl"


def filename(n_atoms, maxsteps, freq=1.0):
    if n_atoms == 512:
        maxsteps = int(maxsteps * (1 / 2))
        return f"gk.to_{maxsteps}.every_5.freq_{freq:.2f}.nc"
    else:
        maxsteps = int(maxsteps * (1 / 10))
        return f"gk.to_{maxsteps}.freq_{freq:.2f}.nc"


def get_dataset(model, temperature, n, maxsteps):
    return gk.combine(
        ensemble(
            ((basedir / model) / workflow) / f"{temperature}/n_{n}",
            "maxsteps",
            filename(n, maxsteps, freq=1.0),
        ),
        maxtime=1e6,
    )


def get_kappa(model, temperature, n, maxsteps):
    data = get_dataset(model, temperature, n, maxsteps)
    return gk.get_kappa(data, a=None, eps=0)


n_atomss = [512, 1728, 4096]

def get_range(maximum):
    return range(500000, maximum + 1, 500000)

maximums = {
    400: {
        512: 10_000_000,
        1728: 10_000_000,
        4096: 10_000_000,
    },
    800: {
        512: 10_000_000,
        1728: 10_000_000,
        4096: 8_000_000,
    },
}

for model in models:
    for temperature in [400, 800]:
        outfile = Path(f"{model}_{temperature}.nc")
        if outfile.is_file():
            print(f"{outfile} exists, skip")
            continue

        print(f"working on {outfile.stem}")

        def get_maxsteps(n, maxsteps):
            k, e = get_kappa(model, temperature, n, maxsteps)
            print(f"...... {maxsteps} {k:.1f}±{e:.1f}")
            k = xr.DataArray(k, name="kappa_mean")
            e = xr.DataArray(e, name="kappa_stderr")

            d = xr.Dataset({"kappa_mean": k, "kappa_stderr": e})

            return d

        def get_maxstepss(n):
            print(f"... n={n}")
            return get_and_concatenate(
                lambda maxsteps: get_maxsteps(n, maxsteps), get_range(maximums[temperature][n]), "maxsteps"
            )

        def get_n_atomss():
            return get_and_concatenate(lambda n: get_maxstepss(n), n_atomss, "n_atoms")

        data = get_n_atomss()
        data.to_netcdf(outfile)
