import pandas as pd
from rdflib import Graph, Literal, BNode, Namespace, RDF, URIRef
from trackGraphBuilder import get_track_graph
from os import listdir
from os.path import isfile, join


def PlaylistGraph(playlists):
	mypath = 'data/PlaylistGraphs/'
	onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
	playlists_done = [f.replace(".ttl","") for f in onlyfiles]

	for i,playlist in playlists.iterrows():
		playlists.loc[playlists['_id'] == playlist['_id'],['_id']] = playlist['_id'].replace("{'$oid': '","").replace("'}","")

	for i,playlist in playlists.iterrows():
		if playlist['_id'] not in playlists_done:
			print(playlist['_id'])
			playlistGraph = Graph()
			tracks = playlist['tracks'].replace("'","").replace("[","").replace("]","").replace(" ", "").split(',')
	   
			for trackId in tracks:
				playlistGraph = playlistGraph + get_track_graph(trackId)
			file_name = 'data/PlaylistGraphs/%s.ttl' %(playlist['_id'])
			playlistGraph.serialize(destination = file_name, format='turtle')
	   
   