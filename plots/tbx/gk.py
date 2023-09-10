from .literals import *
from .stats import ci_68, ci_95

error_scale = 1.0  # we simply use the standard error for now

kk = "heat_flux_autocorrelation_cumtrapz"
kkf = "heat_flux_autocorrelation_cumtrapz_filtered"
kkm = "heat_flux_autocorrelation_cumtrapz_mean"
kkfm = "heat_flux_autocorrelation_cumtrapz_filtered_mean"
kkfs = "heat_flux_autocorrelation_cumtrapz_filtered_stderr"
khfacf = "heat_flux_autocorrelation"
khfacfm = "heat_flux_autocorrelation_mean"
khfacff = "heat_flux_autocorrelation_filtered"
khfacffm = "heat_flux_autocorrelation_filtered_mean"
khfacffs = "heat_flux_autocorrelation_filtered_stderr"


def diag(quantity, a):
    if a is not None:
        if quantity.dims == ("time", "a", "b"):
            return quantity.sel(a=a, b=a)
        else:
            return quantity.sel(a=a)
    else:
        return isotropic(quantity)


def isotropic(quantity):
    if quantity.dims == ("time", "a", "b"):
        return (
            quantity.sel(a=0, b=0) + quantity.sel(a=1, b=1) + quantity.sel(a=2, b=2)
        ) / 3
    else:
        return quantity.mean(dim="a")


def get_diagonal(quantity):
    return xr.concat([quantity.sel(a=a, b=a) for a in range(3)], dim="a").transpose()


def plot_single_kappa(
    ax, kappa, color=black, alpha=1.0, linestyle=solid, label="__nolabel__", **kwargs
):
    kappa.plot(
        ax=ax, color=color, alpha=alpha, linestyle=linestyle, label=label, **kwargs
    )


def plot_mean_kappa(
    ax,
    dataset,
    color=black,
    alpha=1.0,
    alpha_err=0.1,
    linestyle=solid,
    stderr_mult=1.0,
    key=kkf,
    a=None,
    label="__nolabel__",
    total=False,
    **kwargs,
):
    if total is True:
        total = "_total"
    else:
        total = ""

    mean = dataset[key + "_mean" + total]
    err = stderr_mult * dataset[key + "_stderr" + total]

    mean = diag(mean, a)
    err = diag(err, a)

    plot_single_kappa(
        ax,
        mean,
        color=color,
        alpha=alpha,
        linestyle=linestyle,
        label=label,
        **kwargs,
    )
    ax.fill_between(
        dataset.time,
        mean - err * error_scale,
        mean + err * error_scale,
        alpha=alpha_err,
        color=color,
    )


def get_cutoff(dataset, key="heat_flux_autocorrelation_filtered_mean", a=None, eps=0.0):
    hfacf = diag(dataset[key], a)
    return hfacf.time[hfacf < eps].min()


def plot_cutoff(
    ax,
    dataset,
    suffix="_filtered_mean",
    a=None,
    color=black,
    alpha=1.0,
    linestyle=solid,
    kappa=False,
    cutoff=True,
    eps=0.0,
    alpha_err=0.1,
):
    key_hfacf = "heat_flux_autocorrelation" + suffix
    key_kappa = "heat_flux_autocorrelation_cumtrapz" + suffix
    cu = get_cutoff(dataset, key_hfacf, a=a, eps=eps)
    k = diag(dataset[key_kappa], a)
    key_error = key_kappa.replace("_mean", "_stderr")
    kerr = diag(dataset[key_error], a)

    if cutoff:
        ax.axvline(
            dataset.time.sel(time=cu), color=color, alpha=alpha, linestyle=linestyle
        )

    if kappa:
        ax.axhline(k.sel(time=cu), color=color, alpha=alpha, linestyle=linestyle)
        ax.fill_between(
            k.time,
            k.sel(time=cu) - kerr.sel(time=cu) * error_scale,
            k.sel(time=cu) + kerr.sel(time=cu) * error_scale,
            color=color,
            alpha=alpha_err,
            linestyle=linestyle,
        )

    return float(cu), (float(k.sel(time=cu)), float(kerr.sel(time=cu)))
