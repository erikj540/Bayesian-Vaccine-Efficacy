import numpy as np
import pandas as pd
import pickle
import pystan as ps
from scipy.stats import bernoulli, uniform, norm, beta, gamma, binom
from scipy.special import expit
import arviz as ar
import sys
from utilities.plotUtils import *
from utilities.utilityFunctions import unpickle_object

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
        else: # se_prior=='fixed*' & sp_rior!='fixed*'
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

# def sample_from_model(compiled_model_path, n_burnin, n_samples, n_chains):
#     # unpickle compiled model
#     model = unpickle_object(compiled_model_path)
#     code = model.model_code
#     # sample from model
#     fit = sample_from_model(model, stan_data, n_burnin, n_samples, n_chains)
#     idata = ar.from_pystan(fit)

#     del(model) # delete model

#     return {
#         'fit': idata,
#         'code': code,
#     }

class SimulatedData:
    def __init__(self, N, vax_prob, beta0, beta1, se, sp):
        self.N = N
        self.vax_prob = vax_prob
        self.beta0 = beta0
        self.beta1 = beta1 
        self.se = se
        self.sp = sp

    def generate_ve_study_data(self):
        x1 = bernoulli.rvs(self.vax_prob, size=self.N) # vaccinated (1)/unvaccinated (0)
        X = pd.DataFrame({'vax': x1,})
        beta_vec = np.array([self.beta0, self.beta1])
        X['prob_td'] = X.apply(lambda row: expit(np.dot(np.array([1, row['vax']]), beta_vec)), axis=1)
        # X['test_id'] = test_id
        X['test_result'] = -1
        X['test_result'] = X['prob_td'].apply(lambda p: bernoulli.rvs(self.se*p + (1-self.sp)*(1-p)))

        self.study_data = X

    def generate_test_validation_data(self, n, prob):
        return binom.rvs(n, prob)

    def create_stan_data_se_sp_validation_one_dx_test(self, n_sens, n_spec):
        VALIDATION_ONE_DX_TEST_NEEDED_PARAMS = ['N', 'x1', 'testResults', 'y_spec', 'n_spec', 'y_sens', 'n_sens']
        self.n_sens = n_sens
        self.n_spec = n_spec
        self.y_sens = self.generate_test_validation_data(self.n_sens, self.se)
        self.y_spec = self.generate_test_validation_data(self.n_spec, self.sp)

        self.stan_data = {
            'N': self.N,
            'x1': np.array(self.study_data['vax']),
            'testResults': np.array(self.study_data['test_result']),
            'y_spec': self.y_spec,
            'n_spec': self.n_spec,
            'y_sens': self.y_sens,
            'n_sens': self.n_sens,
        }

    def create_stan_data_se_sp_fixed_one_dx_test(self, se, sp):
        self.stan_data = {
            'N': self.N,
            'x1': np.array(self.study_data['vax']),
            'testResults': np.array(self.study_data['test_result']),
            'se': se,
            'sp': sp,
        }

class StudyData:
    def __init__(self, vax_prob, beta0, beta1):
        self.vax_prob = vax_prob
        self.beta0 = beta0
        self.beta1 = beta1

    def generate_validation_data(self, n, prob):
        return binom.rvs(n, prob)

    def generate_one_test_data(self, N, se, sp, test_id):
        x1 = bernoulli.rvs(self.vax_prob, size=N) # vaccinated (1)/unvaccinated (0)
        X = pd.DataFrame({'vax': x1,})
        beta_vec = np.array([self.beta0, self.beta1])
        X['prob_td'] = X.apply(lambda row: expit(np.dot(np.array([1, row['vax']]), beta_vec)), axis=1)
        X['test_id'] = test_id
        X['test_result'] = -1
        X['test_result'] = X['prob_td'].apply(lambda p: bernoulli.rvs(se*p + (1-sp)*(1-p)))

        data = {
            f'N': N, 
            f'se': se,
            f'sp': sp, 
            f'X': X
        }

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
    prop = np.sum((x>=interval[0]) & (x<=interval[1]))/len(x)
    return (interval, prop)

def compute_centered_credible_interval(samples, val, step, prob=0.95):
    """
    Computes X% credible interval where the credible interval is centered on user supplied value. 
    """
    prop = 0
    ii = 1
    while prop<prob:
        interval = [val-ii*step, val+ii*step]
        prop = compute_probability_of_interval(samples, interval)
        ii += 1
    return (interval, prop)

def compute_lower_credible_interval(samples, step, prob=0.95):
    prop = 0
    ii = 1
    min_val = samples.min()
    while prop<prob:
        interval = [min_val, val+ii*step]
        prop = compute_probability_of_interval(samples, interval)
        ii += 1
    return (interval, prop)

def compute_upper_credible_interval(samples, step, prob=0.95):
    prop = 0
    ii = 1
    max_val = samples.max()
    while prop<prob:
        interval = [max_val-ii*step, max_val]
        prop = compute_probability_of_interval(samples, interval)
        ii += 1
    return (interval, prop)

def compute_probability_of_interval(samples, interval):
    samples = samples.sort_values().reset_index(drop=True)
    mask = ((samples>=interval[0]) & (samples<=interval[1]))
    return np.sum(mask)/len(samples)

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
    low, up = 0.0001, 0.9999
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
def posterior_plot(idata, param, true_val, prior_name,
                   mean=False, lower=False, upper=False, 
                  ):

    """
    
    """
    fig, axs = fig_setup(1,1)

    # true value as vertical line
    # true = model.true_params[param]
    tt=axs[0].axvline(x=true_val, color='k', linestyle='--',
                label=f"true {param}={true_val}"
                ) #

    # prior
    prior = generate_prior(prior_name)
    if param=='beta1':
        prior[:,0] = (-1)*prior[:,0]
    tt=axs[0].plot(prior[:,0], prior[:,1], 
                lw=3, 
                color='r', 
                label=f'prior {prior_name}'
                )

    # posterior samples
    nbins = 100
    x = idata.to_dataframe()[('posterior', f'{param}')]
    n, bins, patches =axs[0].hist(x,
                        bins=nbins,
                        density=True,
                        label='posterior samples',
    #                      label=f'{param}'
                        )
    max_count = np.max(n)

    # credible intervals
    # HDI
    interval, prob = compute_hdi(idata, param)
    prob = np.sum((x>=interval[0]) & (x<=interval[1]))/len(x)
    tt=axs[0].hlines(y=max_count/10,
                    xmin=interval[0], 
                    xmax=interval[1], 
                    lw=2, 
                    label=f'HDI ({prob:0.4})'
                    )

    # CI equal-tailed around mean
    if mean is True:
        val = x.mean()
        interval, prob = compute_centered_credible_interval(x, val, 0.0005)
        tt=axs[0].hlines(y=max_count/12,
                        xmin=interval[0], 
                        xmax=interval[1], 
                        lw=2,
                        label=f'mean CI ({prob:0.4})'
                        )

    # lower CI
    if lower is True:
        interval, prob = compute_lower_credible_interval(x, 0.0005)
        tt=axs[0].hlines(y=max_count/14,
                        xmin=interval[0], 
                        xmax=interval[1], 
                        lw=2, 
                        label=f'lower ({prob:0.4})'
                        )

    # upper CI
    if upper is True:
        interval, prob = compute_upper_credible_interval(x, 0.05)
        tt=axs[0].hlines(y=max_count/16,
                        xmin=interval[0], 
                        xmax=interval[1], 
                        lw=2, 
                        label=f'upper ({prob:0.4})'
                        )


    tt=axs[0].set_xlim(x.min(), x.max())
    tt=set_title_axes_labels(axs[0],None,f'{param}','density')
    
    return (fig, axs)


def bernoulli_confidence_interval(p_hat, n, alpha=0.05):
    z_val = norm.ppf(1-(alpha/2))
#     print(z_val)
    se = np.sqrt(p_hat*(1-p_hat)/n)
    return [p_hat-z_val*se, p_hat+z_val*se]

def create_ci_plots(df, param, outpath, sort=False):
    # subset to single parameter
    ci_df = df[df['param']==param]
    
    # sort and reset index dataframe
    if sort is True:
        ci_df.sort_values('true', inplace=True) # sort
    ci_df.reset_index(inplace=True, drop=True) # reset index
    
    # compute proportion of CIs capturing true parameter value
    prop_ci_capturing_true = np.sum((ci_df['true']>=ci_df['lower']) & (ci_df['true']<=ci_df['upper']))/ci_df.shape[0]
    interval = bernoulli_confidence_interval(prop_ci_capturing_true, ci_df.shape[0])
#     interval
    
    # plot
    fig, axs = fig_setup(1, 1, w=20)
    tt=centered_credible_interval_plot(axs[0], ci_df)
    tt=set_title_axes_labels(axs[0], 
                        f'{param}\nproportion of CIs capturing true = {prop_ci_capturing_true} ([{interval[0]:.3}, {interval[1]:.3}])',
                        'iteration',
                        'CI centered on true'
                        )
    plt.tight_layout()
    tt=axs[0].set_xlim([-1,201])
    finalize(axs[0])
    plt.savefig(outpath,
                dpi=300
            )

def sample_from_prior(stan_prior):
    name = stan_prior.split('(')[0]
    if name!='fixed':
        param1, param2 = float(stan_prior.split('(')[1].split('-')[0]), float(stan_prior.split('(')[1].split('-')[1][:-1])
    else:
        sample = float(stan_prior.split('(')[1][:-1])

    if name=='normal':
        sample = norm.rvs(loc=param1, scale=param2)
    elif name=='beta':
        sample = beta.rvs(a=param1, b=param2)
    elif name=='gamma':
        sample = gamma.rvs(a=param1, scale=1/param2)
    elif name=='uniform': 
        sample = uniform.rvs(a=param1, scale=param2-param1)

    return sample

class MCMCSamples:
    """This class is for plotting and analyzing the results of MCMC samples"""
    def __init__(self, data, mcmc_samples, true_param_vals):
        """ 
        Params:
            - data (DataFrame) : has to have 'test_result' and 'vax' column. vax=0 (1) should be unvaccinated (vaccinated) and test_result=0 (1) should be test negative (positive)
            - mcmc_samples : output of arviz.from_pystan
            - true_param_vals : dict containing true param values
        """
        self.data = data
        self.mcmc_samples = mcmc_samples
        self.true_param_vals = true_param_vals

    def compute_test_result_summaries(self):
        tmp = self.data.groupby(['vax', 'test_result'])['test_result'].count()
        self.num_unvax_testNeg = tmp[0][0]
        self.num_unvax_testPos = tmp[0][1]
        self.num_vax_testNeg = tmp[1][0]
        self.num_vax_testPos = tmp[1][1]
        
    def compute_uncorrected_point_estimates(self):
        """
        Compute naive odds ratio which is (n_vp / n_vn) / (n_up / n_un)
        """
        vax_odds = self.num_vax_testPos/self.num_vax_testNeg
        unvax_odds = self.num_unvax_testPos/self.num_unvax_testNeg

        # return vax_odds/unvax_odds
        self.uncorrected_odds_ratio = vax_odds/unvax_odds
        self.uncorrected_ve_pt_estimate = 1 - self.uncorrected_odds_ratio

    def compute_corrected_point_estimates(self):
        """
        Compute corrected odds ratio ala Endo et al. equation 3 and Marc's derivation.
        """
        nu = self.num_unvax_testNeg + self.num_unvax_testPos
        nv = self.num_vax_testNeg + self.num_vax_testPos
        se, sp = self.true_param_vals['se'], self.true_param_vals['sp']
        vax_odds = (self.num_vax_testPos - (1-sp)*nv)/(self.num_vax_testNeg - (1-se)*nv)
        unvax_odds = (self.num_unvax_testPos - (1-sp)*nu)/(self.num_unvax_testNeg - (1-se)*nu)

        # return vax_odds/unvax_odds
        self.corrected_odds_ratio = vax_odds/unvax_odds
        self.corrected_ve_pt_estimate = 1 - self.corrected_odds_ratio
    
    def posterior_samples_plot(self, param, ax, smooth=0):
        nbins = 100
        samples = self.mcmc_samples.to_dataframe()[('posterior', f'{param}')]
        n, bins = np.histogram(counts, bins=100, density=True)
        n, bins, patches = ax.hist(
            samples,
            bins=nbins,
            density=True,
            label='posterior samples',
            # label=f'{param}'
        )
        tt = ax.axvline(
            x=self.true_param_vals[param], 
            color='k', 
            linestyle='--',
            label=f"true {param}={self.true_param_vals[param]:.3f}"
        )
        # return ax

    # def credible_interval_df(self, prob=0.95):


    def centered_ci_plot(self, param=None):
        if param is None:
            for param in self.true_param_vals.keys():
                samples = self.mcmc_samples.to_dataframe()[('posterior', f'{param}')]
                compute_centered_credible_interval(samples, val, 0.0005, prob)


def generate_study_data(beta0, beta1, vax_prob, N, se, sp, test_id):
        x1 = bernoulli.rvs(vax_prob, size=N) # vaccinated (1)/unvaccinated (0)
        X = pd.DataFrame({'vax': x1,})
        beta_vec = np.array([beta0, beta1])
        X['prob_td'] = X.apply(lambda row: expit(np.dot(np.array([1, row['vax']]), beta_vec)), axis=1)
        X['test_id'] = test_id
        X['test_result'] = -1
        X['test_result'] = X['prob_td'].apply(lambda p: bernoulli.rvs(se*p + (1-sp)*(1-p)))

        data = {
            'beta0': beta0,
            'beta1': beta1,
            'vax_prob': vax_prob,
            'N': N, 
            'se': se,
            'sp': sp, 
            'X': X
        }

        return data