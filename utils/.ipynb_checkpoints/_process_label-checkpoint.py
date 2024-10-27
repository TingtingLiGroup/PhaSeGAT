import pandas as pd
import numpy as np
import os

os.chdir('/home/lyz/co-phase-separation/PSGAT/data/')

hprot = pd.read_table('./Label/UniProt-SwissProt (Release 22_03)/HUMAN_9606_table.tsv')
label = pd.read_pickle('./Label/human.condensate-formation.proteins-v1.pkl')
phasep = label[label['source']=='literature']['uniprot_entry'].tolist()
hprot = hprot['Entry'].to_frame()
hprot.loc[hprot['Entry'].isin(phasep), 'label'] = 1
hprot['label'] = hprot['label'].fillna(0).astype(int)
hprot.rename(columns={'Entry': 'Gene'}).to_csv('./Label/labels.csv', index=None)