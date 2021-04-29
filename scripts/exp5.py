import pystan
import arviz as ar
from scipy.special import expit, logit
from scipy.stats import bernoulli, uniform, norm, beta, gamma
from utilities.utilityFunctions import unpickle_object, pickle_object
from BayesianVE.library import *
import os

NAME = 'covid_medium_prev'
DATA_DIR = '/Users/erjo3868/Bayesian-Vaccine-Efficacy/data'
MODEL_DIR = '/Users/erjo3868/Bayesian-Vaccine-Efficacy/stan_models'
TEST = 0 # 1=test, 0=not test

if TEST==1: # testing
    N_0, N_1 = 50, 40
    n_burnin, n_samples, n_chains = 10, 100, 2
    n_burnin, n_samples, n_chains = 1000, 3000, 3
else: # not testing
    N_0, N_1 = 5000, 5000
    n_burnin, n_samples, n_chains = 1000, 3000, 3

prev = 0.5
alpha = 0.1
ve = 1-alpha
se_0 = 0.99
sp_0 = 0.99
se_1 = 0.89
sp_1 = 0.99
beta0, beta1 = logit(prev), np.log(alpha)
vax_prop = 0.5

params = {
    'N0': N_0,
    'N1': N_1,
    'prev': prev,
    'alpha': alpha,
    've': ve,
    'se0': se_0,
    'sp0': sp_0, 
    'se1': se_1,
    'sp1': sp_1,
    'beta0': beta0,
    'beta1': beta1,
    'vax_prop': vax_prop,
    'n_burnin': n_burnin,
    'n_samples': n_samples,
    'n_chains': n_chains
}

dataEngine = StudyData(vax_prop, beta0, beta1)

# run one test model on two datasets
## test 0
data_0 = dataEngine.create_one_test_data(N_0, se_0, sp_0, 0)
stan_data = {
    'N': data_0['N'],
    'x1': np.array(data_0['X']['vax']),
    'testResults': np.array(data_0['X']['test_result']),
    'se': data_0['se'],
    'sp': data_0['sp']
}

model = unpickle_object(os.path.join(MODEL_DIR, 'one_test_fixed.pkl'))
fit = sample_from_model(model, stan_data, n_burnin, n_samples, n_chains)
idata_0 = ar.from_pystan(fit)
del(model)

## test 1
data_1 = dataEngine.create_one_test_data(N_1, se_1, sp_1, 1)
stan_data = {
    'N': data_1['N'],
    'x1': np.array(data_1['X']['vax']),
    'testResults': np.array(data_1['X']['test_result']),
    'se': data_1['se'],
    'sp': data_1['sp']
}

model = unpickle_object(os.path.join(MODEL_DIR, 'one_test_fixed.pkl'))
fit = sample_from_model(model, stan_data, n_burnin, n_samples, n_chains)
idata_1 = ar.from_pystan(fit)
del(model)

# run two test model
stan_data = {
    'N_0': data_0['N'],
    'x1_0': np.array(data_0['X']['vax']),
    'testResults_0': np.array(data_0['X']['test_result']),
    'se_0': data_0['se'],
    'sp_0': data_0['sp'], 

    'N_1': data_1['N'],
    'x1_1': np.array(data_1['X']['vax']),
    'testResults_1': np.array(data_1['X']['test_result']),
    'se_1': data_1['se'],
    'sp_1': data_1['sp']
}
model = unpickle_object(os.path.join(MODEL_DIR, 'two_test_fixed.pkl'))
fit = sample_from_model(model, stan_data, n_burnin, n_samples, n_chains)
idata_01 = ar.from_pystan(fit)

results = {
    'params': params,

    'data_0': data_0,
    'data_1': data_1,

    'idata_0': idata_0,
    'idata_1': idata_1,
    'idata_01': idata_01,
}

pickle_object(os.path.join(DATA_DIR,f'{NAME}.pkl'), results)


