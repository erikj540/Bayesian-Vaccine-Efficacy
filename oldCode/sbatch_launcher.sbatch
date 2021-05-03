#!/bin/bash

##SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=23:00:00
#SBATCH --mem-per-cpu=500MB

# mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-type=ALL
#SBATCH --mail-user=erjo3868@colorado.edu

#SBATCH --job-name=exp4
#SBATCH --output=/Users/erjo3868/Bayesian-Vaccine-Efficacy/output/exp3.out
#SBATCH --error=/Users/erjo3868/Bayesian-Vaccine-Efficacy/output/exp3.err

/Users/erjo3868/anaconda3/envs/stan/bin/python ${NAME}.py
# python exp1.py
# python exp2.py
# python exp3.py
# python exp4.py 