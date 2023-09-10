import xarray as xr
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plot

basedir = Path("/talos/scratch/mlang/gknet-nnmd/experiments/ccl_zro_t96/")


def vector_norm(x, dim, ord=None):
    return xr.apply_ufunc(
        np.linalg.norm,
        x,
        input_core_dims=[[dim]],
        kwargs={"ord": ord, "axis": -1},
        dask="parallelized",
    )


def get_displacements(data, start_idx=500, mode="mean", mean_slice=None):
    if mode == "mean":
        if mean_slice is None:
            reference = data.positions.mean(dim="time")
        else:
            reference = data.positions.isel(time=mean_slice).mean(dim="time")
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


ens = "01"

trajs_monoclinic = {}
trajs_monoclinic[300] = xr.open_mfdataset(
    f"{basedir}/cu_5.0_e_inpt_4387/train_n2_s1/variations_mex_2/300/n_1500/{ens}/md/trajectory/*.nc"
)

trajs_monoclinic[600] = xr.open_mfdataset(
    f"{basedir}/cu_5.0_e_inpt_4387/train_n2_s1/variations_mex_2/600/n_1500/{ens}/md/trajectory/*.nc"
)

trajs_monoclinic[1400] = xr.open_mfdataset(
    f"{basedir}/cu_5.0_e_inpt_4387/train_n2_s1/variations_mex_2/1400/n_1500/{ens}/md/trajectory/*.nc"
)

for temp in [900, 1200]:
    trajs_monoclinic[temp] = xr.open_mfdataset(
        f"{basedir}/cu_5.0_e_inpt_4387/train_n2_s1/monoclinic_exp_real_prod_1/{temp}/n_1500/{ens}/md/trajectory/*.nc"
    )

trajs_tetragonal = {}
trajs_tetragonal[1400] = xr.open_mfdataset(
    f"{basedir}/cu_5.0_e_inpt_4387/train_n2_s1/variations_tex_2/1400/n_1500/{ens}/md/trajectory/*.nc"
)

for temp in [1500, 1650, 1800, 1900]:
    trajs_tetragonal[temp] = xr.open_mfdataset(
        f"{basedir}/cu_5.0_e_inpt_4387/train_n2_s1/tetragonal_exp_real_prod_1/{temp}/n_1500/{ens}/md/trajectory/*.nc"
    )

trajs_exploded = {}
for temp in [2000]:
    trajs_exploded[temp] = xr.open_mfdataset(
        f"{basedir}/cu_5.0_e_inpt_4387/train_n2_s1/tetragonal_exp_real_prod_1/{temp}/n_1500/{ens}/md/trajectory/*.nc"
    )

minsteps = 0
maxsteps = 250000
stepsize = 250

monoclinic = {
    k: v.isel(time=slice(minsteps, maxsteps, stepsize))
    for k, v in trajs_monoclinic.items()
}
tetragonal = {
    k: v.isel(time=slice(minsteps, maxsteps, stepsize))
    for k, v in trajs_tetragonal.items()
}
exploded = {
    k: v.isel(time=slice(minsteps, maxsteps, stepsize))
    for k, v in trajs_exploded.items()
}

disp_monoclinic = {
    k: get_norm_displacements(v, start_idx=500).max(dim="I")
    for k, v in monoclinic.items()
}
disp_tetragonal = {
    k: get_norm_displacements(v, start_idx=500).max(dim="I")
    for k, v in tetragonal.items()
}
disp_exploded = {
    k: get_norm_displacements(v, start_idx=500, mean_slice=slice(0, 100)).max(dim="I")
    for k, v in exploded.items()
}

disp_tetragonal = {**disp_tetragonal, **disp_exploded}


def make_dataset(data):
    temps = xr.DataArray(
        np.array([k for k in data.keys()]), name="temperature", dims="temperature"
    )
    ds = xr.concat(list(data.values()), dim=temps)

    return ds


data_monoclinic = make_dataset(disp_monoclinic)
data_tetragonal = make_dataset(disp_tetragonal)

data_monoclinic.to_netcdf("schnet_monoclinic.nc")
data_tetragonal.to_netcdf("schnet_tetragonal.nc")


