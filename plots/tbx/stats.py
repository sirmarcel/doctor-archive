from scipy.stats import t

# we use 11 trajectories everywhere for now
tinv = lambda p, df: abs(t.ppf(p / 2, df))
ci_factors = [tinv(1.0 - pp, 11 - 1) for pp in [0.68, 0.95, 0.997]]
ci_68 = ci_factors[0]
ci_95 = ci_factors[1]
