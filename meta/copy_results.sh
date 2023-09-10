cd ..
mkdir results

cp meta/README_results.md results/README.md

cd results/

mkdir glp
cd glp
rsync -rL --exclude "__pycache__/" ~/base/desk/phd/projects/glp/glp-results/data/si_kappa_convergence_N_t .
rsync -rL --exclude "__pycache__/" ~/base/desk/phd/projects/glp/glp-results/data/si_phonons .

cd ..
mkdir gknet
cd gknet

rsync -rL --exclude "__pycache__/" ~/base/desk/phd/projects/gknet/gknet-results/data/displacements .
rsync -rL --exclude "__pycache__/" ~/base/desk/phd/projects/gknet/gknet-results/data/training_data .
rsync -rL --exclude "__pycache__/" ~/base/desk/phd/projects/gknet/gknet-results/data/training_process .

mkdir training_variations
cd training_variations

cp ~/base/desk/phd/projects/gknet/gknet/experiments/ccl_zro_t96/cu_5.0_e_inpt_4387/train_n2_vs1_fast/predict/nomad/loss.txt fast.txt
cp ~/base/desk/phd/projects/gknet/gknet/experiments/ccl_zro_t96/cu_5.0_e_inpt_4387/train_n2_vs1_fastdecay/predict/nomad/loss.txt fastdecay.txt
cp ~/base/desk/phd/projects/gknet/gknet/experiments/ccl_zro_t96/cu_5.0_e_inpt_4387/train_n2_vs1_fastest/predict/nomad/loss.txt fastest.txt
cp ~/base/desk/phd/projects/gknet/gknet/experiments/ccl_zro_t96/cu_5.0_e_inpt_4387/train_n2_vs1_lilbatch/predict/nomad/loss.txt lilbatch.txt
cp ~/base/desk/phd/projects/gknet/gknet/experiments/ccl_zro_t96/cu_5.0_e_inpt_4387/train_n2_vs1_lowstress/predict/nomad/loss.txt lowstress.txt
cp ~/base/desk/phd/projects/gknet/gknet/experiments/ccl_zro_t96/cu_5.0_e_inpt_4387/train_n2_vs1_wide/predict/nomad/loss.txt wide.txt
cp ~/base/desk/phd/projects/gknet/gknet/experiments/ccl_zro_t96/cu_5.0_e_inpt_4387/train_n2_s1/predict/nomad/loss.txt default.txt
