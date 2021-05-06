#!/bin/bash

##SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=23:50:00
#SBATCH --mem-per-cpu=500MB

# mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-type=ALL
#SBATCH --mail-user=erjo3868@colorado.edu

#SBATCH --job-name=pt3
#SBATCH --output=/Users/erjo3868/Bayesian-Vaccine-Efficacy/fiji_out/pt3.out
#SBATCH --error=/Users/erjo3868/Bayesian-Vaccine-Efficacy/fiji_out/pt3.err

/Users/erjo3868/anaconda3/envs/stan/bin/python scripts/point3.py --i=${i}
