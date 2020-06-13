#!/bin/bash

#SBATCH -n 1                        # number of cores
#SBATCH -t 0-4:00                  # wall time (D-HH:MM)
#SBATCH -o slurm.%j.out             # STDOUT (%j = JobId)

python3 Screening.py
