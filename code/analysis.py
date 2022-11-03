import pandas as pd
from os.path import isfile, join
from os import listdir

#playlists = [f for f in listdir('data/PlaylistCosineSim/') if isfile(join('data/PlaylistCosineSim/', f))]
data = pd.read_json("data/playlists.json", lines = True)
coping = pd.read_csv("data/userCopingPotential.csv")
playlist2use = pd.read_csv("data/playlist16.csv")
outfile = open("data/analysisData.csv", "w")
outfile.write("playlistId,owner,copingPotential,context,length,cosSimMean,cosSimVar,cosSimMin,cosSimMax\n")

for index, row in coping.iterrows():
	userId = row['Userid']
	userCoping = row['CopingPotential']
	playlists = data.loc[data['owner'] == userId,'_id']
	for p in playlists:
		playlistId = p['$oid']
		length = list(data.loc[data['_id'] == p,'tracks'].map(len))
		outfile.write(playlistId + ',' + str(length[0])+'\n') 
	break

print(length[0])
	