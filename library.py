import numpy as np
import pandas as pd
import pickle
import pystan as ps
from scipy.stats import bernoulli, uniform, norm, beta, gamma
from scipy.special import expit
import arviz as ar
import sys

def create_model_code(priors):
    """

    """
    data_block = 'data {{\nint<lower=0> N;\nint<lower=0,upper=1> y[N];\nint<lower=0,upper=1> x1[N];\n}}\n'
    transformed_data_block = 'transformed data {{}}\n'
    transformed_parameters_block  = 'transformed parameters {{\nreal<upper=0> beta1;\nbeta1 = -1*beta1_pos;\n}}\n'
    generated_quantities_block = 'generated quantities {{}}\n'
    if priors['se'].split('(')[0]=='fixed':
        se = float(priors['se'].split('(')[1].split(')')[0])
        if priors['sp'].split('(')[0]=='fixed': # se_prior=='fixed*' & sp_prior=='fixed*'
            sp = float(priors['sp'].split('(')[1].split(')')[0])
            parameters_block = 'parameters {{\nreal beta0;\nreal<lower=0> beta1_pos;\n}}\n'
            model_block = 'model {{\nbeta0 ~ {0};\nbeta1_pos ~ {1};\nfor(i in 1:N) {{\nreal p;\nreal se;\nreal sp;\nse = {2};\nsp = {3};\np = inv_logit(beta0 + beta1*x1[i]);\ny[i] ~ bernoulli(se*p + (1-sp)*(1-p));\n}}\n}}\n'.format(priors['beta0'], priors['beta1'], se, sp)
        else: # se_prior=='fixed*' & sp_prior!='fixed*' 
            parameters_block = 'parameters {{\nreal beta0;\nreal<lower=0> beta1_pos;\nreal<lower=0,upper=1> sp;\n}}\n'
            model_block = 'model {{\nbeta0 ~ {0};\nbeta1_pos ~ {1};\nsp ~ {2};\nfor(i in 1:N) {{\nreal p;\nreal se;\nse = {3};\np = inv_logit(beta0 + beta1*x1[i]);\ny[i] ~ bernoulli(se*p + (1-sp)*(1-p));\n}}\n}}\n'.format(priors['beta0'], priors['beta1'], priors['sp'], se)
    else: 
        if priors['sp'].split('(')[0]=='fixed': # se_prior!='fixed*' & sp_prior=='fixed*' 
            sp = float(priors['sp'].split('(')[1].split(')')[0])
            parameters_block = 'parameters {{\nreal beta0;\nreal<lower=0> beta1_pos;\nreal<lower=0,upper=1> se;\n}}\n'
            model_block = 'model {{\nbeta0 ~ {0};\nbeta1_pos ~ {1};\nse ~ {2}\nfor(i in 1:N) {{\nreal p;\nreal sp;\nsp = {3};\np = inv_logit(beta0 + beta1*x1[i]);\ny[i] ~ bernoulli(se*p + (1-sp)*(1-p));\n}}\n}}\n'.format(priors['beta0'], priors['beta1'], priors['se'], sp)
        else: # se_prior!='fixed*' & sp_prior!='fixed*' 
            parameters_block = 'parameters {{\nreal beta0;\nreal<lower=0> beta1_pos;\nreal<lower=0,upper=1> se;\nreal<lower=0,upper=1> sp;\n}}\n'
            model_block = 'model {{\nbeta0 ~ {0};\nbeta1_pos ~ {1};\nse ~ {2};\nsp ~ {3};\nfor(i in 1:N) {{\nreal p;\np = inv_logit(beta0 + beta1*x1[i]);\ny[i] ~ bernoulli(se*p + (1-sp)*(1-p));\n}}\n}}\n'.format(priors['beta0'], priors['beta1'], priors['se'], priors['sp'])
    
    model_code = data_block + transformed_data_block + parameters_block + transformed_parameters_block + model_block +  generated_quantities_block
    model_code = model_code.replace('{{','{').replace('}}','}')
    
    return model_code

def create_stan_model(code):
    model = ps.StanModel(model_code=code)
    return model

def save_stan_model(model, save_path):
    with open(save_path, 'wb') as f:
        pickle.dump(model, f, protocol=pickle.HIGHEST_PROTOCOL)

def sample_from_model(model, data, n_burnin, n_samples, n_chains):
    fit = model.sampling(data=data, iter=n_samples+n_burnin, chains=n_chains, warmup=n_burnin)
    return fit

def create_vax_data(N, vax_prob, beta0, beta1, se, sp, seed=None):
    if seed is not None:
        np.random.seed(seed)
    x1 = bernoulli.rvs(vax_prob, size=N) # vaccinated (1)/unvaccinated (0)
    X = pd.DataFrame({
        'vax': x1,
        })
    beta_vec = np.array([beta0, beta1])
    X['prob_TD'] = X.apply(lambda row: expit(np.dot(np.array([1, row['vax']]), beta_vec)), axis=1)
    X['test_TD'] = X['prob_TD'].apply(lambda x: bernoulli.rvs(se*x + (1-sp)*(1-x)))
    y = X['test_TD']

    data = dict(
        x1=x1,
        y=y,
        N=N
    )
    return data

def plot_centered_error_bars(ax, x, y, true_y, lower, upper, label=None):
    ax.errorbar(x, y-true_y, yerr=(y-lower, upper-y), fmt='o', label=label) # error is (lower, upper) = (mean-lower, upper-mean)
    return ax

# def get_command_line_arguments(args):
def get_command_line_arguments():
    """
    Get command line arguments. Generally 
    """
    args = sys.argv
    args = args[1:]
    argument_dict = {}
    for arg in args:
        name = arg.split('=')[0][2:]
        val = arg.split('=')[1]
        argument_dict[name] = val
    return argument_dict

def compute_hdi(idata, param, prob=0.95):
    hdi = ar.hdi(idata, hdi_prob=prob).to_dataframe()
    interval = [hdi[param][0], hdi[param][1]]
    
    x = idata.to_dataframe()[('posterior', f'{param}')]
    prob = np.sum((x>=interval[0]) & (x<=interval[1]))/len(x)
    return (interval, prob)

def compute_credible_interval(idata, param):
    nbins = 1000
    x = idata.to_dataframe()[('posterior', f'{param}')]
    fig, axs = fig_setup(1,1)
    n, bins, patches = axs[0].hist(x, bins=nbins)

def compute_centered_credible_interval(samples, val, step, thresh=0.95):
    prob = 0
    ii = 1
    while prob<thresh:
        interval = [val-ii*step, val+ii*step]
        prob = compute_probability_of_interval(samples, interval)
        ii += 1
    return (interval, prob)

def compute_lower_credible_interval(samples, step, thresh=0.95):
    prob = 0
    ii = 1
    min_val = samples.min()
    while prob<thresh:
        interval = [min_val, val+ii*step]
        prob = compute_probability_of_interval(samples, interval)
        ii += 1
    return (interval, prob)

def compute_upper_credible_interval(samples, step, thresh=0.95):
    prob = 0
    ii = 1
    max_val = samples.max()
    while prob<thresh:
        interval = [val-ii*step, max_val]
        prob = compute_probability_of_interval(samples, interval)
        ii += 1
    return (interval, prob)

def compute_probability_of_interval(samples, interval):
    samples = samples.sort_values().reset_index(drop=True)
    mask = ((samples>=interval[0]) & (samples<=interval[1]))
    return np.sum(mask)/len(x)

def hdi_from_models(list_of_models, param):
    ci_df = []
    for model in list_of_models:
        idata = ar.from_pystan(model.fit)
        interval, prob = compute_hdi(idata, param) # change this line if you want a different CI
        true = model.true_params[param]
        ci_df.append([param, true, interval[0], interval[1], interval[1]-interval[0], prob])

    ci_df = pd.DataFrame(ci_df, \
                        columns=['param','true','lower','upper','width','prob'] 
                        )
    return ci_df

def centered_credible_interval_plot(ax, ci_df):
    """
    
    """
    true, lower, upper = ci_df['true'], ci_df['lower'], ci_df['upper']
    index = np.arange(1,len(lower)+1)
    for ii in range(len(index)):
        tt=ax.vlines(index[ii],
                      ymin=lower[ii]-true[ii],
                      ymax=upper[ii]-true[ii],
                      color='r',
                      lw=2,
                      ls='-',
#                       label=f'{true[ii]}'
                     )

    tt=ax.axhline(0,
                   color='k',
                   ls='--'
                  )
    # return ax

def generate_prior(stan_prior):
    size = 1000
    name = stan_prior.split('(')[0]
    param1, param2 = float(stan_prior.split('(')[1].split(',')[0]), float(stan_prior.split('(')[1].split(',')[1][:-1])
    if name=='normal':
        ppf = lambda xx: norm.ppf(xx, loc=param1, scale=param2)
        pdf = lambda xx: norm.pdf(xx, loc=param1, scale=param2)
    elif name=='beta':
        ppf = lambda xx: beta.ppf(xx, a=param1, b=param2)
        pdf = lambda xx: beta.pdf(xx, a=param1, b=param2)
    elif name=='gamma':
        ppf = lambda xx: gamma.ppf(xx, a=param1, scale=1/param2)
        pdf = lambda xx: gamma.pdf(xx, a=param1, scale=1/param2)
    elif name=='uniform': 
        ppf = lambda xx: gamma.ppf(xx, a=param1, scale=param2-param1)
        pdf = lambda xx: gamma.pdf(xx, a=param1, scale=param2-param1)
        
    prior = np.zeros((size, 2))
    prior[:,0] = np.linspace(ppf(low), ppf(up), size)
    prior[:,1] = pdf(prior[:,0])
    
    return prior

# def posterior_plot(model, param):
def posterior_plot(idata, param, true_val):

    """
    
    """
    fig, axs = fig_setup(1,1)

    # true value as vertical line
    # true = model.true_params[param]
    tt=axs[0].axvline(x=true_val, color='k', linestyle='--',
                label=f"true {param}={true}"
                ) #

    # prior
    # idata = ar.from_pystan(model.fit)
    x = idata.to_dataframe()[('posterior', f'{param}')]
    name = model.priors[param]
    prior = generate_prior(name)
    tt=axs[0].plot(prior[:,0], prior[:,1], 
                lw=3, 
                color='r', 
                label=f'prior {name}'
                )

    # posterior samples
    nbins = 100
    n, bins, patches =axs[0].hist(x,
                        bins=nbins,
                        density=True,
                        label='posterior samples',
    #                      label=f'{param}'
                        )

    # credible intervals
    # HDI
    interval = compute_hdi(idata, param)
    prob = np.sum((x>=interval[0]) & (x<=interval[1]))/len(x)
    tt=axs[0].hlines(y=0.1,
                    xmin=interval[0], 
                    xmax=interval[1], 
                    lw=2, 
                    label=f'HDI ({prob:0.4})'
                    )

    # CI equal-tailed around mean
    # val = x.mean()
    # interval, prob = compute_centered_credible_interval(x, val, 0.0005)
    # tt=axs[0].hlines(y=0.2,
    #                 xmin=interval[0], 
    #                 xmax=interval[1], 
    #                 lw=2, 
    #                 label=f'mean CI ({prob:0.4})'
    #                 )

    # # lower CI
    # interval, prob = compute_lower_credible_interval(x, 0.0005)
    # tt=axs[0].hlines(y=0.3,
    #                 xmin=interval[0], 
    #                 xmax=interval[1], 
    #                 lw=2, 
    #                 label=f'lower ({prob:0.4})'
    #                 )

    # # upper CI
    # interval, prob = compute_upper_credible_interval(x, 0.0005)
    # tt=axs[0].hlines(y=0.4,
    #                 xmin=interval[0], 
    #                 xmax=interval[1], 
    #                 lw=2, 
    #                 label=f'upper ({prob:0.4})'
    #                 )


    tt=axs[0].set_xlim(x.min(), x.max())
    tt=set_title_axes_labels(axs[0],None,f'{param}','density')
    finalize(axs[0])
    
    return (fig, axs)