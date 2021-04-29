data {
    int<lower=0> N_0;
    int<lower=0> x1_0[N_0];
    int<lower=0> testResults_0[N_0];
    real<lower=0, upper=1> se_0;
    real<lower=0, upper=1> sp_0;

    int<lower=0> N_1;
    int<lower=0> x1_1[N_1];
    int<lower=0> testResults_1[N_1];
    real<lower=0, upper=1> se_1;
    real<lower=0, upper=1> sp_1;
}

transformed data {}

parameters {
    real beta0;
    real<lower=0> pos_beta1;
}

transformed parameters {
    real<upper=0> beta1 = -1*pos_beta1;
}

model {
    // Priors
    beta0 ~ normal(0,1);
    pos_beta1 ~ gamma(2,1);

    // Likelihood
    // test 1
    for(i in 1:N_0) {
        real p_0  = inv_logit(beta0 + beta1*x1_0[i]);
        testResults_0[i] ~ bernoulli(se_0*p_0 + (1-sp_0)*(1-p_0));
    }
    // test 2
    for(i in 1:N_1) {
        real p_1  = inv_logit(beta0 + beta1*x1_1[i]);
        testResults_1[i] ~ bernoulli(se_1*p_1 + (1-sp_1)*(1-p_1));
    }
}

generated quantities {}

