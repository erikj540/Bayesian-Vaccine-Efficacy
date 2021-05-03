import pickle
import pystan as ps
import os
import sys

MODEL_DIR = '/Users/erjo3868/Bayesian-Vaccine-Efficacy/stan_models'

def get_command_line_arguments():
    """
    Get command line arguments.
    """
    args = sys.argv
    args = args[1:]
    argument_dict = {}
    for arg in args:
        name = arg.split('=')[0][2:]
        val = arg.split('=')[1]
        argument_dict[name] = val
    return argument_dict

def main(name):
    """

    """
    path2model = os.path.join(MODEL_DIR, f'{name}.stan')
    outpath = os.path.join(MODEL_DIR, f'{name}.pkl')
    # if os.path.exists(outpath):
    #     print('Model already exists! I am NOT going to overwrite the existing model!')
    # else:
    model = ps.StanModel(file=path2model)
    with open(outpath, 'wb') as f:
        pickle.dump(
            model, 
            f, 
            protocol=pickle.HIGHEST_PROTOCOL
        )

if __name__=="__main__":
    needed_params = [
        'name'
    ]
    params = get_command_line_arguments()
    for param in needed_params:
        assert param in params, '{} not in params and is required'.format(param)
    print(f'params = {params}')

    main(params['name'])