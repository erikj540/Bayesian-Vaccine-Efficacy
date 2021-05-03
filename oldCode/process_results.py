import os, glob
import numpy as np
from utilities.utilityFunctions import unpickle_object, pickle_object
from library import *

# names = ['exp1', 'exp3']
# names = ['exp2']
names = ['exp4']

##################################
# EXPERIMENT 1
if 'exp1' in names:
    name = '2exp1'
    print(f'Processing {name} data')
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
    params = ['beta0', 'beta1']
    for f in files:
        results = unpickle_object(f)
        idata = results['idata']
        true_params = results['true_params']
        for param in params:
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
    name = '2exp2'
    print(f'Processing {name} data')
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
    params = ['beta0', 'beta1', 'se', 'sp']
    for f in files:
        results = unpickle_object(f)
        idata = results['idata']
        true_params = results['true_params']
        for param in params:
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
    name = '2exp3'
    print(f'Processing {name} data')
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
    params = ['beta0', 'beta1']
    for f in files:
        results = unpickle_object(f)
        idata = results['idata']
        true_params = results['true_params']
        for param in params:
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
if 'exp4' in names:
    name = '2exp4'
    print(f'Processing {name} data')
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
    params = ['beta0', 'beta1', 'se', 'sp']
    for f in files:
        results = unpickle_object(f)
        idata = results['idata']
        true_params = results['true_params']
        for param in params:
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