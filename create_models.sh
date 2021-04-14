#!/bin/bash

python create_stan_model.py --beta0="normal(0,1)" --beta1="gamma(2,4)" --se="fixed(0.95)" --sp="fixed(0.95)" --savepath="/Users/erjo3868/Bayesian-Vaccine-Efficacy/data/exp1/model.pkl"
python create_stan_model.py --beta0="normal(0,1)" --beta1="gamma(2,4)" --se="beta(4,2)" --sp="beta(4,2)" --savepath="/Users/erjo3868/Bayesian-Vaccine-Efficacy/data/exp2/model.pkl"
python create_stan_model.py --beta0="normal(0,1)" --beta1="gamma(2,4)" --se="fixed(0.95)" --sp="fixed(0.95)" --savepath="/Users/erjo3868/Bayesian-Vaccine-Efficacy/data/exp3/model.pkl"
python create_stan_model.py --beta0="normal(0,1)" --beta1="gamma(2,4)" --se="beta(10,2)" --sp="beta(10,2)" --savepath="/Users/erjo3868/Bayesian-Vaccine-Efficacy/data/exp4/model.pkl"