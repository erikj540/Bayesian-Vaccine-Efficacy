import pickle
import pystan as ps
import os, argparse, sys

MODEL_DIR = '/Users/erjo3868/Bayesian-Vaccine-Efficacy/stan_models'

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
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', action='store', type=str, required=True)
    args = parser.parse_args()

    main(args.name)