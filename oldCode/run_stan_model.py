import pystan
import arviz as ar
from scipy.special import expit, logit
from scipy.stats import bernoulli, uniform, norm, beta, gamma
from utilities.utilityFunctions import unpickle_object, pickle_object
from library import create_vax_data, sample_from_model, get_command_line_arguments, sample_from_prior, StudyData
import os

DATA_DIR = '/Users/erjo3868/Bayesian-Vaccine-Efficacy/model_output'
MODEL_DIR = '/Users/erjo3868/Bayesian-Vaccine-Efficacy/stan_models'

one_test_model = unpickle_object(os.path.join(MODEL_DIR,'one_test_fixed.pkl'))
two_test_model = unpickle_object(os.path.join(MODEL_DIR,'two_test_fixed.pkl'))

N_0 = 10000
N_1 = 10000
prev = 0.2
alpha = 0.1
ve = 1-alpha
se_0 = 0.99
sp_0 = 0.99
se_1 = 0.89
sp_1 = 0.99
beta0, beta1 = logit(true_prev), np.log(alpha)
vax_prop = 0.5

params = {
    'prev': prev,
    'alpha': alpha,
    've': ve

}

data = StudyData(vax_prop, beta0, beta1)

test0_data = data.create_one_test_data(N_0, se_0, sp_0, 0)
test1_data = data.create_one_test_data(N_1, se_1, sp_1, 1)

N_test0 = X[X['test_id']==0].shape[0]
N_test1 = X[X['test_id']==1].shape[0]

x1_test0 = np.array(X[X['test_id']==0]['vax'])
x1_test1 = np.array(X[X['test_id']==1]['vax'])

test0_results = np.array(X[X['test_id']==0]['prob_td'].apply(lambda p: bernoulli.rvs(true_se0*p + (1-true_sp0)*(1-p))))
test1_results = np.array(X[X['test_id']==1]['prob_td'].apply(lambda p: bernoulli.rvs(true_se1*p + (1-true_sp1)*(1-p))))

sample_from_model(model, data, 1000, 3000, 3)

def main(params):
    vax_prob, n_burnin, n_samples, n_chains = 0.5, 1000, 5000, 3
    vax_prob, n_burnin, n_samples, n_chains = 0.5, 10, 100, 2 # for testing

    beta0 = sample_from_prior(params['beta0'])
    beta1 = (-1)*sample_from_prior(params['beta1'])
    se = sample_from_prior(params['se'])
    sp = sample_from_prior(params['sp'])
    true_params = {'beta0': beta0, 
                'beta1': beta1, 
                'se': se, 
                'sp': sp
                }

    model = unpickle_object(params['model'])
    data = create_vax_data(int(params['N']), vax_prob, beta0, beta1, se, sp)
    fit = sample_from_model(model, data, n_burnin, n_samples, n_chains)
    idata = ar.from_pystan(fit)

    rand_int = np.random.randint(0, 100000)
    out_path = os.path.join(DATA_DIR, f'{rand_int}.pkl')
    while os.path.exists(out_path):
        rand_int = np.random.randint(0, 100000)
        out_path = os.path.join(DATA_DIR, f'{rand_int}.pkl')

    results = {
        'true_params': true_params, 
        'data': data, 
        'idata': idata
        }
    pickle_object(outpath, results)


if __name__=="__main__":
    needed_params = ['model', 'N', 
                    'beta0', 'beta1', 'se', 'sp'
                    ]
    params = get_command_line_arguments()
    for param in needed_params:
        assert param in params, '{} not in params and is required'.format(param)
    print(f'params = {params}')

