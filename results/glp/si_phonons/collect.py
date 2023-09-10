import sys

sys.path.insert(0, "../../")

from tbx import *

from vibes.phonopy.postprocess import postprocess
from vibes.phonopy.wrapper import set_bandstructure


def get_phonons(folder, suffix="trajectory.son"):
    phonons = postprocess(folder / suffix, enforce_sum_rules=False)

    set_bandstructure(phonons)

    q_mesh = [45, 45, 45]
    phonons.run_mesh(q_mesh)
    phonons.run_total_dos(use_tetrahedron_method=True)

    return {
        "bs_all_distances": np.array(phonons._band_structure._distances),
        "bs_all_frequencies": np.array(phonons._band_structure._frequencies),
        "bs_labels": np.array(phonons._band_structure._labels),
        "bs_special_points": np.array(phonons._band_structure._special_points),
        "dos_frequency_points": np.array(phonons._total_dos._frequency_points),
        "dos_total_dos": np.array(phonons._total_dos._dos),
    }


np.savez_compressed(
    f"production_1_l2_cu5.0_efs_1.npz",
    **get_phonons(
        work_remote
        / "runs/si/production_1_l2_cu5.0_efs_1/phonons/phonons_216/phonopy/",
        suffix="trajectory.son",
    ),
)

np.savez_compressed(
    f"production_1_l2_cu5.0_ef_1.npz",
    **get_phonons(
        work_remote / "runs/si/production_1_l2_cu5.0_ef_1/phonons/phonons_216/phonopy/",
        suffix="trajectory.son",
    ),
)

np.savez_compressed(
    f"production_1_l2_cu6.0_ef_1.npz",
    **get_phonons(
        work_remote / "runs/si/production_1_l2_cu6.0_ef_1/phonons/phonons_216/phonopy/",
        suffix="trajectory.son",
    ),
)

np.savez_compressed(
    f"production_1_l1_cu5.0_efs_1.npz",
    **get_phonons(
        work_remote
        / "runs/si/production_1_l1_cu5.0_efs_1/phonons/phonons_216/phonopy/",
        suffix="trajectory.son",
    ),
)

np.savez_compressed(
    f"production_1_l1_cu5.0_ef_1.npz",
    **get_phonons(
        work_remote / "runs/si/production_1_l1_cu5.0_ef_1/phonons/phonons_216/phonopy/",
        suffix="trajectory.son",
    ),
)


np.savez_compressed(
    f"production_1_l3_cu5.0_ef_1.npz",
    **get_phonons(
        work_remote / "runs/si/production_1_l3_cu5.0_ef_1/phonons/phonons_216/phonopy/",
        suffix="trajectory.son",
    ),
)

np.savez_compressed(
    f"aims_256.npz",
    **get_phonons(work_remote / "runs/si/reference/", suffix="phonopy.son"),
)
