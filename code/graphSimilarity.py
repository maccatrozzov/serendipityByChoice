from rdflib import compare, Graph
import pandas as pd
from rdflib.extras.external_graph_libs import rdflib_to_networkx_graph
import networkx as nx
from os import listdir
from os.path import isfile, join

# compare every pair of songs in a playlist
# save the numbers in a file (so later can decide how to merge)

# 1 get playlist lists
# 2 per playlist, get tracks list
# 3 compare per track pairs

playlists = pd.read_csv('data/filteredSample.csv')

mypath = 'data/PlaylistSimilarity/'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
playlists_done = [f.replace(".csv","") for f in onlyfiles]

for i, playlist in playlists.iterrows():
    playlists.loc[playlists['_id'] == playlist['_id'], ['_id']] = playlist['_id'].replace("{'$oid': '", "").replace("'}", "")

for i, playlist in playlists.iterrows():
    if playlist['_id'] not in playlists_done:
        print(playlist['_id'])
        tracks = playlist['tracks'].replace("'", "").replace("[", "").replace("]", "").replace(" ", "").split(',')

        pairs = [(a, b) for idx, a in enumerate(tracks) for b in tracks[idx + 1:]]
        f = open('data/PlaylistSimilarity/%s.csv' % (playlist['_id']), 'w')
        f.write('trackId1, trackId2, in_both, in_first, in_second\n')

        for trackId1, trackId2 in pairs:
            trackGraph1 = Graph()
            trackGraph1.parse('data/TrackGraphs/%s.ttl' %(trackId1),format='turtle')
            trackGraph2 = Graph()
            trackGraph2.parse('data/TrackGraphs/%s.ttl' % (trackId2), format='turtle')
            iso1 = compare.to_isomorphic(trackGraph1)
            iso2 = compare.to_isomorphic(trackGraph2)
            
            in_both, in_first, in_second = compare.graph_diff(iso1, iso2)
            f.write("%s,%s,%s,%s,%s\n" %(trackId1, trackId2, len(in_both), len(in_first), len(in_second)))

