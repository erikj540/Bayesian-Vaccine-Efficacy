# Bayesian-Vaccine-Efficacy

## Simulation
The simulation framework takes a dictionary. The dictionary MUST have five required keys: 
1. `model_name` which is name of pickled STAN model assumed to be in `MODEL_DIR`
1. `n_burnin` which is number of burn in samples
1. `n_samples` which is number of (approximate) posterior samples to draw
1. `n_chains` which is number of Monte Carol chains to use
1. `name`. In path `DATA_DIR/<name>.pkl`, saves a dictionary  dictionary containing the params (key=`params`), posterior samples (key=`idata`), the STAN code (key=`code`) (in particular, so one can verify the priors that were used), and the `SimulationData` data (key=`data`).

The dictionary MUST have additional keys and for those keys there are two options. **Option 1** is to pass a `SimulationData` object via key `data` if, for instance, you  are using the same data for many simulations. **Option 2** is to pass several keys that are used generate a `SimulationData` object. The keys are `N`, `vax_prob`, `beta0` (`beta0 = logit(prev)`), `beta1` (`beta1=log(alpha)`), `se`, and `sp`.

The simulation framework can be called from the command line via
```
# option 1
python scripts/test.py -model_name= -n_burnin= -n_samples= -n_chains= -name= -data=

# option 2
python scipts/test.py -model_name= -n_burnin= -n_samples= -n_chains= -name= -N= -prev= -alpha= -se= -sp= -vax_prob=
```

# STAN models
- `one_test_fixed`: fixed se and sp. The input data has `N`, `x1` (=vaccination status), `testResults`, `se`, and `sp`. 
- `calibration_study_one_test`: is for a calibration study. The input data has `N`, `x1`, `testResults`, `y_spec`, `n_spec`, `y_sens`, `n_sens`. 


## Create Stan model
### Option 1
The possible Stan priors include `normal(mu,sd)`, `gamma(a,b)`, `beta(a,b)`, `fixed(val)`, etc. The following command compiles a Stan model with the supplied posteriors and path2save.

`python create_stan_model.py --beta0="<prior>" --beta1=="<prior>"  --se=="<prior>"  --sp=="<prior>"  --savepath=="<path>"`

### Option 2
Save STAN model code in `stan_models` directory as `<name>.stan`. Then run 
```
python scripts/compile_stan_model.py --name=<name>
```
This will compile the STAN model and save it in the same `stan_models` directory as `<name>.pkl`.

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
- Centered credible intervals plot: centered_credible_interval_plot(ax, ci_df)
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


## Processing the MCMC sampling data
- **Credible intervals**: *ALL* return a 2-tuple, `interval`, with the CI bounds (`interval=[<lower>, <upper>]`) and the proportion, `prop`, of samples that are contained in the interval. If you don't supply the `prob` in the CI functions, the default is 0.95. To get the `samples` argument for the non-HDI CIs from `idata` and `param`, do `samples = idata.to_dataframe()[("posterior", f"{param}")]`
    - HDI: `compute_hdi(idata, param, prob=0.95)`
    - Centered CI: `compute_centered_credible_interval(samples, val, step, prob=0.95)`
    - Upper CI: `compute_upper_credible_interval(samples, step, prob=0.95)`
    - Lower CI: `compute_lower_credible_interval(samples, step, prob=0.95)`  

## Next steps
- (4/14) 
- (4/14)