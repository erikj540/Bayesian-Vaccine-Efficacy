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
    print(f'iter = {ii}')
    if f.find('iter')!=-1:
        pickled_dict = unpickle_object(f)
        colms, vals = [], []
        for key, val in pickled_dict['params'].items():
            colms.append(key)
            vals.append(val)
        colms.append('code')
        vals.append(pickled_dict['code'])

        # colms.append('posterior_samples')
        # vals.append(pickled_dict['posterior'])


        # colms.append(f'{int(100*hdpi_prob)}_hdpi')
        interval, prob = compute_hdi(pickled_dict['posterior'], 'beta1', hdpi_prob)
        interval = [1-np.exp(val) for val in interval] # turn odds-ratio into VE
        interval.sort()
        
        colms.append(f'{int(100*hdpi_prob)}_hdpi_lower')
        vals.append(interval[0])
        colms.append(f'{int(100*hdpi_prob)}_hdpi_upper')
        vals.append(interval[1])
        colms.append(f'{int(100*hdpi_prob)}_hdpi_prob')
        vals.append(prob)
        df.append(vals)

df = pd.DataFrame(
    df,
    columns=colms,
)

# print(df.head(2))

pickle_object(os.path.join(SAVE_DIR, 'df_averaged.pkl'), df)