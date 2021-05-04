import pystan
import arviz as ar
from scipy.special import expit, logit
import os, argparse

from utilities.utilityFunctions import unpickle_object, pickle_object
from BayesianVE.library import *

DATA_DIR = '/Users/erjo3868/Bayesian-Vaccine-Efficacy/4local'
MODEL_DIR = '/Users/erjo3868/Bayesian-Vaccine-Efficacy/stan_models'
MODEL_PATH = os.path.join(MODEL_DIR, 'calibration_study_one_test.pkl')
TEST = 0 # 1=test, 0=not test

# set parameters
if TEST==1: # testing
    N_BURNIN, N_SAMPLES, N_CHAINS = 10, 100, 2
else: # not testing
    N_BURNIN, N_SAMPLES, N_CHAINS = 1000, 10000, 1

def validation_ve_study(prev, alpha, se, sp, vax_prop, N, n_sens, n_spec, model_path, name):
    ve, beta0, beta1 = 1-alpha, logit(prev), np.log(alpha)
    name = name + f'_N{N}_prev{int(100*prev)}_alpha{int(100*alpha)}_se{int(se*100)}_sp{int(sp*100)}_nSpec{n_spec}_nSens{n_sens}_vaxProp{int(vax_prop*100)}'

    if os.path.exists(os.path.join(DATA_DIR,f'{name}.pkl')):
        print(f'File already exists! {name}')
    else:
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
            'n_burnin': N_BURNIN,
            'n_samples': N_SAMPLES,
            'n_chains': N_CHAINS,
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
        model = unpickle_object(model_path)
        fit = sample_from_model(model, stan_data, N_BURNIN, N_SAMPLES, N_CHAINS)
        idata = ar.from_pystan(fit)
        del(model)

        results = {
            'params': params,
            'data': data,
            'stan_data': stan_data,
            'idata': idata,
        }
        pickle_object(os.path.join(DATA_DIR,f'{name}.pkl'), results)

prevs = [0.5]
alphas = [0.5]
Ns = [5000]
ses = [0.7]
sps = [0.9]
vax_props = [0.5]
num_validation_tests = 500
sp_proportions = np.linspace(0, 1, 21)
name = 'point5_2'

for prev in prevs:
    for alpha in alphas:
        for N in Ns:
            for se in ses:
                for sp in sps:
                    for vax_prop in vax_props:
                        for prop in sp_proportions:
                            n_spec = int(prop*num_validation_tests)
                            n_sens = num_validation_tests - n_spec
                            # np.random.seed(23)
                            validation_ve_study(
                                prev, alpha, se, sp, 
                                vax_prop, N, n_sens, n_spec, 
                                MODEL_PATH, name
                            )
