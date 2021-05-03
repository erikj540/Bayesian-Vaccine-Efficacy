import arviz as ar
from utilities.utilityFunctions import unpickle_object, pickle_object
from library import create_vax_data, sample_from_model, get_command_line_arguments, sample_from_prior

needed_params = ['model', 'N', 'outpath', 
                 'beta0', 'beta1', 'se', 'sp'
                ]
params = get_command_line_arguments()
for param in needed_params:
    assert param in params, '{} not in params'.format(param)
print(f'params = {params}')

vax_prob, n_burnin, n_samples, n_chains = 0.5, 1000, 5000, 3
# vax_prob, n_burnin, n_samples, n_chains = 0.5, 10, 100, 2 # for testing

beta0 = sample_from_prior(params['beta0'])
beta1 = (-1)*sample_from_prior(params['beta1'])
se = sample_from_prior(params['se'])
sp = sample_from_prior(params['sp'])
true_params = {'beta0': beta0, 
               'beta1': beta1, 
               'se': se, 
               'sp': sp
               }
print(f'true_parms = {true_params}')

model = unpickle_object(params['model'])
data = create_vax_data(int(params['N']), vax_prob, beta0, beta1, se, sp)
fit = sample_from_model(model, data, n_burnin, n_samples, n_chains)
idata = ar.from_pystan(fit)

results = {'true_params': true_params, 
           'data': data, 
           'idata': idata}
pickle_object(params['outpath'], results)
