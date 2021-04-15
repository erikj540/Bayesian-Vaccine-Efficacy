import os, glob
import numpy as np
from utilities.utilityFunctions import unpickle_object, pickle_object
from library import *

# names = ['exp1', 'exp3']
names = ['exp2']

##################################
# EXPERIMENT 1
if 'exp1' in names:
    name = 'exp1'
    print('Processing experiment 1 data')
    needed_files = [f'./data/{name}/{val}.pkl' for val in np.arange(0,200)]
    files = [f for f in glob.glob(f'./data/{name}/*.pkl') if f.split('/')[-1]!='model.pkl']

    missing_files = []
    for f in needed_files:
        if f not in files: missing_files.append(f)
    if len(missing_files)==0:
        print('No missing files. Yay!')
    else:
        print(f'{len(missing_files)} missing files:\n{missing_files}')

    ci_df = []
    true_params = {'beta0': 0.5, 'beta1': np.log(0.9)}
    for f in files:
        idata = unpickle_object(f)
        for param in ['beta0', 'beta1']:
            samples = idata.to_dataframe()[('posterior', f'{param}')]
            mean = samples.mean()
            interval, prob = compute_hdi(idata, param, prob=0.95)
            ci_df.append([param, true_params[param],
                        interval[0], interval[1],
                        prob
                        ])
            # print(interval, prob, mean)
        # break
    ci_df = pd.DataFrame(ci_df, columns=['param', 'true', 'lower', 'upper', 'prob'])
    ci_df.to_pickle(f'./data/{name}_ci_df.pkl')

##################################
# EXPERIMENT 2
if 'exp2' in names:
    name = 'exp2'
    print('Processing experiment 2 data')
    needed_files = [f'./data/{name}/{val}.pkl' for val in np.arange(0,200)]
    files = [f for f in glob.glob(f'./data/{name}/*.pkl') if f.split('/')[-1]!='model.pkl']

    missing_files = []
    for f in needed_files:
        if f not in files: missing_files.append(f)
    if len(missing_files)==0:
        print('No missing files. Yay!')
    else:
        print(f'{len(missing_files)} missing files:\n{missing_files}')

    ci_df = []
    true_params = {'se': 0.95, 'sp': 0.95, 'beta0': 0.5, 'beta1': np.log(0.9)}
    for f in files:
        idata = unpickle_object(f)
        for param in ['se', 'sp', 'beta0', 'beta1']:
            samples = idata.to_dataframe()[('posterior', f'{param}')]
            mean = samples.mean()
            interval, prob = compute_hdi(idata, param, prob=0.95)
            ci_df.append([param, true_params[param],
                        interval[0], interval[1],
                        prob
                        ])
            # print(interval, prob, mean)
        # break
    ci_df = pd.DataFrame(ci_df, columns=['param', 'true', 'lower', 'upper', 'prob'])
    ci_df.to_pickle(f'./data/{name}_ci_df.pkl')

##################################
# EXPERIMENT 3
if 'exp3' in names:
    name = 'exp3'
    print('Processing experiment 3 data')
    needed_files = [f'./data/{name}/{val}.pkl' for val in np.arange(0,200)]
    files = [f for f in glob.glob(f'./data/{name}/*.pkl') if f.split('/')[-1]!='model.pkl']

    missing_files = []
    for f in needed_files:
        if f not in files: missing_files.append(f)
    if len(missing_files)==0:
        print('No missing files. Yay!')
    else:
        print(f'{len(missing_files)} missing files:\n{missing_files}')

    ci_df = []
    for f in files:
        results = unpickle_object(f)
        true_params = results['true_params']
        idata = results['idata']
        for param in ['beta0', 'beta1']:
            samples = idata.to_dataframe()[('posterior', f'{param}')]
            mean = samples.mean()
            interval, prob = compute_hdi(idata, param, prob=0.95)
            ci_df.append([param, true_params[param],
                        interval[0], interval[1],
                        prob
                        ])
            # print(interval, prob, mean)
        # break
    ci_df = pd.DataFrame(ci_df, columns=['param', 'true', 'lower', 'upper', 'prob'])
    ci_df.to_pickle(f'./data/{name}_ci_df.pkl')