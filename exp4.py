import os
import numpy as np
import arviz as ar
import pystan as ps
import glob
from utilities.utilityFunctions import unpickle_object, pickle_object, remove_and_make_directory
from library import create_vax_data, sample_from_model, get_command_line_arguments
from scipy.stats import uniform, norm, beta, gamma

DATA_DIR = '/Users/erjo3868/Bayesian-Vaccine-Efficacy/data/exp4'

# remove files that aren't the Stan model
# files = glob.glob(os.path.join(DATA_DIR, '*.pkl'))
# files = [f for f in files if f.split('/')[-1]!='model.pkl']
# for f in files: os.remove(f)

n_burnin, n_samples, n_chains = 1000, 5000, 3
N = 5000
n_sims = 200
# N, n_burnin, n_samples, n_chains, n_sims = 100, 50, 100, 2, 3 # for testing

print(f'Starting simulations')
for ii in range(189, n_sims):
    model = unpickle_object(os.path.join(DATA_DIR, 'model.pkl'))
    beta0 = norm.rvs(loc=0, scale=1)
    beta1 = (-1)*gamma.rvs(a=2, scale=1/4)
    se = beta.rvs(a=10, b=2)
    sp = beta.rvs(a=10, b=2)
    true_params = {'beta0': beta0, 'beta1': beta1, 'se': se, 'sp': sp}

    data = create_vax_data(N, 0.5, beta0, beta1, se, sp)
    fit = sample_from_model(model, data, n_burnin, n_samples, n_chains)
    idata = ar.from_pystan(fit)

    results = {'true_params': true_params, 'idata': idata}
    pickle_object(os.path.join(DATA_DIR, f'{ii}.pkl'), results)
    del(model)
print(f'Done with simulations')

