import math
from scipy.spatial import distance
import pandas as pd
from os.path import isfile, join
from os import listdir
from collections import Counter


def unique(list1): 
  
    # intilize a null list 
    unique_list = [] 
      
    # traverse for all elements 
    for x in list1: 
        # check if exists in unique_list or not 
        if x not in unique_list: 
            unique_list.append(x) 
    return(unique_list)
      
  
def calculateCosine(song1, song2, paths):
	types1 = []
	types2 = []
	
	for index, row in paths.loc[(paths['Song1'] == song1)].iterrows():
		if isinstance(row['Pattern'], str):
			types1.extend(row['Pattern'].replace(' ','').split('\t'))
		else:
			continue
	for index, row in paths.loc[(paths['Song2'] == song1)].iterrows():
		if isinstance(row['Pattern'], str):
			types1.extend(row['Pattern'].replace(' ','').split('\t'))
		else:
			continue	
	frequencies1 = Counter(types1)
	
	for index, row in paths.loc[(paths['Song1'] == song2)].iterrows():
		if isinstance(row['Pattern'], str):
			types2.extend(row['Pattern'].replace(' ','').split('\t'))
		else:
			continue
	for index, row in paths.loc[(paths['Song2'] == song2)].iterrows():
		if isinstance(row['Pattern'], str):
			types2.extend(row['Pattern'].replace(' ','').split('\t'))
		else:
			continue
	frequencies2 = Counter(types2)
	
	frequency1 = { key: frequencies1[key] for key in (frequencies1.keys() & frequencies2.keys())}
	frequency2 = { key: frequencies2[key] for key in (frequencies2.keys() & frequencies1.keys())}
	
	return 1-distance.cosine(list(frequency1.values()), list(frequency2.values()))
	

def getPlaylistCosineSim():
    playlists = [f for f in listdir('data/AllPaths/') if isfile(join('data/AllPaths/', f))]

    playlists_done = [f for f in listdir('data/PlaylistCosineSim/') if isfile(join('data/PlaylistCosineSim/', f))]

    for playlistId in playlists:
        if playlistId not in playlists_done:
            print(playlistId)
            paths = pd.read_csv('data/AllPaths/%s' %(playlistId))
            songs1 = paths['Song1'].unique()
            songs2 = paths['Song2'].unique()
            f = open('data/PlaylistCosineSim/%s' %(playlistId), 'w')	
            f.write('Song1,Song2,CosineSim\n')
            for song1 in songs1:
                for song2 in songs2:
                    cosine = calculateCosine(song1, song2, paths)
                    f.write("%s,%s,%s\n" %(song1, song2, cosine))
	
	