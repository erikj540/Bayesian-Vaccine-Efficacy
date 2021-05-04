import pystan
import arviz as ar
from scipy.special import expit, logit
import os, argparse

from utilities.utilityFunctions import unpickle_object, pickle_object
from BayesianVE.library import *

# NAME = 'point3'
DATA_DIR = '/Users/erjo3868/Bayesian-Vaccine-Efficacy/4local'
MODEL_DIR = '/Users/erjo3868/Bayesian-Vaccine-Efficacy/stan_models'
MODEL_PATH = os.path.join(MODEL_DIR, 'one_test_fixed.pkl')
TEST = 0 # 1=test, 0=not test

# set parameters
if TEST==1: # testing
    N = 50
    N_BURNIN, N_SAMPLES, N_CHAINS = 10, 100, 2
else: # not testing
    N_BURNIN, N_SAMPLES, N_CHAINS = 1000, 10000, 1

def fixed_se_sp(prev, alpha, se, sp, vax_prop, N, model_path, name):

params = {
    'N': N,
    'prev': prev,
    'alpha': alpha,
    've': ve,
    'se': se,
    'sp': sp,
    'beta0': beta0,
    'beta1': beta1,
    'vax_prop': vax_prop,
    'n_burnin': n_burnin,
    'n_samples': n_samples,
    'n_chains': n_chains
}

dataEngine = StudyData(vax_prop, beta0, beta1)

# generate data
data = dataEngine.generate_one_test_data(N, se, sp, 0)
stan_data = {
    'N': data['N'],
    'x1': np.array(data['X']['vax']),
    'testResults': np.array(data['X']['test_result']),
    'se': data['se'],
    'sp': data['sp']
}

# fit model
model = unpickle_object(os.path.join(MODEL_DIR, 'one_test_fixed.pkl'))
fit = sample_from_model(model, stan_data, n_burnin, n_samples, n_chains)
idata_corrected = ar.from_pystan(fit)
del(model)

# fit model assuming perfect sensitivity and specificity
stan_data = {
    'N': data['N'],
    'x1': np.array(data['X']['vax']),
    'testResults': np.array(data['X']['test_result']),
    'se': 1,
    'sp': 1,
}

# fit model
model = unpickle_object(os.path.join(MODEL_DIR, 'one_test_fixed.pkl'))
fit = sample_from_model(model, stan_data, n_burnin, n_samples, n_chains)
idata_uncorrected = ar.from_pystan(fit)
del(model)


# save results
results = {
    'params': params,
    'data': data,
    # 'stan_data': stan_data,
    'idata_corrected': idata_corrected,
    'idata_uncorrected': idata_uncorrected
}

NAME = NAME+f'_N{N}_prev{int(100*prev)}_alpha{int(100*alpha)}_se{int(se*100)}_sp{int(sp*100)}_vaxProp{int(vax_prop*100)}'
pickle_object(os.path.join(DATA_DIR,f'{NAME}.pkl'), results)


