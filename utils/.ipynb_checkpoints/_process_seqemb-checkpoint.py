import pandas as pd
import numpy as np
import h5py
import os
from sklearn.decomposition import PCA

os.chdir('/home/lyz/co-phase-separation/PSGAT/data/')

filename = './NodeFeat/SeqEmb/human-proteome.h5'
data = h5py.File(filename, 'r')
Datasetnames = list(data.keys())

def get_dict_value(now_dict):
    for key in now_dict.keys():
        data = now_dict[key]
    if isinstance(data, h5py.Group):
        data = get_dict_value(data)
    return data

seq_dict = dict()
for key in data.keys() :
    if isinstance(data[key], h5py.Dataset)==True:
        seq_encode = data[key][:].reshape(-1, 1)
    elif isinstance(data[key], h5py.Group)==True:
        seq_encode = get_dict_value(data[key])[:].reshape(-1, 1)
    key_entry = key.split('|')[1]
    seq_dict[key_entry] = seq_encode

data = np.concatenate(list(seq_dict.values())).reshape(-1, 6165)
data = np.asarray(data, dtype='float')
embed = pd.DataFrame(data)
embed.index = seq_dict.keys()
embed = embed.reset_index().rename(columns={'index': 'entry'})
X = embed.iloc[:, 1:].to_numpy()

n_components = [60, 80, 100, 120]

for n in n_components:
    pca = PCA(n_components=n)
    X_new = pca.fit_transform(X)
    embed_new = pd.concat([embed['entry'], pd.DataFrame(X_new)], axis=1)
    embed_new.to_pickle(f'./NodeFeat/SeqEmb/seqemb_{n}d.pkl')