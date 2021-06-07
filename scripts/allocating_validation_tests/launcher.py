import os
import numpy as np

prevs = [0.01, 0.95]
alphas = [0.1, 0.9]
vax_probs = [0.05, 0.95]
N = 5000
se, sp = 0.97, 0.97
num_validation_tests = 200
n_burnin, n_samples, n_chains = 2000, 10000, 1
sp_proportions = np.linspace(0, 1, 41)
n_sims = 25

for prev in prevs:
    for alpha in alphas:
        for vax_prob in vax_probs:
            for prop in sp_proportions:
                for ii in range(n_sims):
                    n_spec = int(prop*num_validation_tests)
                    n_sens = num_validation_tests - n_spec

                    name = f'prev{int(100*prev)}_alpha{int(100*alpha)}_vaxProb{int(vax_prob*100)}_iter{ii}_nSpec{n_spec}_nSens{n_sens}_N{N}_se{int(se*100)}_sp{int(sp*100)}_nBurnin{n_burnin}_nSamples{n_samples}_nChains{n_chains}'

                    code = f'sbatch --job-name=pt5 --export=prev="{prev}",alpha="{alpha}",se="{se}",sp="{sp}",vax_prob="{vax_prob}",N={N},n_sens={n_sens},n_spec={n_spec},n_burnin={n_burnin},n_samples={n_samples},n_chains={n_chains},name="{name}" scripts/allocating_validation_tests/slurm_script.sbatch'

                    os.system(code)