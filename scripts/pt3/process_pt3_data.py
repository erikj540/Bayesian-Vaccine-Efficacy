import pystan
import pandas as pd
import arviz as ar
import os, argparse, glob

from utilities.utilityFunctions import unpickle_object, pickle_object
from BayesianVE.library import *

DATA_DIR = '/Users/erjo3868/Bayesian-Vaccine-Efficacy/4local/pt3'

files = glob.glob(os.path.join(DATA_DIR,'*.pkl'))
df = []
# for f in files[:100]:
for f in files:
    res = unpickle_object(f)

    # compute VE point estimates
    eng = MCMCSamples(res['data']['X'], None, res['params'])
    eng.compute_test_result_summaries()
    eng.compute_corrected_point_estimates()
    eng.compute_uncorrected_point_estimates()

    # corrected HDPI
    interval, prob = compute_hdi(res['idata_corrected'], 'beta1')
    corrected_interval = [1-np.exp(val) for val in interval] # turn odds-ratio into VE
    corrected_interval.sort()

    # uncorrected HDPI
    interval, prob = compute_hdi(res['idata_uncorrected'], 'beta1')
    uncorrected_interval = [1-np.exp(val) for val in interval] # turn odds-ratio into VE
    uncorrected_interval.sort()

    # add row to dataframe
    df.append([
        res['params']['ve'],
        # res['params']['n_spec'],
        # res['params']['n_sens'],
        res['params']['se'],
        res['params']['sp'],
        res['params']['prev'],
        res['params']['vax_prop'],
        eng.corrected_ve_pt_estimate,
        eng.uncorrected_ve_pt_estimate,
        corrected_interval[0],
        corrected_interval[1],
        uncorrected_interval[0],
        uncorrected_interval[1],
        eng.num_unvax_testNeg,
        eng.num_unvax_testPos,
        eng.num_vax_testNeg,
        eng.num_vax_testPos
    ])
    # break

df = pd.DataFrame(
    df,
    columns=[
        've', 
        # 'n_spec', 
        # 'n_sens',
        'se', 
        'sp', 
        'prev',
        'vax_prob',
        'corrected_ve_pt',
        'uncorrected_ve_pt',
        'corrected_hdpi_lower',
        'corrected_hdpi_upper',
        'uncorrected_hdpi_lower',
        'uncorrected_hdpi_upper',
        'unvax_testNeg',
        'unvax_testPos',
        'vax_testNeg',
        'vax_testPos'
    ]
)

pickle_object('4local/pt3_df.pkl', df)