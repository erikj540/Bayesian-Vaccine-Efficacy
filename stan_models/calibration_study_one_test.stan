data {
    int<lower=0> N;
    int<lower=0> x1[N];
    int<lower=0> testResults[N];
    int<lower = 0> y_spec;
    int<lower = 0> n_spec;
    int<lower = 0> y_sens;
    int<lower = 0> n_sens;
}
parameters {
    real beta0;
    real<lower=0> pos_beta1;
    real<lower=0, upper = 1> sp;
    real<lower=0, upper = 1> se;
}
transformed parameters {
    real<upper=0> beta1 = -1*pos_beta1;
}
model {
    // Priors
    beta0 ~ normal(0,1);
    pos_beta1 ~ gamma(2,1);
    se ~ uniform(0,1);
    sp ~ uniform(0,1);

    // Calibration likelihood
    y_spec ~ binomial(n_spec, sp);
    y_sens ~ binomial(n_sens, se);

    // VE likelihood
    for(i in 1:N) {
        real p  = inv_logit(beta0 + beta1*x1[i]);
        testResults[i] ~ bernoulli(se*p + (1-sp)*(1-p));
    }
}
generated quantities {}