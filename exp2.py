import os
import numpy as np
import arviz as ar
import pystan as ps
import glob
from utilities.utilityFunctions import unpickle_object, pickle_object, remove_and_make_directory
from library import create_vax_data, sample_from_model, get_command_line_arguments


DATA_DIR = '/Users/erjo3868/Bayesian-Vaccine-Efficacy/data/exp2'
# remove files that aren't the Stan model
files = glob.glob(os.path.join(DATA_DIR, '*.pkl'))
files = [f for f in files if f.split('/')[-1]!='model.pkl']
for f in files: os.remove(f)

beta0, beta1, se, sp = 0.5, np.log(0.9), 0.95, 0.95
true_params = {'beta0': beta0, 'beta1': beta1, 'se': sp, 'sp': se}
n_burnin, n_samples, n_chains = 1000, 5000, 3
N = 5000
n_sims = 200
# N, n_burnin, n_samples, n_chains, n_sims = 100, 50, 100, 2, 3 # for testing

print(f'Starting simulations')
for ii in range(n_sims):
    model = unpickle_object(os.path.join(DATA_DIR, 'model.pkl'))
    data = create_vax_data(N, 0.5, beta0, beta1, se, sp)
    fit = sample_from_model(model, data, n_burnin, n_samples, n_chains)
    idata = ar.from_pystan(fit)
    pickle_object(os.path.join(DATA_DIR, f'{ii}.pkl'), idata)
    del(model)
print(f'Done with simulations')

