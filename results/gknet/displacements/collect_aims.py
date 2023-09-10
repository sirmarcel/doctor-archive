import xarray as xr
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plot

from vibes.trajectory import reader


names = {
    4: 3000,
    8: 2250,
    3: 1500,
    7: 750,
}

aims = {
    names[i]: reader(f"/talos/scratch/mlang/gknet/raw/ccl_zro_t96/inpt_{i}.son").dataset
    for i in [4, 3, 8, 7]
}


def vector_norm(x, dim, ord=None):
    return xr.apply_ufunc(
        np.linalg.norm,
        x,
        input_core_dims=[[dim]],
        kwargs={"ord": ord, "axis": -1},
        dask="parallelized",
    )


def get_displacements(data, start_idx=500, mode="mean"):
    if mode == "mean":
        reference = data.positions.mean(dim="time")
    else:
        reference = data.positions.isel(time=0)
    displacements = data.positions - reference
    if start_idx:
        displacements = displacements.isel(I=slice(start_idx, len(displacements.I)))
    return displacements.compute()


def get_norm_displacements(data, **kwargs):
    #     reference = data.positions.isel(time=0)
    #     reference = data.positions.mean(dim="time")
    displacements = get_displacements(data, **kwargs)
    norm_displacements = vector_norm(displacements, "a")
    #     norm_displacements = norm_displacements.compute()
    return norm_displacements


stepsize = 25

aims = {k: v.isel(time=slice(0, len(v.time), stepsize)) for k, v in aims.items()}

disp_aims = {
    k: get_norm_displacements(v, start_idx=32).max(dim="I") for k, v in aims.items()
}


def make_dataset(data):
    temps = xr.DataArray(
        np.array([k for k in data.keys()]), name="temperature", dims="temperature"
    )
    ds = xr.concat(list(data.values()), dim=temps)

    return ds


data_aims = make_dataset(disp_aims)

data_aims.to_netcdf("aims.nc")

