import pandas as pd
import numpy as np
import os

os.chdir('/home/lyz/co-phase-separation/PSGAT/data/')

integrate = pd.read_json('./PPIN/edge.w_sim.js')
integrate.columns = ['A', 'B', 'combined_score']
integrate['combined_score'] = integrate['combined_score'] * 1e3
integrate.to_csv('./PPIN/INTEGRATE.csv', index=None)

string = pd.read_table('./PPIN/9606.protein.links.v11.5.txt', sep=' ')
string['protein1'] = string['protein1'].apply(lambda x: x.split('.')[-1])
string['protein2'] = string['protein2'].apply(lambda x: x.split('.')[-1])

ensp2entry_dict = pd.read_table('./IdMapping/ensp2uniprot.txt')\
                    .dropna(subset=['Protein stable ID', 'UniProtKB/Swiss-Prot ID'])\
                    .groupby('Protein stable ID')['UniProtKB/Swiss-Prot ID']\
                    .apply(lambda x: ','.join(set(x))).to_dict()

string['A'] = string['protein1'].map(ensp2entry_dict)
string['B'] = string['protein2'].map(ensp2entry_dict)
string = string.dropna(subset=['A', 'B'])[['A', 'B', 'combined_score']].copy()
string.to_csv('./PPIN/STRING.csv', index=None)