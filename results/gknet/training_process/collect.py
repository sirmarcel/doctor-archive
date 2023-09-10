import xarray as xr
import numpy as np


data = np.loadtxt(
    "/u/mlang/gknet/gknet/experiments/ccl_zro_t96/cu_5.0_e_inpt_4387/train_n2_s1/train/log.csv",
    skiprows=1,
    delimiter=",",
)
keys = [
    "time",
    "lr",
    "loss_train",
    "loss_valid",
    "mae_energy",
    "mae_forces",
    "mae_stress",
]

epochs = {"epoch": np.arange(data.shape[0])}

result = {}
for i, key in enumerate(keys):
    result[key] = xr.DataArray(data=data[:, i], coords=epochs, dims="epoch")

dataset = xr.Dataset(result)
dataset.to_netcdf("cu5_n2.nc")
