import pandas as pd


playlists = pd.read_csv("data/filteredSample.csv")

for i, playlist in playlists.iterrows():
	playlists.loc[playlists['_id'] == playlist['_id'], ['_id']] = playlist['_id'].replace("{'$oid': '", "").replace("'}", "")

playlistNames = playlists.groupby('_id')['name'].agg(list)
print(len(playlists))
print(len(playlistNames))
for playlist, name in playlistNames.iteritems():
	print(name)