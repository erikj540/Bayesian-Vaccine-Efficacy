data {
    int<lower=0> N_test0;
    int<lower=0> N_test1;
    int<lower=0> x1_test0[N_test0];
    int<lower=0> x1_test1[N_test1];
    int<lower=0> test0_results[N_test0];
    int<lower=0> test1_results[N_test1];
    real logit_se0_prior_mu;
    real<lower=0> logit_se0_prior_scale;
    real logit_sp0_prior_mu;
    real<lower=0> logit_sp0_prior_scale;
    real logit_se1_prior_mu;
    real<lower=0> logit_se1_prior_scale;
    real logit_sp1_prior_mu;
    real<lower=0> logit_sp1_prior_scale;
}
transformed data {}
parameters {
    real beta0;
    real<lower=0> pos_beta1;
    real<lower=0,upper=1> logit_se0;
    real<lower=0,upper=1> logit_sp0; 
    real<lower=0,upper=1> logit_se1;
    real<lower=0,upper=1> logit_sp1; 
}
transformed parameters {
    real<lower=0, upper=1> beta1 = -1*pos_beta1;
    real<lower=0, upper=1> se0 = inv_logit(logit_se0);
    real<lower=0, upper=1> sp0 = inv_logit(logit_sp0);
    real<lower=0, upper=1> se1 = inv_logit(logit_se1);
    real<lower=0, upper=1> sp1 = inv_logit(logit_sp1);
}

model {
    // Priors
    beta0 ~ normal(0,2);
    pos_beta1 ~ gamma(2,1);
    logit_se0 ~ normal(logit_se0_prior_mu, logit_se0_prior_scale);
    logit_sp0 ~ normal(logit_sp0_prior_mu, logit_sp0_prior_scale);
    logit_se1 ~ normal(logit_se1_prior_mu, logit_se1_prior_scale);
    logit_sp1 ~ normal(logit_sp1_prior_mu, logit_sp1_prior_scale);

    // Vectorized Bernoulli test probabilities
    // real p0[N_test0] = beta0 + beta1*x1_test0;
    // real p1[N_test1] = beta0 + beta1*x1_test1;

    // Likelihood
    // test0_results ~ binomial(N_test0, p0);
    // test1_results ~ binomial(N_test1, p1);

    for(i in 1:N_test0) {
        real p;
        p = inv_logit(beta0 + beta1*x1_test0[i]);
        test0_results[i] ~ bernoulli(se0*p + (1-sp0)*(1-p));
    }

    for(i in 1:N_test1) {
        real p;
        p = inv_logit(beta0 + beta1*x1_test1[i]);
        test0_results[i] ~ bernoulli(se1*p + (1-sp1)*(1-p));
    }
}
generated quantities {}

