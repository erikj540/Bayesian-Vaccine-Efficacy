import numpy as np
import os
import time

n_sims = 500
for ii in range(n_sims):
    code = f'sbatch --job-name=pt3 --export=i="{ii}" scripts/pt3.sbatch'
    os.system(code)
    time.sleep(0.1)