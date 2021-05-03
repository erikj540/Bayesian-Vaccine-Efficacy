#!/bin/bash

##SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=23:50:00
#SBATCH --mem-per-cpu=500MB

# mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-type=ALL
#SBATCH --mail-user=erjo3868@colorado.edu

/Users/erjo3868/anaconda3/envs/stan/bin/python one_job.py --model=${MODEL} --N=${N} --outpath=${OUTPATH} --beta0=${BETA0} --beta1=${BETA1} --se=${SE} --sp=${SP}