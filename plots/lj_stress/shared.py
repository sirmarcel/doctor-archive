from tbx import *


def get_data(suffix="32"):
    return load(
        glp_work
        / f"implementation_stress_and_heat_flux/lj_mk04/results_{suffix}.npz"
    )


def get(data, key, prop="stress"):
    true = data[prop + "_reference"].flatten()
    pred = data[prop + "_" + key].flatten()

    return true, pred


def mae(true, pred):
    return np.mean(np.abs(true - pred))


def maxae(true, pred):
    return np.max(np.abs(true - pred))


def ape(true, pred):
    return np.abs((true - pred) / pred)


def mape(true, pred):
    return 100 * np.mean(ape(true, pred))


def maxape(true, pred):
    return 100 * np.max(ape(true, pred))
