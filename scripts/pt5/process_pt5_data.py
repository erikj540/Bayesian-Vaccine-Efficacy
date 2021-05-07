import pystan
import pandas as pd
import arviz as ar
from scipy.special import expit, logit
import os, argparse, glob

from utilities.utilityFunctions import unpickle_object, pickle_object
from BayesianVE.library import *

DATA_DIR = '/Users/erjo3868/Bayesian-Vaccine-Efficacy/4local/pt5_2'

files = glob.glob(os.path.join(DATA_DIR,'*.pkl'))
df = []
# for f in files[:100]:
for f in files:
    res = unpickle_object(f)
    interval, prob = compute_hdi(res['idata'], 'beta1')
    interval = [1-np.exp(val) for val in interval] # turn odds-ratio into VE
    interval.sort()
    df.append([
        res['params']['ve'],
        res['params']['n_spec'],
        res['params']['n_sens'],
        res['params']['n_spec']/(res['params']['n_spec']+res['params']['n_sens']),
        interval[0],
        interval[1],
    ])
    # break

df = pd.DataFrame(
    df,
    columns=[
        've', 
        'n_spec', 
        'n_sens', 
        'prop_se', 
        'lower_hdi_bound', 
        'higher_hdi_bound'
    ]
)

pickle_object('4local/pt5_2_df.pkl', df)