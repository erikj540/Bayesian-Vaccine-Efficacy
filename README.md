# Bayesian-Vaccine-Efficacy

## Create Stan Model
The possible Stan priors include `normal(mu,sd)`, `gamma(a,b)`, `beta(a,b)`, `fixed(val)`, etc. The following command compiles a Stan model with the supplied posteriors and path2save.

`python create_stan_model.py --beta0="<prior>" --beta1=="<prior>"  --se=="<prior>"  --sp=="<prior>"  --savepath=="<path>"`

## Sampling From a Model
Most often running/sampling from a Stan model involves three steps/commands: (1) load the model, (2) create/supply data, (3) posterior sampling via MCMC.
```
model = unpickle_object(os.path.join(DATA_DIR, 'model.pkl')) # load model  
data = create_vax_data(N, vax_prob, beta0, beta1, se, sp) # generate data
fit = sample_from_model(model, data, n_burnin, n_samples, n_chains) # sample from model
```

