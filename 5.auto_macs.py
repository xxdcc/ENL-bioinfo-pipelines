from __future__ import print_function
import glob
import os
import pandas as pd
import numpy as np


# configure the parameters
nodes_ppn = [1, 1]
memory = 16
wait_time = [20, 00]
quene = "medium"
inpath = '/mount/weili3/xc3/ENL2_ChIP/data/'
exps = ['293*', 'HK2*']
ctrl = 'input*'
treat = 'F*'

outpath = '/mount/weili3/xc3/ENL2_ChIP/res_nsp/'


# open the initialization header for pbs and read the contents
with open('/home/xc3/experiment/initial.pbs','r') as f:
	pbs_header = f.readlines()


for exp in exps:
	
	treat_files = glob.glob(inpath+exp+treat+'/*.bowtie.bed.nsp.shuf')
	ctrl_file = glob.glob(inpath+exp+ctrl+'/*.bowtie.bed.nsp.shuf')[0]
	names = [ifile.split('/')[-2] for ifile in treat_files]

	for i, treat_file in enumerate(treat_files):
		experiment_name = "macs_{}.ato".format(names[i])
		with open(experiment_name,'w') as f:

			pbs_initial = pbs_header[:]
			# configuration for the experiments
			# pbs_initial[1]::job name
			pbs_initial[1] = pbs_initial[1].format(str(names[i]))
			# pbs_initial[2]::nodes and ppn
			pbs_initial[2] = pbs_initial[2].format(*nodes_ppn)
			# pbs_initial[4]::memeroy
			pbs_initial[4] = pbs_initial[4].format(memory)
			# pbs_initial[5]::waiting time
			pbs_initial[5] = pbs_initial[5].format(*wait_time)
			# pbs_initial[11]::err output
			pbs_initial[11] = pbs_initial[11].format(names[i])
			# pbs_initial[12]::log
			pbs_initial[12] = pbs_initial[12].format(names[i])
			# pbs_initial[14]::quene
			pbs_initial[14] = pbs_initial[14].format(quene)

			
			# write all the configurations into the pbs file
			for line in pbs_initial:
				f.write(line)

			# write the shuf code
			line ="macs14 -t {} -c {} -n {}.nsp --nomodel --nolambda -g hs --wig -S -p 1e-8".format(treat_files[i], ctrl_file, outpath + names[i])
			
			f.write(line)
