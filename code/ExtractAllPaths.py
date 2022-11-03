from rdflib.extras.external_graph_libs import rdflib_to_networkx_graph
import networkx as nx
import pandas as pd
from os import listdir
from os.path import isfile, join
from rdflib import Graph, Literal, BNode, Namespace, RDF, URIRef
import itertools
import csv
import time
import pandas as pd
import urllib

DB = Namespace('http://dbpedia.org/ontology/')
skos = Namespace('http://www.w3.org/2004/02/skos/core#')

def extractAllPath():
    playlists = [f for f in listdir('data/PlaylistGraphs/') if isfile(join('data/PlaylistGraphs/', f))]

    onlyfiles = [f for f in listdir('data/AllPaths/') if isfile(join('data/AllPaths/', f))]
    playlists_done = [f.replace(".csv","") for f in onlyfiles]

    for playlist in playlists:
        playlistId = playlist.replace(".ttl","")
        if playlistId not in playlists_done:
            print(playlistId)
            playlistGraph = Graph()
            playlistGraph.parse('data/PlaylistGraphsEnriched/%s' %(playlist), format='turtle')
            for s, p, dblink in playlistGraph.triples( (None, skos.closeMatch, None) ):
                part2fix = dblink.replace("http://dbpedia.org/resource/","")
                part2fix = urllib.parse.quote(part2fix)
                dblink = "http://dbpedia.org/resource/%s" %(part2fix)
                dbGraph = Graph()
                dbGraph.parse(dblink)
                playlistGraph = playlistGraph + dbGraph
            pairs_done = []
            G = rdflib_to_networkx_graph(playlistGraph)
            f = open('data/AllPaths/%s.csv' %(playlistId), 'w')
            f.write("Song1,Song2,Pattern,Length\n")
        
            for s1, p, o in playlistGraph.triples( (None, RDF.type, DB.Song) ):
                for s2, p, o in playlistGraph.triples( (None, RDF.type, DB.Song) ):
                    if s1 != s2 and (s1,s2) not in pairs_done:
                        pairs_done.append((s1,s2))
                        pairs_done.append((s2,s1))
                        for path in nx.all_simple_paths(G, s1, s2, cutoff = 6):
                            f.write("%s,%s,\"%s\",%s\n" %(s1,s2,"\t".join(path),str(len(path))))

def extractAllPathsWihtInput(playlists):
    for playlistId in playlists:
           #print(playlistId)
            playlistGraph = Graph()
            playlistGraph.parse('data/PlaylistGraphsEnriched/%s.ttl' %(playlistId), format='turtle')
            for s, p, dblink in playlistGraph.triples( (None, skos.closeMatch, None) ):
                part2fix = dblink.replace("http://dbpedia.org/resource/","")
                part2fix = urllib.parse.quote(part2fix)
                dblink = "http://dbpedia.org/resource/%s" %(part2fix)
                dbGraph = Graph()
                dbGraph.parse(dblink)
                playlistGraph = playlistGraph + dbGraph
            pairs_done = []
            G = rdflib_to_networkx_graph(playlistGraph)
            f = open('data/AllPaths/%s.csv' %(playlistId), 'w')
            f.write("Song1,Song2,Pattern,Length\n")
        
            for s1, p, o in playlistGraph.triples( (None, RDF.type, DB.Song) ):
                for s2, p, o in playlistGraph.triples( (None, RDF.type, DB.Song) ):
                    if s1 != s2 and (s1,s2) not in pairs_done:
                        pairs_done.append((s1,s2))
                        pairs_done.append((s2,s1))
                        for path in nx.all_simple_paths(G, s1, s2, cutoff = 6):
                            f.write("%s,%s,\"%s\",%s\n" %(s1,s2,"\t".join(path),str(len(path))))