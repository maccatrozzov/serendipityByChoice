from SPARQLWrapper import SPARQLWrapper, JSON
sparql = SPARQLWrapper("http://dbpedia.org/sparql")	


# build query incrementally
# first, get the artist uri
# if found, then get the album uri
# if found, then get the track uri

def runQuery(query):
	sparql.setQuery(query)
	sparql.setReturnFormat(JSON)
	query_result = sparql.query().convert()	
	try:
		results = []
		for res in query_result["results"]["bindings"]:
			results.append(res["uri"]["value"])
		if len(results) == 1:
			return results[0]
		elif len(results) == 0:
			return None
		else:
			return results
	except:
		return None
	
def artistQuery(label):
	query =  """
			   SELECT  ?uri
			   WHERE { 
				?uri <http://xmlns.com/foaf/0.1/name> "%s"@en.
				?uri a <http://dbpedia.org/ontology/MusicalArtist>.
				}
			 """ %(label.replace('"',''))
	return query
	
def albumQuery(artistURL,label):
	query =  """
			   SELECT  ?uri
			   WHERE { 
				?uri <http://xmlns.com/foaf/0.1/name> "%s"@en.
				?uri a <http://dbpedia.org/ontology/Album>.
				?uri <http://dbpedia.org/ontology/artist> <%s>.
				}
			 """ %(label.replace('"',''),artistURL)
	return query		 

def trackQuery(albumURL,label):			 
	query =  """
			   SELECT  ?uri
			   WHERE { 
			   	<%s> <http://dbpedia.org/property/title> ?uri.
				?uri <http://xmlns.com/foaf/0.1/name> "%s"@en.
				}
			 """ %(albumURL,label.replace('"',''))
	
	return query
	
def getGenres(albumURL):
	query =  """
			   SELECT ?uri
			   WHERE { 
			   	<%s> <http://dbpedia.org/ontology/genre> ?uri.
				}
			 """ %(albumURL)	
	return query

def getCategories(albumURL):
	query =  """
			   SELECT  ?uri
			   WHERE { 
			   	<%s> <http://purl.org/dc/terms/subject> ?uri.
				}
			 """ %(albumURL)	
	return query
	
def getDBpediaURI(artist, album, track):
	artist = artist.replace("/\\", "")
	artistURL = runQuery(artistQuery(artist))

	if (artistURL and album == "None" and track == "None"):
		if isinstance(artistURL, list):
			artistURLS = artistURL
			for artistURL in artistURLS:
				genres = runQuery(getGenres(artistURL))
				return[artistURL, genres]
		else:
			genres = runQuery(getGenres(artistURL))
			return [artistURL, genres]
	elif(not(artistURL)):
		return [None, None]

	elif (artistURL and album != "None" and track != "None"):
		if isinstance(artistURL, list):
			artistURLS = artistURL
			for artistURL in artistURLS:
				albumURL = runQuery(albumQuery(artistURL,album))
				if albumURL:
					if isinstance(albumURL, list):
						albumURLS = albumURL
						for albumURL in albumURLS:
							trackURL = runQuery(trackQuery(albumURL,track))
							genres = runQuery(getGenres(albumURL))
							categories = runQuery(getCategories(albumURL))
							if trackURL:
								return[artistURL, albumURL, trackURL, genres, categories]
						if not trackURL:
							return[artistURL, None, None, None, None]
				else:
					return[None,None,None,None,None]
		else:
			albumURL = runQuery(albumQuery(artistURL,album))
			if albumURL:
				if isinstance(albumURL, list):
					albumURLS = albumURL
					for albumURL in albumURLS:
						trackURL = runQuery(trackQuery(albumURL,track))
						genres = runQuery(getGenres(albumURL))
						categories = runQuery(getCategories(albumURL))
						if trackURL:
							return[artistURL, albumURL, trackURL, genres, categories]
					if not trackURL:
						return[artistURL, None, None, None, None]
				else:
					trackURL = runQuery(trackQuery(albumURL,track))
					genres = runQuery(getGenres(albumURL))
					categories = runQuery(getCategories(albumURL))
					if trackURL:
						return[artistURL, albumURL, trackURL, genres, categories]
					else:
						return[artistURL, albumURL, None, genres, categories]
			else:
				return[artistURL,None,None,None,None]
	else:
		return[None,None,None,None,None]
		



