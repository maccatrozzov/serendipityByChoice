from DbpediaAlignment import getDBpediaURI
from rdflib import Graph, Literal, BNode, Namespace, RDF, URIRef
from rdflib.namespace import RDF, FOAF, RDFS
import pandas as pd
from os import listdir
from os.path import isfile, join
import time

DB = Namespace('http://dbpedia.org/ontology/')


def getEnrichment(playlists):
    mypath = 'data/PlaylistGraphsEnriched/'
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    playlists_done = [f.replace(".ttl","") for f in onlyfiles]


    for i,playlist in playlists.iterrows():
        playlistId = playlist['_id'].replace("{'$oid': '","").replace("'}","")
        if playlistId not in playlists_done:
            print(playlistId)
            playlistGraph = Graph()
            playlistGraph.parse('data/PlaylistGraphs/%s.ttl' %(playlistId),format='turtle')
            res = playlistGraph.query(''' 
								    SELECT ?artistLabel ?albumLabel ?trackLabel ?artist ?album ?track
								    WHERE { 
								      ?track a DB:Song. 
								      ?track <http://www.w3.org/2000/01/rdf-schema#label> ?trackLabel.
								      ?track DB:album ?album . 
								      ?album <http://www.w3.org/2000/01/rdf-schema#label> ?albumLabel.
								      ?track DB:musicalArtist ?artist.
								      ?artist <http://xmlns.com/foaf/0.1/name> ?artistLabel
								      }
								    ''')
            for row in res:
                [artistURI, albumURI, trackURI, genres, categories] =  getDBpediaURI(row["artistLabel"],row["albumLabel"],row["trackLabel"])
                if artistURI:
                    playlistGraph.add((URIRef(row["artist"]), URIRef("http://www.w3.org/2004/02/skos/core#closeMatch"), URIRef(artistURI)))
                    if albumURI:
                        playlistGraph.add((URIRef(row["album"]), URIRef("http://www.w3.org/2004/02/skos/core#closeMatch"), URIRef(albumURI)))
                        if genres:
                            if isinstance(genres, list):
                                for genre in genres:
                                    playlistGraph.add((URIRef(row["album"]), URIRef("http://dbpedia.org/ontology/genre"), URIRef(genre)))
                            else:
                                playlistGraph.add((URIRef(row["album"]), URIRef("http://dbpedia.org/ontology/genre"), URIRef(genres)))
                        if categories:
                            if isinstance(categories, list):
                                for category in categories:
                                    playlistGraph.add((URIRef(row["album"]), URIRef("http://purl.org/dc/terms/subject"), URIRef(category)))
                            else:
                                playlistGraph.add((URIRef(row["album"]), URIRef("http://purl.org/dc/terms/subject"), URIRef(categories)))
                        if trackURI:
                            playlistGraph.add((URIRef(row["track"]), URIRef("http://www.w3.org/2004/02/skos/core#closeMatch"), URIRef(trackURI)))
                time.sleep(1)
            file_name = '%s%s.ttl' %(mypath, playlistId)
            playlistGraph.serialize(destination=file_name, format='turtle')

def getArtistGenre(playlists):
    mypath = 'data/PlaylistGraphsEnrichedArtistGenre/'
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    playlists_done = [f.replace(".ttl", "") for f in onlyfiles]


    for i,playlist in playlists.iterrows():
        playlistId = playlist['_id'].replace("{'$oid': '","").replace("'}","")
        if playlistId not in playlists_done:
            print(playlistId)
            playlistGraph = Graph()
            playlistGraph.parse('data/PlaylistGraphs/%s.ttl' %(playlistId),format='turtle')
            res = playlistGraph.query('''
                                      SELECT ?artistLabel ?artist
                                      WHERE { 
                                      ?track DB:musicalArtist ?artist.
                                      ?artist <http://xmlns.com/foaf/0.1/name> ?artistLabel}
                                      ''')
            for row in res:
                [artistURI, genres] = getDBpediaURI(row["artistLabel"], "None", "None")
                if artistURI:
                    # playlistGraph.add((URIRef(row["artist"]), URIRef("http://www.w3.org/2004/02/skos/core#closeMatch"), URIRef(artistURI)))
                    if genres:
                        if isinstance(genres, list):
                            for genre in genres:
                                playlistGraph.add((URIRef(row["artist"]), URIRef("http://dbpedia.org/ontology/genre"), URIRef(genre)))
                        else:
                            playlistGraph.add((URIRef(row["artist"]), URIRef("http://dbpedia.org/ontology/genre"), URIRef(genres)))
                time.sleep(1)
            file_name = '%s%s.ttl' %(mypath, playlistId)
            playlistGraph.serialize(destination=file_name, format='turtle')