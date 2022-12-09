from sentence_transformers import SentenceTransformer, util
import pandas as pd
import pickle
import os
from os import listdir
from os.path import isfile, join
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import numpy as np

model = SentenceTransformer('all-mpnet-base-v2')
playlists = pd.read_csv("data/filteredSample.csv")
# for i, playlist in playlists.iterrows():
#  	playlists.loc[playlists['_id'] == playlist['_id'], ['_id']] = playlist['_id'].replace("{'$oid': '", "").replace("'}", "")

cache_path = 'data/names embeddings/'


def getEmbedding(id, corpus_sentences):
	id = id.replace("{'$oid': '", "").replace("'}", "")
	embedding_cache_path = '%s%s.pkl' % (cache_path, id)
	if not os.path.exists(embedding_cache_path):
		# read your corpus etc
		# print("Encoding the corpus. This might take a while")
		corpus_embeddings = model.encode(corpus_sentences)

		# print("Storing file on disc")
		with open(embedding_cache_path, "wb") as fOut:
			pickle.dump({'embeddings': corpus_embeddings}, fOut)

	else:
		# print("Loading pre-computed embeddings from disc")
		with open(embedding_cache_path, "rb") as fIn:
			cache_data = pickle.load(fIn)
			corpus_embeddings = cache_data['embeddings']

	return corpus_embeddings


onlyfiles = [f for f in listdir('data/categories/') if isfile(join('data/categories/', f))]
categories = [f.replace(".csv", "") for f in onlyfiles]

out = open("data/playlistCategories.csv", "w")
out.write("playlist_id, cluster\n")

for i, playlist in playlists.iterrows():
	# print(playlist['_id'])
	playlist_embedding = getEmbedding(playlist['_id'], playlist['name'])
	cos_sim = -2
	cluster = ''
	for c in categories:
		corpus = pd.read_csv("data/categories/%s.csv" % c, encoding="utf-8", names=['name'], header=None)
		if len(corpus['name'].values.tolist()) > 0:
			cat_embedding = getEmbedding(c, (' ').join(corpus['name'].values.tolist()))
			# print(playlist_embedding)
			cos_sim_temp = util.cos_sim(playlist_embedding, cat_embedding).item()
			if cos_sim == -2:
				cluster = c
				cos_sim = cos_sim_temp
			elif cos_sim_temp > cos_sim:
				cluster = c
				cos_sim = cos_sim_temp

	row = "%s,%s\n" % (playlist['_id'], cluster)
	out.write(row)
out.close()
