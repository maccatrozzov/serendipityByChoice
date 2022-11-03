from rdflib.extras.external_graph_libs import rdflib_to_networkx_graph
import networkx as nx
import pandas as pd
from os import listdir
from os.path import isfile, join
from rdflib import Graph, Literal, BNode, Namespace, RDF, URIRef
import itertools
import csv

DB = Namespace('http://dbpedia.org/ontology/')

mypath = 'data/PlaylistGraphsWithPatterns/'
playlists = [f for f in listdir(mypath) if isfile(join(mypath, f))]

for playlist in playlists:
	playlistId = playlist.replace(".ttl","")
	playlistGraph = Graph()
	playlistGraph.parse('data/PlaylistGraphsWithPatterns/%s' %(playlist),format='turtle')
	
	pairs_done = []
	G = rdflib_to_networkx_graph(playlistGraph)
	f = open('data/ShortestPaths/%s.csv' %(playlistId), 'w')	
	for s1, p, o in playlistGraph.triples( (None, RDF.type, DB.Song) ):
		for s2, p, o in playlistGraph.triples( (None, RDF.type, DB.Song) ):
			if s1 != s2 and (s1,s2) not in pairs_done:
				pairs_done.append((s1,s2))
				pairs_done.append((s2,s1))
				shortestPath = nx.shortest_path(G, s1, s2)
				row = s1 + ", " + s2 + ", " + "\t".join(shortestPath) + ", " + str(len(shortestPath))
				f.write(row)
				f.write('\n')
	