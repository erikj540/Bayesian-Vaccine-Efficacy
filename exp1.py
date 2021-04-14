import os
import numpy as np
import arviz as ar
import pystan as ps
from utilities.utilityFunctions import unpickle_object, pickle_object
from library import create_vax_data, sample_from_model, get_command_line_arguments

DATA_DIR = '/Users/erjo3868/Bayesian-Vaccine-Efficacy/data/exp1'
beta0, beta1, se, sp = 0.5, np.log(0.9), 0.95, 0.95
true_params = {'beta0': beta0, 'beta1': beta1, 'se': sp, 'sp': se}
n_sims = 20
n_burnin, n_samples, n_chains = 1000, 5000, 3
N_vals = [10, 50, 100, 500, 1000, 5000, 10000, 50000, 100000]
# N_vals, n_burnin, n_samples, n_chains, n_sims = [10, 50], 50, 100, 2, 3 # for testing

for N in N_vals:
    print(f'Starting N={N}')
    for ii in range(n_sims):
        model = unpickle_object(os.path.join(DATA_DIR, 'model.pkl'))
        data = create_vax_data(N, 0.5, beta0, beta1, se, sp)
        fit = sample_from_model(model, data, n_burnin, n_samples, n_chains)
        idata = ar.from_pystan(fit)
        pickle_object(os.path.join(DATA_DIR, f'{N}_{ii}.pkl'), idata)
        del(model)
    print(f'DONE WITH N={N}')

