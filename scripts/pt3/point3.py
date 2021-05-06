import pystan
import arviz as ar
from scipy.special import expit, logit
import os, argparse

from utilities.utilityFunctions import unpickle_object, pickle_object
from BayesianVE.library import *

# NAME = 'point3'
DATA_DIR = '/Users/erjo3868/Bayesian-Vaccine-Efficacy/4local/pt3'
MODEL_DIR = '/Users/erjo3868/Bayesian-Vaccine-Efficacy/stan_models'
MODEL_PATH = os.path.join(MODEL_DIR, 'one_test_fixed.pkl')
TEST = 0 # 1=test, 0=not test

# set parameters
if TEST==1: # testing
    N_BURNIN, N_SAMPLES, N_CHAINS = 10, 100, 2
else: # not testing
    N_BURNIN, N_SAMPLES, N_CHAINS = 1000, 10000, 1

def fixed_se_sp(prev, alpha, se, sp, vax_prop, N, model_path, name):
    ve, beta0, beta1 = 1-alpha, logit(prev), np.log(alpha)
    # name = name + f'_N{N}_prev{int(100*prev)}_alpha{int(100*alpha)}_se{int(se*100)}_sp{int(sp*100)}_vaxProp{int(vax_prop*100)}'

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
            'n_chains': N_CHAINS
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
        model = unpickle_object(model_path)
        fit = sample_from_model(model, stan_data, N_BURNIN, N_SAMPLES, N_CHAINS)
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
        model = unpickle_object(model_path)
        fit = sample_from_model(model, stan_data, N_BURNIN, N_SAMPLES, N_CHAINS)
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

        pickle_object(os.path.join(DATA_DIR,f'{name}.pkl'), results)

# prev, alpha, se, sp, vax_prop = 0.1, 0.5, 0.8, 0.9, 0.5
# fixed_se_sp(prev, alpha, se, sp, vax_prop, N, MODEL_PATH)
# if __name__=="__main__":
#     parser = argparse.ArgumentParser()
#     parser.add_argument('--prev', action='store', type=float, required=True)
#     parser.add_argument('--alpha', action='store', type=float, required=True)
#     parser.add_argument('--se', action='store', type=float, required=True)
#     parser.add_argument('--sp', action='store', type=float, required=True)
#     parser.add_argument('--vax_prop', action='store', type=float, required=True)
#     parser.add_argument('--N', action='store', type=int, required=True)
#     parser.add_argument('--name', action='store', type=str, required=True)

#     args = parser.parse_args()

#     fixed_se_sp(
#         args.prev, args.alpha, args.se, args.sp,
#         args.vax_prop, args.N, MODEL_PATH, args.name
#     )

# n_sims = 2

# for ii in range(n_sims):
#     prev = np.random.uniform(0.1, 0.9)
#     alpha = np.random.uniform(0, 0.5)
#     se = np.random.uniform(0.6, 1)
#     sp = np.random.uniform(0.6, 1)
#     vax_prob = 0.5
#     N = 5000

#     name = f'pt3_{ii}'
#     fixed_se_sp(
#         prev, alpha, se, sp, 
#         vax_prob, N, MODEL_PATH, name
#     )

# prevs = [0.1, 0.5, 0.9]
# alphas = [0.01, 0.5, 0.9]
# Ns = [5000]
# ses = [0.6, 0.8, 1]
# sps = [0.6, 0.8, 1]
# vax_props = [0.1, 0.5, 0.9]

# for prev in prevs:
#     for alpha in alphas:
#         for N in Ns:
#             for se in ses:
#                 for sp in sps:
#                     for vax_prop in vax_props:
#                         fixed_se_sp(
#                             prev, alpha, se, sp,
#                             vax_prop, N, MODEL_PATH, name
#                         )


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--i', action='store', type=int, required=True)
    args = parser.parse_args()

    prev = np.random.uniform(0.1, 0.9)
    alpha = np.random.uniform(0, 0.5)
    se = np.random.uniform(0.6, 1)
    sp = np.random.uniform(0.6, 1)
    vax_prop = 0.5
    N = 5000

    name = f'pt3_{args.i}'
    fixed_se_sp(
        prev, alpha, se, sp, 
        vax_prop, N, MODEL_PATH, name
    )