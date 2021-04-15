# Bayesian-Vaccine-Efficacy

## Create Stan model
The possible Stan priors include `normal(mu,sd)`, `gamma(a,b)`, `beta(a,b)`, `fixed(val)`, etc. The following command compiles a Stan model with the supplied posteriors and path2save.

`python create_stan_model.py --beta0="<prior>" --beta1=="<prior>"  --se=="<prior>"  --sp=="<prior>"  --savepath=="<path>"`

## Sampling from Stan model
Most often running/sampling from a Stan model involves three steps/commands: (1) load the model, (2) create/supply data, (3) posterior sampling via MCMC.
```
model = unpickle_object(os.path.join(DATA_DIR, 'model.pkl')) # load model  
data = create_vax_data(N, vax_prob, beta0, beta1, se, sp) # generate data
fit = sample_from_model(model, data, n_burnin, n_samples, n_chains) # sample from model
```

## Processing sampling data
Import required functons with `from library import *`. Then
- Posterior plot: `posterior_plot(idata, param, true_val)`
- Prior: `pdf = generate_prior(stan_prior)`
- Credible intervals: given `idata` and parameter name `param`
```
param = ... # e.g., 'beta0', 'beta1', 'se', 'sp'
samples = idata.to_dataframe()[('posterior', f'{param}')]

# credible intervals
interval, prob = compute_centered_credible_interval(samples, val, step, thresh=0.95)
# or
interval, prob = compute_hdi(idata, param, prob=0.95)
# or 
interval, prob = compute_lower_credible_interval(samples, step, thresh=0.95)
# or 
interval, prob = compute_upper_credible_interval(samples, step, thresh=0.95)
```

## Experiments
### Experiment 1
Consistency for fixed and known se and sp. And fixed but unknown beta0 and beta1. 
`NAME="exp1" && python create_stan_model.py --beta0='normal(0,1)' --beta1='gamma(2,4)' --se='fixed(0.95)' --sp='fixed(0.95)' --savepath='/Users/erjo3868/Bayesian-Vaccine-Efficacy/data/${NAME}/model.pkl'`

`NAME="exp1" && DIR="/Users/erjo3868/Bayesian-Vaccine-Efficacy/output/" && sbatch --job-name=${NAME} --output=${DIR}${NAME}.out --error=${DIR}${NAME}.err --export=NAME=${NAME} sbatch_launcher.sbatch`

### Experiment 2
Consistency for fixed but unknown se and sp. And fixed but unknown beta0 and beta1. 
`NAME="exp2" && python create_stan_model.py --beta0='normal(0,1)' --beta1='gamma(2,4)' --se='beta(4,2)' --sp='beta(4,2)' --savepath='/Users/erjo3868/Bayesian-Vaccine-Efficacy/data/${NAME}/model.pkl'`

`NAME="exp2" && DIR="/Users/erjo3868/Bayesian-Vaccine-Efficacy/output/" && sbatch --job-name=${NAME} --output=${DIR}${NAME}.out --error=${DIR}${NAME}.err --export=NAME=${NAME} sbatch_launcher.sbatch`

### Experiment 3
Consistency for fixed and known se and sp. And unknown beta0 and beta1, i.e., they come from their priors.
`NAME="exp3" && python create_stan_model.py --beta0='normal(0,1)' --beta1='gamma(2,4)' --se='fixed(0.95)' --sp='fixed(0.95)' --savepath=/Users/erjo3868/Bayesian-Vaccine-Efficacy/data/${NAME}/model.pkl`

`NAME="exp3" && DIR="/Users/erjo3868/Bayesian-Vaccine-Efficacy/output/" && sbatch --job-name=${NAME} --output=${DIR}${NAME}.out --error=${DIR}${NAME}.err --export=NAME=${NAME} sbatch_launcher.sbatch`

### Experiment 4
Consistency for unknown beta0, beta1, se, and sp, i.e., they come from their priors.
`NAME="exp4" && python create_stan_model.py --beta0='normal(0,1)' --beta1='gamma(2,4)' --se='beta(10,2)' --sp='beta(10,2)' --savepath='/Users/erjo3868/Bayesian-Vaccine-Efficacy/data/${NAME}/model.pkl'`

`NAME="exp4" && DIR="/Users/erjo3868/Bayesian-Vaccine-Efficacy/output/" && sbatch --job-name=${NAME} --output=${DIR}${NAME}.out --error=${DIR}${NAME}.err --export=NAME=${NAME} sbatch_launcher.sbatch`

## Next steps
- (4/14) 
- (4/14)