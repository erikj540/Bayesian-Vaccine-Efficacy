#!/bin/bash

##SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=23:50:00
#SBATCH --mem-per-cpu=500MB

# mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-type=ALL
#SBATCH --mail-user=erjo3868@colorado.edu

#SBATCH --job-name=pt5
#SBATCH --output=/Users/erjo3868/Bayesian-Vaccine-Efficacy/fiji_out/pt5.out
#SBATCH --error=/Users/erjo3868/Bayesian-Vaccine-Efficacy/fiji_out/pt5.err

/Users/erjo3868/anaconda3/envs/stan/bin/python scripts/point5_slurm.py --prev=${prev} --alpha=${alpha} --se=${se} --sp=${sp} --vax_prop=${vax_prop} --N=${N} --n_sens=${n_sens} --n_spec=${n_spec} --n_sims=${n_sims}