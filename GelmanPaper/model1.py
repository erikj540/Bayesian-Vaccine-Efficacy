import pystan
import arviz as ar
from scipy.special import expit, logit
from utilities.utilityFunctions import unpickle_object, pickle_object
from BayesianVE.library import *
import os

NAME = 'model1'
DATA_DIR = '/Users/erjo3868/Bayesian-Vaccine-Efficacy/GelmanPaper'
MODEL_DIR = '/Users/erjo3868/Bayesian-Vaccine-Efficacy/stan_models'
n_burnin, n_samples, n_chains = 1000, 10000, 1

needed_params = [
    'y_sample', 'n_sample',
    'y_spec', 'n_spec',
    'y_sens', 'n_sens'
]

params = {
    'y_sample': 50,
    'n_sample': 3330,
    'y_spec': 399,
    'n_spec': 401,
    'y_sens': 103,
    'n_sens': 122
}

# data for STAN
stan_data = {key: params[key] for key in needed_params}

# fit model
model = unpickle_object(os.path.join(MODEL_DIR, f'Gelman_{NAME}.pkl'))
fit = sample_from_model(model, stan_data, n_burnin, n_samples, n_chains)
idata = ar.from_pystan(fit) 
del(model)

# save results
results = {
    'params': params,
    'idata': idata
}

pickle_object(os.path.join(DATA_DIR,f'{NAME}.pkl'), results)


