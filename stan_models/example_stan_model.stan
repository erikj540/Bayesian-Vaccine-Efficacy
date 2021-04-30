data {
    int<lower=0> N;
    int<lower=0,upper=1> y[N];
    int<lower=0,upper=1> x1[N];
}
transformed data {}
parameters {
    real beta0;
    real<lower=0> beta1_pos;
    real<lower=0,upper=1> se;
    real<lower=0,upper=1> sp;
}
transformed parameters {
    real<upper=0> beta1;
    beta1 = -1*beta1_pos;
}
model {
    // Priors
    beta0 ~ normal(0,1);
    beta1_pos ~ gamma(2,4);
    se ~ beta(4,2);
    sp ~ beta(4,2);
    // Likelihood
    for(i in 1:N) {
        real p;
        p = inv_logit(beta0 + beta1*x1[i]);
        y[i] ~ bernoulli(se*p + (1-sp)*(1-p));
    }
}
generated quantities {}