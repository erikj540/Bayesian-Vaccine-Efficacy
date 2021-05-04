data {
    int<lower=0> N;
    int<lower=0> x1[N];
    int<lower=0> testResults[N];
    real<lower=0, upper=1> se;
    real<lower=0, upper=1> sp;
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
    for(i in 1:N) {
        real p  = inv_logit(beta0 + beta1*x1[i]);
        testResults[i] ~ bernoulli(se*p + (1-sp)*(1-p));
    }
}
generated quantities {}

