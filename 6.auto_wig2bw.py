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
inpath = '/mount/weili3/xc3/ENL2_ChIP/res_nsp/'
os.chdir('/home/xc3/experiment/ENL2/Chip-seq_analysis/second_batch')

files = glob.glob(inpath+'*treat*.wig.gz')
names = [ifile.split('/')[-1].split('.')[0] for ifile in files]

# open the initialization header for pbs and read the contents
with open('/home/xc3/experiment/initial.pbs','r') as f:
	pbs_header = f.readlines()

# write each sample a pbs files
for i in range(len(files)):
	experiment_name = "wig2bw_{}_treat.ato".format(names[i])
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

		# line = 'cd {}\n\n'.format(inpath)
		# f.write(line)
		name = names[i]
		# line: command to run to extract the sequence
		# sed -n 2~4p : print from line 2 with step interval for 4 
		line ='gunzip -c {} > {}.raw.wig'.format(files[i],files[i])

		f.write(line + '\n')

		line = '/home/xc3/software/wigToBigWig -clip {}.raw.wig /mount/weili3/xc3/genomes/hg19.chrom.sizes {}_treat.nsp.bw'.format(files[i], inpath+names[i])
		
		f.write(line + '\n')



