from tbx import *
from tbx.tables import *

#  train_n2_vs1_fast/
#  train_n2_vs1_fastdecay/
#  train_n2_vs1_fastest/
#  train_n2_vs1_lilbatch/
#  train_n2_vs1_lowstress/
#  train_n2_vs1_wide/


def get_losses(file):
    with open(file) as f:
        lines = f.readlines()
        energy = list(map(float, lines[1].split()[1:4]))
        forces = list(map(float, lines[2].split()[1:4]))

        return energy, forces


title = [f"{'Change':<40}", r"$R^2$ Energy in \%", r"$R^2$ Forces in \%"]
table = []

energy, forces = get_losses(
    gknet_train / f"ccl_zro_t96/cu_5.0_e_inpt_4387/train_n2_s1/predict/nomad/loss.txt"
)
# print(f"og: {energy[2]*100:.1f} {forces[2]*100:.1f}")
comment = "No change"
table.append([f"{comment:<40}", f"{energy[2]*100:.1f}", f"{forces[2]*100:.1f}"])


# modifiers = [
#     "fast", # patience halved
#     "fastdecay", # decay factor 0.5 instead of 0.75
#     "fastest", # patience /10
#     "lilbatch", # batch size 25
#     "lowstress", # stress weight 10
#     "wide", # 256 feature dim
# ]

modifiers = {
    "fast": "Patience halved",
    "fastdecay": r"Learning rate decay $1/2$",
    "fastest": r"Patience reduced to $1/10$",
    "lilbatch": r"Batch size $25$",
    "lowstress": r"Stress weight changed to $10$",
    "wide": r"$256 \rightarrow 128 \rightarrow 1$ output network",
}

for modifier, comment in modifiers.items():
    energy, forces = get_losses(
        gknet_train
        / f"ccl_zro_t96/cu_5.0_e_inpt_4387/train_n2_vs1_{modifier}/predict/nomad/loss.txt"
    )
    table.append([f"{comment:<40}", f"{energy[2]*100:.1f}", f"{forces[2]*100:.1f}"])

print(table_to_string(table))

savetab(
    make_tabular(title, table, layout="l r r", width=30),
    tables / "gk/zro_training_variations.tex",
)

# /Users/marcel/base/desk/phd/projects/gknet/gknet/experiments/ccl_zro_t96/cu_5.0_e_inpt_4387
