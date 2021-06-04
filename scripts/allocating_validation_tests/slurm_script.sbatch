#!/bin/bash

##SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=23:50:00
#SBATCH --mem-per-cpu=500MB

# mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-type=ALL
#SBATCH --mail-user=erjo3868@colorado.edu

#SBATCH --job-name=pt5
#SBATCH --output=/Users/erjo3868/Bayesian-Vaccine-Efficacy/fiji_out/allocating.out
#SBATCH --error=/Users/erjo3868/Bayesian-Vaccine-Efficacy/fiji_out/allocating.err

# /Users/erjo3868/anaconda3/envs/stan/bin/python scripts/simulation.py -model_name=calibration_study_one_test -n_burnin=${n_burnin} -n_samples=${n_samples} -n_chains=${n_chains} -name=${name} -N=${N} -prev=${prev} -alpha=${alpha} -se=${se} -sp=${sp} -vax_prob=${vax_prob} -n_sens=${n_sens} -n_spec=${n_spec}

/Users/erjo3868/anaconda3/envs/stan/bin/python scripts/simulation.py -model_name=calibration_study_one_test -n_burnin=${n_burnin} -n_samples=${n_samples} -n_chains=${n_chains} -name=${name} -N=${N} -prev=${prev} -alpha=${alpha} -se=${se} -sp=${sp} -vax_prob=${vax_prob} -n_sens=${n_sens} -n_spec=${n_spec}