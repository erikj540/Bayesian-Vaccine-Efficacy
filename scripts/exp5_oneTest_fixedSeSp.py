import pystan
import arviz as ar
from scipy.special import expit, logit
import os

from utilities.utilityFunctions import unpickle_object, pickle_object
from BayesianVE.library import *

NAME = 'flu_prev50_N10000'
DATA_DIR = '/Users/erjo3868/Bayesian-Vaccine-Efficacy/data'
MODEL_DIR = '/Users/erjo3868/Bayesian-Vaccine-Efficacy/stan_models'
TEST = 0 # 1=test, 0=not test

# set parameters
if TEST==1: # testing
    N_0, N_1 = 50, 40
    n_burnin, n_samples, n_chains = 10, 100, 2
    n_burnin, n_samples, n_chains = 1000, 3000, 3
else: # not testing
    N_0, N_1 = 10000, 10000
    n_burnin, n_samples, n_chains = 1000, 3000, 3

prev = 0.5
alpha = 0.5
ve = 1-alpha
se = 0.50
sp = 0.90
beta0, beta1 = logit(prev), np.log(alpha)
vax_prop = 0.5

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
data = dataEngine.create_one_test_data(N, se, sp, 0)
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
idata = ar.from_pystan(fit)
del(model)

# save results
results = {
    'params': params,
    'data': data,
    'stan_data': stan_data,
    'idata': idata
}
pickle_object(os.path.join(DATA_DIR,f'{NAME}.pkl'), results)


