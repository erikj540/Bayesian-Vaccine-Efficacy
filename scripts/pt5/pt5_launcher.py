import numpy as np
import os

TEST = 0 # 1=test, 0=not test

# set parameters
if TEST==1: # testing
    sp_proportions = [0.5, 0.6]
    n_sims = 2
else: # not testing
    sp_proportions = np.linspace(0, 1, 41)
    n_sims = 50
    
# prevs = [0.5]
# alphas = [0.5]
# Ns = [5000]
# ses = [0.7]
# sps = [0.9]
# vax_props = [0.5]
# num_validation_tests = 500

# for prev in prevs:
#     for alpha in alphas:
#         for N in Ns:
#             for se in ses:
#                 for sp in sps:
#                     for vax_prop in vax_props:
#                         for prop in sp_proportions:
#                             n_spec = int(prop*num_validation_tests)
#                             n_sens = num_validation_tests - n_spec

#                             code = f'sbatch --job-name=point5 --export=prev="{prev}",alpha="{alpha}",se="{se}",sp="{sp}",vax_prop="{vax_prop}",N={N},n_sens={n_sens},n_spec={n_spec},n_sims={n_sims} scripts/pt5.sbatch'

#                             os.system(code)

prev, alpha = 0.5, 0.1
N = 5000
se, sp = 0.7, 0.9
vax_prop = 0.5
num_validation_tests = 500

for prop in sp_proportions:
    n_spec = int(prop*num_validation_tests)
    n_sens = num_validation_tests - n_spec

    code = f'sbatch --job-name=pt5 --export=prev="{prev}",alpha="{alpha}",se="{se}",sp="{sp}",vax_prop="{vax_prop}",N={N},n_sens={n_sens},n_spec={n_spec},n_sims={n_sims} scripts/pt5.sbatch'

    os.system(code)