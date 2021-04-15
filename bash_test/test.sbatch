#!/bin/bash

##SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=23:00:00
#SBATCH --mem-per-cpu=500MB

# mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-type=ALL
#SBATCH --mail-user=erjo3868@colorado.edu

# python ${NAME}.py
python print_test.py