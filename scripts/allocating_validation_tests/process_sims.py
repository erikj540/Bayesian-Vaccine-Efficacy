import pystan
import pandas as pd
import arviz as ar
from scipy.special import expit, logit
import os, argparse, glob

from utilities.utilityFunctions import unpickle_object, pickle_object
from BayesianVE.library import *

DATA_DIR = '/Users/erjo3868/Bayesian-Vaccine-Efficacy/results/allocating_validation_tests/sims'
SAVE_DIR = '/Users/erjo3868/Bayesian-Vaccine-Efficacy/results/allocating_validation_tests'
hdpi_prob = 0.95

files = glob.glob(os.path.join(DATA_DIR,'*.pkl'))

df = []
for ii, f in enumerate(files):
    pickled_dict = unpickle_object(f)
    colms, vals = [], []
    for key, val in pickled_dict['params'].items():
        colms.append(key)
        vals.append(val)
    colms.append(key)
    vals.append(pickled_dict['code'])

    # colms.append('posterior_samples')
    # vals.append(pickled_dict['posterior'])


    colms.append(f'{int(100*hdpi_prob)}_hdpi')
    vals.append(compute_hdi(pickled_dict['posterior'], 'beta1', hdpi_prob))
    # if ii>2: break
# print(colms)
# print(vals)
#     interval, prob = compute_hdi(res['idata'], 'beta1')
#     interval = [1-np.exp(val) for val in interval] # turn odds-ratio into VE
#     interval.sort()
#     df.append([
#         res['params']['ve'],
#         res['params']['n_spec'],
#         res['params']['n_sens'],
#         res['params']['n_spec']/(res['params']['n_spec']+res['params']['n_sens']),
#         interval[0],
#         interval[1],
#     ])
#     # break

df = pd.DataFrame(
    df,
    columns=colms,
)

pickle_object(os.path.join(SAVE_DIR, 'df.pkl'), df)