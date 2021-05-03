import numpy as np 
import os

# names = ['exp1', 'exp2']
# names = ['exp4']
names = ['exp3', 'exp4']


###########################################
# EXPERIMENT 1
if 'exp1' in names:
    n_sims = 200
    name = '2exp1'
    model = '/Users/erjo3868/Bayesian-Vaccine-Efficacy/data/exp1/model.pkl'
    folder = '/Users/erjo3868/Bayesian-Vaccine-Efficacy/output/'
    beta0 = 'fixed(0.5)'
    beta1 = 'fixed(0.10536051565782628)'
    se = 'fixed(0.95)'
    sp = 'fixed(0.95)'

    for ii in range(0, n_sims):
        outpath = f'/Users/erjo3868/Bayesian-Vaccine-Efficacy/data/{name}/{ii}.pkl'
        code = f'sbatch --job-name={name}{ii} --output={folder}{name}{ii}.out --error={folder}{name}{ii}.err --export=MODEL={model},OUTPATH={outpath},N=5000,BETA0="{beta0}",BETA1="{beta1}",SE="{se}",SP="{sp}" one_job_launcher.sbatch'
        os.system(code)

###########################################
# EXPERIMENT 2
if 'exp2' in names:
    n_sims = 200
    name = '2exp2'
    model = '/Users/erjo3868/Bayesian-Vaccine-Efficacy/data/exp2/model.pkl'
    folder = '/Users/erjo3868/Bayesian-Vaccine-Efficacy/output/'
    beta0 = 'fixed(0.5)'
    beta1 = 'fixed(0.10536051565782628)'
    se = 'fixed(0.95)'
    sp = 'fixed(0.95)'

    for ii in range(0, n_sims):
        outpath = f'/Users/erjo3868/Bayesian-Vaccine-Efficacy/data/{name}/{ii}.pkl'
        code = f'sbatch --job-name={name}{ii} --output={folder}{name}{ii}.out --error={folder}{name}{ii}.err --export=MODEL={model},OUTPATH={outpath},N=5000,BETA0="{beta0}",BETA1="{beta1}",SE="{se}",SP="{sp}" one_job_launcher.sbatch'
        os.system(code)

###########################################
# EXPERIMENT 3
if 'exp3' in names:
    n_sims = 200
    name = '2exp3'
    model = '/Users/erjo3868/Bayesian-Vaccine-Efficacy/data/exp3/model.pkl'
    folder = '/Users/erjo3868/Bayesian-Vaccine-Efficacy/output/'
    beta0 = 'normal(0-1)'
    beta1 = 'gamma(2-4)'
    se = 'fixed(0.95)'
    sp = 'fixed(0.95)'

    for ii in range(0, n_sims):
        outpath = f'/Users/erjo3868/Bayesian-Vaccine-Efficacy/data/{name}/{ii}.pkl'
        code = f'sbatch --job-name={name}{ii} --output={folder}{name}{ii}.out --error={folder}{name}{ii}.err --export=MODEL={model},OUTPATH={outpath},N=5000,BETA0="{beta0}",BETA1="{beta1}",SE="{se}",SP="{sp}" one_job_launcher.sbatch'
        os.system(code)

###########################################
# EXPERIMENT 4
if 'exp4' in names:
    n_sims = 200
    name = '2exp4'
    model = '/Users/erjo3868/Bayesian-Vaccine-Efficacy/data/exp4/model.pkl'
    folder = '/Users/erjo3868/Bayesian-Vaccine-Efficacy/output/'
    beta0 = 'normal(0-1)'
    beta1 = 'gamma(2-4)'
    se = 'beta(10-2)'
    sp = 'beta(10-2)'

    for ii in range(0, n_sims):
        outpath = f'/Users/erjo3868/Bayesian-Vaccine-Efficacy/data/{name}/{ii}.pkl'
        code = f'sbatch --job-name={name}{ii} --output={folder}{name}{ii}.out --error={folder}{name}{ii}.err --export=MODEL={model},OUTPATH={outpath},N=5000,BETA0="{beta0}",BETA1="{beta1}",SE="{se}",SP="{sp}" one_job_launcher.sbatch'
        os.system(code)