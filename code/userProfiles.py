import pandas as pd
from rdflib import Graph, Literal, BNode, Namespace, RDF, URIRef

DB = Namespace('http://dbpedia.org/ontology/')

playlists = pd.read_csv("data/filteredSample.csv")
# patterns = pd.read_csv("data/ShortestPathsAnalysis.csv", names=["playlistId", "types", "length"])

for i, playlist in playlists.iterrows():
	playlists.loc[playlists['_id'] == playlist['_id'],['_id']] = playlist['_id'].replace("{'$oid': '","").replace("'}","")

playlistOwner = playlists.groupby('owner')['_id'].agg(list)

coping = open('data/userCopingPotentialArtistGenre.csv', 'w')
# analysisFile = open('data/analysisFile.csv', 'w')
coping.write("Userid, CopingPotential\n")
# analysisFile.write("userid, copingPotential, playlistid, lengthPattern, typePattern")

for owner, playlists in playlistOwner.iteritems():
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
		# patterns.loc[playlistId, "playlistId"]
		# analysisFile.write(str(owner) + "," + str(len(genres)) + "," + str(playlistId) + "," + "," + "\n" )
				
	coping.write(str(owner) + "," + str(len(genres)) + "\n")
	
	