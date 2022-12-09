import pandas as pd
from rdflib import Graph
import numpy as np


def coping_potential(playlistOwners):
	coping = open('data/userCopingPotentialArtistGenre.csv', 'w')
	coping.write("Userid, CopingPotential\n")

	for owner, playlists in playlistOwners.iteritems():
		profile = open('data/UserProfilesArtistGenre/%s.csv' %(owner), 'w')
		genres = []
		print(owner)
		for playlistId in playlists:
			playlistGraph = Graph()
			playlistGraph.parse('data/PlaylistGraphsEnrichedArtistGenre/%s.ttl' %(playlistId),format='turtle')
			for s, p, o in playlistGraph.triples( (None, DB.genre, None) ):
				if o not in genres:
					genres.append(o)
					profile.write(o + '\n')
		coping.write(str(owner) + "," + str(len(genres)) + "\n")
	
def serendipity_level(playlistOwners, cp):
	try:
		up = pd.read_csv('data/ups.csv')
	except:
		up = open('data/ups.csv', 'w')
		up.write("Userid,CopingPotential,Serendipity,SerendipityMax,SerendipityMin\n")
		for owner, playlists in playlistOwners.iteritems():
			serendipity_values = []
			serendipityMax_values = []
			serendipityMin_values = []
			for playlistId in playlists:
				pl = pd.read_csv("data/PlaylistSerendipity/%s.csv" % playlistId)
				serendipity_values.append(pl['serendipity'].item())
				serendipityMax_values.append(pl['serendipity_max'].item())
				serendipityMin_values.append(pl['serendipity_min'].item())
			serendipity = sum(serendipity_values) / len(serendipity_values)
			serendipityMax = max(serendipityMax_values)
			serendipityMin = min(serendipityMin_values)
			copingPotential = cp.loc[cp['Userid'] == owner, 'CopingPotential'].item()
			up.write("%s,%s,%s,%s,%s\n" % (str(owner), str(copingPotential), str(serendipity), str(serendipityMax), str(serendipityMin)))
		up = pd.read_csv('data/ups.csv')
	return up
def serendipity_level_cluster(clusterPlaylist):
	try:
		serendipityCat = pd.read_csv('data/serendipity_category.csv')
	except:
		out = open('data/serendipity_category.csv', 'w')
		out.write("Cluster,Serendipity,SerendipityMax,SerendipityMin\n")
		for cluster, playlists in clusterPlaylist.iteritems():
			serendipity_values = []
			serendipityMax_values = []
			serendipityMin_values = []
			for playlistId in playlists:
				pl = pd.read_csv("data/PlaylistSerendipity/%s.csv" % playlistId)
				serendipity_values.append(pl['serendipity'].item())
				serendipityMax_values.append(pl['serendipity_max'].item())
				serendipityMin_values.append(pl['serendipity_min'].item())
			serendipity = sum(serendipity_values) / len(serendipity_values)
			serendipityMax = max(serendipityMax_values)
			serendipityMin = min(serendipityMin_values)

			out.write("%s,%s,%s,%s\n" % (str(cluster), str(serendipity), str(serendipityMax), str(serendipityMin)))

		serendipityCat = pd.read_csv('data/serendipity_category.csv')
	return serendipityCat

playlists = pd.read_csv("data/filteredSample.csv")

for i, playlist in playlists.iterrows():
	playlists.loc[playlists['_id'] == playlist['_id'],['_id']] = playlist['_id'].replace("{'$oid': '","").replace("'}","")

playlistOwners = playlists.groupby('owner')['_id'].agg(list)
cp = pd.read_csv('data/userCopingPotentialArtistGenre.csv', usecols=[0, 1], names=['Userid', 'CopingPotential'])
clusters = pd.read_csv('data/playlistCategories.csv')
clusterPlaylist = clusters.groupby('cluster')['playlist_id'].agg(list)


ups = serendipity_level(playlistOwners, cp)
serendipityCat = serendipity_level_cluster(clusterPlaylist)
