data {
    int<lower = 0> y_sample;
    int<lower = 0> n_sample;
    int<lower = 0> J_spec;
    int<lower = 0> y_spec[J_spec];
    int<lower = 0> n_spec[J_spec];
    int<lower = 0> J_sens;
    int<lower = 0> y_sens[J_sens];
    int<lower = 0> n_sens[J_sens];
    real<lower = 0> logit_spec_prior_scale;
    real<lower = 0> logit_sens_prior_scale;
}
parameters {
    real<lower = 0, upper = 1> p;
    real mu_logit_spec;
    real mu_logit_sens;
    real<lower = 0> sigma_logit_spec;
    real<lower = 0> sigma_logit_sens;
    vector<offset = mu_logit_spec, multiplier = sigma_logit_spec>[J_spec] logit_spec;
    vector<offset = mu_logit_sens, multiplier = sigma_logit_sens>[J_sens] logit_sens;
}
transformed parameters {
    vector[J_spec] spec = inv_logit(logit_spec);
    vector[J_sens] sens = inv_logit(logit_sens);
}
model {
    real p_sample = p * sens[1] + (1 - p) * (1 - spec[1]);
    y_sample ~ binomial(n_sample, p_sample);
    y_spec ~ binomial(n_spec, spec);
    y_sens ~ binomial(n_sens, sens);
    logit_spec ~ normal(mu_logit_spec, sigma_logit_spec);
    logit_sens ~ normal(mu_logit_sens, sigma_logit_sens);
    sigma_logit_spec ~ normal(0, logit_spec_prior_scale);
    sigma_logit_sens ~ normal(0, logit_sens_prior_scale);
    mu_logit_spec ~ normal(4, 2); // weak prior on mean of distribution of spec
    mu_logit_sens ~ normal(4, 2); // weak prior on mean of distribution of sens
}