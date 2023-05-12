import pandas as pd
import numpy as np
import scipy 
import sympy 
import requests
import spotipy

from SPARQLWrapper import SPARQLWrapper, JSON
from spotipy.oauth2 import SpotifyClientCredentials
from rdflib import Graph, Literal, BNode, Namespace, RDF, URIRef
from rdflib.namespace import RDF, FOAF, RDFS, XSD

## Get tracks info from spotify and build the graph

SP = Namespace('https://open.spotify.com/')
DB = Namespace('http://dbpedia.org/ontology/')

sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

	
def get_track_graph(trackId):
	trackGraph = Graph()
	try:
		trackGraph.parse("data/TrackGraphs/%s.ttl" %(trackId),format="turtle")
	except:
		#trackId = '5EauMVTXVoQOkax03XXVaV'
		print(trackId)
		lz_uri = 'spotify:track:%s' %(trackId)

		trackGraph = Graph()
		file_name = 'data/TrackGraphs/%s.ttl' % (trackId)
		#try:
		results = sp.track(lz_uri)

		trackGraph.add((SP['track/'+trackId], RDF['type'], DB['Song']))
		trackGraph.add((SP['track/'+trackId], RDFS['label'], Literal(results['name'])))

		trackGraph.add((SP['track/'+trackId], DB['musicalArtist'], URIRef(results['album']['artists'][0]['external_urls']['spotify'])))
		trackGraph.add((URIRef(results['album']['artists'][0]['external_urls']['spotify']),FOAF['name'],Literal(results['album']['artists'][0]['name'])))
		trackGraph.add((URIRef(results['album']['artists'][0]['external_urls']['spotify']),FOAF['name'],Literal(results['album']['artists'][0]['name'])))

		trackGraph.add((SP['track/'+trackId], DB['album'], URIRef(results['album']['external_urls']['spotify'])))
		trackGraph.add((URIRef(results['album']['external_urls']['spotify']),RDFS['label'],Literal(results['album']['name'])))
		trackGraph.add((URIRef(results['album']['external_urls']['spotify']),DB['artist'],URIRef(results['album']['artists'][0]['external_urls']['spotify'])))

		trackGraph.add((SP['track/'+trackId], DB['releaseDate'], Literal(results['album']['release_date'])))

		trackGraph.add((SP['track/'+trackId], DB['duration'], Literal(results['duration_ms'], datatype=XSD.integer)))


		trackGraph.bind("DB",DB)
		trackGraph.bind("SP",SP)
		trackGraph.bind("FOAF",FOAF)

		trackGraph.serialize(destination = file_name, format='turtle')
		#except:
		#	trackGraph.serialize(destination=file_name, format='turtle')
	print(trackGraph)
	return(trackGraph)

  
