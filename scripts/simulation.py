import pystan
import arviz as ar
from scipy.special import expit, logit
import os, argparse

from utilities.utilityFunctions import unpickle_object, pickle_object
from BayesianVE.library import *

DATA_DIR = '/Users/erjo3868/Bayesian-Vaccine-Efficacy/results/allocating_validation_tests/sims'
# DATA_DIR = '/Users/erjo3868/Bayesian-Vaccine-Efficacy/results/tests'
MODEL_DIR = '/Users/erjo3868/Bayesian-Vaccine-Efficacy/stan_models'


def se_sp_validation_one_dx_test_simulation(params):
    if params['data'] is not None: # provided data
        data = unpickle_object(params['data'])
    else: # generated data
        N, vax_prob = params['N'], params['vax_prob']
        beta0, beta1 = params['beta0'], params['beta1']
        se, sp = params['se'], params['sp']
        data = SimulatedData(N, vax_prob, beta0, beta1, se, sp)
        data.generate_ve_study_data()
    
    data.create_stan_data_se_sp_validation_one_dx_test(params['n_sens'], params['n_spec'])

    return data

def se_sp_fixed_one_dx_test(params):
    """

    """
    print(params)
    if params['data'] is not None: # provided data
        data = unpickle_object(params['data'])
    else: # generated data
        N, vax_prob = params['N'], params['vax_prob']
        beta0, beta1 = params['beta0'], params['beta1']
        se, sp = params['se'], params['sp']
        data = SimulatedData(N, vax_prob, beta0, beta1, se, sp)
        data.generate_ve_study_data()

    data.create_stan_data_se_sp_fixed_one_dx_test(0.9, 0.9)

    return data

    

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-model_name', '--model_name',
        type=str,
        action='store',
        required=True)
    parser.add_argument('-name', '--name', 
        type=str,
        action='store', 
        required=True)
    parser.add_argument('-n_chains', '--n_chains', 
        type=int,
        action='store', 
        required=True)
    parser.add_argument('-n_burnin', '--n_burnin', 
        type=int,
        action='store',
        required=True)
    parser.add_argument('-n_samples', '--n_samples', 
        type=int,
        action='store', 
        required=True
    )
    parser.add_argument('-data', '--data',
        type=str,
        action='store', 
        required=False)
    parser.add_argument('-N', '--N',
        type=int,
        action='store', 
        required=False)
    parser.add_argument('-vax_prob', '--vax_prob', 
        type=float,
        action='store', 
        required=False)
    parser.add_argument('-prev', '--prev', 
        type=float,
        action='store',
        required=False)
    parser.add_argument('-alpha', '--alpha',
        type=float,
        action='store', 
        required=False)
    parser.add_argument('-se', '--se', 
        type=float,
        action='store', 
        required=False)
    parser.add_argument('-sp', '--sp', 
        type=float,
        action='store', 
        required=False)
    parser.add_argument('-n_sens',
        type=int,
        action='store',
        required=False)
    parser.add_argument('-n_spec',
        type=int,
        action='store',
        required=False)
    args = parser.parse_args()
    params = vars(args)

    if params['data'] is None:
        params['beta0'] = logit(params['prev'])
        params['beta1'] = np.log(params['alpha'])

    if params['model_name']=='calibration_study_one_test':
        data = se_sp_validation_one_dx_test_simulation(params)
    
    elif params['model_name']=='one_test_fixed':
        data = se_sp_fixed_one_dx_test(params)

    model = unpickle_object(os.path.join(MODEL_DIR, f"{params['model_name']}.pkl"))
    code = model.model_code
    fit = sample_from_model(model, data.stan_data, params['n_burnin'], params['n_samples'], params['n_chains'])
    idata = ar.from_pystan(fit)
    del(model)

    dict2save = {
        'params': params,
        'posterior': idata,
        'code': code,
        'data': data 
    }

    pickle_object(os.path.join(DATA_DIR, f"{params['name']}.pkl"), dict2save)