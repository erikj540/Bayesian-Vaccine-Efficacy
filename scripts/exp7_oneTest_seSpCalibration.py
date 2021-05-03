import pystan
import arviz as ar
from scipy.special import expit, logit
import os

from utilities.utilityFunctions import unpickle_object, pickle_object
from BayesianVE.library import *

NAME = 'calibration'
DATA_DIR = '/Users/erjo3868/Bayesian-Vaccine-Efficacy/4local'
MODEL_DIR = '/Users/erjo3868/Bayesian-Vaccine-Efficacy/stan_models'
TEST = 0 # 1=test, 0=not test

model = unpickle_object(os.path.join(MODEL_DIR, 'calibration_study_one_test.pkl'))

if TEST==1: # testing
    N = 50
    n_burnin, n_samples, n_chains = 10, 100, 2
else: # not testing
    N = 10000
    n_burnin, n_samples, n_chains = 1000, 10000, 1

prev = 0.5
alpha = 0.5
beta0, beta1 = logit(prev), np.log(alpha)
ve = 1-alpha
se = 0.70
sp = 0.95
vax_prop = 0.5
n_spec, n_sens = 200, 200

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
    'n_chains': n_chains,
    'n_spec': n_spec,
    'n_sens': n_sens,
}

dataEngine = StudyData(vax_prop, beta0, beta1)
y_spec = dataEngine.generate_validation_data(n_spec, sp)
y_sens = dataEngine.generate_validation_data(n_sens, se)

data = dataEngine.generate_one_test_data(N, se, sp, 0)
stan_data = {
    'N': data['N'],
    'x1': np.array(data['X']['vax']),
    'testResults': np.array(data['X']['test_result']),
    'y_spec': y_spec,
    'n_spec': n_spec,
    'y_sens': y_sens,
    'n_sens': n_sens,
}

fit = sample_from_model(model, stan_data, n_burnin, n_samples, n_chains)
idata = ar.from_pystan(fit)
del(model)

results = {
    'params': params,
    'data': data,
    'stan_data': stan_data,
    'idata': idata,
}
NAME = NAME+f'_N{N}_prev{int(100*prev)}_alpha{int(100*alpha)}_se{int(se*100)}_sp{int(sp*100)}_nSpec{n_spec}_nSens{n_sens}_vaxProp{int(vax_prop*100)}'
pickle_object(os.path.join(DATA_DIR,f'{NAME}.pkl'), results)