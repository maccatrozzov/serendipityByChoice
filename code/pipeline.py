from statistics import mean, median, median_low, median_high
import pandas as pd
from random import sample
import numpy as nu	


from playlistGraphBuilder import PlaylistGraph
from graphEnrichment import getEnrichment, getArtistGenre
from ExtractAllPaths import extractAllPath
from cosineSimilarity import getPlaylistCosineSim



def get_sample():
	try:
		print("sample found")
		sample = pd.read_csv('data/filteredSample.csv')
	except:
		print("making sample")
		sample = filterplaylist(makeSample(pd.read_json('data/playlists.json', lines=True))) 

	return(sample)

def datasetStatistics():
	playlists = pd.read_json('data/playlists.json', lines=True)
	playlistLength = []
	playlistNum = []
	owners = playlists['owner']
	for p,playlist in playlists.iterrows():
		playlistLength.append(len(playlist['tracks']))
	quantiles = nu.quantile(playlistLength,(0,.25,.5,.75,1))
	
	for p,playlist in playlists.iterrows():
		owners.append(playlist['owner'])
		if len(playlist['tracks']) >= quantiles[1] and len(playlist['tracks']) <= quantiles[3]:
			playlist2use.append(playlist['id']) 
	
	filteredPlaylists = (playlists.loc[playlists['id'].isin(playlist2use)])
	
def makeSample(playlists):
	users = list(set(playlists['owner']))
	sampleUsers = sample(users, 300)
	playlistSample = (playlists.loc[playlists['owner'].isin(sampleUsers)])
	playlistSample.to_csv('data/sample300users.csv')
	return(playlistSample)
	
def filterplaylist(playlists):
	playlist2use = []
	owners = []
	playlists['id'] = playlists['_id'].map(lambda x: x['$oid'])
	for p,playlist in playlists.iterrows():
		owners.append(playlist['owner'])
		if len(playlist['tracks']) >= 11 and len(playlist['tracks']) <= 41:
			playlist2use.append(playlist['id']) 
	
	filteredPlaylists = (playlists.loc[playlists['id'].isin(playlist2use)])
	filteredPlaylists.to_csv('data/filteredSample.csv')
	return(filteredPlaylists)



#def main(playlists):
print("getting playlists...")
playlists = get_sample()
# print("building playlists graphs")
# PlaylistGraph(playlists)
print("enrichment")
# getEnrichment(playlists)
getArtistGenre(playlists)
# print("patterns extraction")
# extractAllPath()
#print("cosine similarity calculation")
#getPlaylistCosineSim()

