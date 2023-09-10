from tbx import *


def get_data(suffix="32", L=2):
    return load(
        glp_work
        / f"implementation_stress_and_heat_flux/snse/production_models_train_default_L{L}/results_{suffix}.npz"
    )


def get(suffix, key, prop="stress", L=2):
    data = get_data(suffix=suffix, L=L)

    if prop == "stress":
        if suffix == "32":
            d = 1e-3
        elif suffix == "64":
            d = 1e-4

        reference = f"finite_differences_{d:.0e}"
    elif prop == "heat_flux":
        reference = "hf_hardy"

    if prop == "heat_flux":
        from ase.units import fs

        factor = fs
    else:
        factor = 1

    true = data[prop + f"_{reference}"].flatten() * factor
    pred = data[prop + "_" + key].flatten() * factor

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


def r2(true, pred):
    mean = np.mean(true)
    sum_of_squares = np.sum((true - mean) ** 2)
    sum_of_residuals = np.sum((true - pred) ** 2)

    return 100 * (1.0 - (sum_of_residuals / sum_of_squares))
