import numpy as np

qc = [
    # "a.out",
    # "precise",
    # "gs2", gyrokinetics
    # "fluidity", fluid dynamics
    "vasp",
    # "smilei", plasma
    "castep",
    # "iimb", ?
    # "gromacs", classical MD
    # "met office um", weather presumable
    # "software",
    "nwchem",  # https://www.nwchem-sw.org
    # "nek5000", navier-stokes
    # "openfoam", CDF
    "onetep",  # DFT https://onetep.org
    # "code_saturne", CFD
    "siesta",  # linear-scaling DFT https://departments.icmab.es/leem/siesta/
    # "hemelb", BLOOD DYNAMICS
    # "axisem3d", earth stuff
    "cpmd",  # car-parrinello MD https://www.cpmd.org/wordpress/CPMD/getFile.php?file=manual.pdf
    "elk",  # all electron DFT https://elk.sourceforge.io
    "gpaw",  # friends!
    "fhi aims",  # friends!
    # "unidentified",
    # "sbli", # fluids
    # "pdns3d", dunno what this is, i think turbulent flows
    # "senga", "compressible 3d direct numerical simulation"
    # "cloverleaf", hydro
    # "arm forge",
    "hande",  # quantum monte carlo and stuff http://dx.doi.org/10.1021/acs.jctc.8b01217
    # "r-matrix",
    # "nemo", # ocean stuff
    # "fvcom", # ocean stuff
    "rmt",  # many-electron stuff https://iopscience.iop.org/article/10.1088/1742-6596/388/3/032043/pdf
    "casino",  # quantum monte carlo
    "ukrmol+",  # electronic processes https://www.sciencedirect.com/science/article/abs/pii/S0010465519303972
    "xcompact3d",  # flow solver
    # "cluster", # impossible to google
    # "echam", # atmospheric
    # "cesm", # earth
    # "amber", # force field
    # "python",
    # "cosa", # navier stokes
    "crystal",  # quantum chemistry https://www.crystal.unito.it
    # "dl_meso", # mesoscale modeling
    # "wrf", weather
    # "epoch", # plasma
    # "ptau3d", turbulence
    # "lammps", MD
    # "zacros", # kinetic monte carlo https://zacros.org, not sure if that's QC
    # "dl_poly", # MD
    # "mitgcm", # atmosphere
    # "tpls", # direct simulationTM
    # "edamame", # hard to google
    # "hydra", # ?
    # "namd", # classical MD http://www.ks.uiuc.edu/Research/namd/
    # "nektar++", PDEs
    "quantum espresso",  # https://www.quantum-espresso.org
    # "3dns", ?
    "chemshell",  # multiscale https://chemshell.org QM/MM
    # "osiris", # plasma
    "cp2k",  # https://www.cp2k.org
    # "overall",
]

md = [
    "gromacs",  # classical MD
    "amber",  # force field
    # "dl_meso", # mesoscale modeling
    "lammps",  # MD
    # "zacros", # kinetic monte carlo https://zacros.org, not sure if that's QC
    "dl_poly",  # MD
    "namd",  # classical MD http://www.ks.uiuc.edu/Research/namd/
]

months = [(2021, 12)]
for month in range(1, 12):
    months.append((2022, month))

data = {}
keys = []
for year, month in months:
    percent_dft = 0.0
    percent_md = 0.0
    with open(f"{year}-{month:02d}.csv") as f:
        for line in f.readlines():
            split = line.split(",")
            keys.append(split[0])
            if any(x in split[0].lower() for x in qc):
                if year == 2021 or (year == 2022 and month <= 1):
                    percent_dft += float(split[7])
                else:
                    percent_dft += float(split[8])

            if any(x in split[0].lower() for x in md):
                if year == 2021 or (year == 2022 and month <= 1):
                    percent_md += float(split[7])
                else:
                    percent_md += float(split[8])

        data[(year, month)] = (percent_dft, percent_md)

for k, v in data.items():
    print(f"{k}: {v}")

keys = [k.lower() for k in keys]
keys = list(set(keys))
print(keys)

with open("stats.csv", "w") as f:
    f.write("year,month,percent_dft,percent_md\n")
    for k, v in data.items():
        year, month = k
        v1, v2 = v
        f.write(f"{year},{month:02d},{v1:.2f},{v2:.2f}\n")
