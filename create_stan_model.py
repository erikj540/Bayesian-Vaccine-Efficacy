import numpy as np
import pandas as pd
import os, sys
import pystan as ps
from library import get_command_line_arguments, create_model_code, create_stan_model, save_stan_model

needed_params = ['beta0', 'beta1', 'se', 'sp',
                 'savepath'
                ]

params = get_command_line_arguments()
for param in needed_params:
    assert param in params, '{} not in params'.format(param)
print(f'params = {params}')
priors = params
model_code = create_model_code(priors)
model = create_stan_model(model_code)
save_stan_model(model, params['savepath'])