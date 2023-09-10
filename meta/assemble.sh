cd ..

rm -r results
rm -r plots
rm -r thesis

cd meta
sh copy_results.sh
sh copy_plots.sh
sh copy_thesis.sh