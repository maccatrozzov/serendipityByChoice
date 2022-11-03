from sentence_transformers import SentenceTransformer
import pandas as pd
from bertopic import BERTopic


model = SentenceTransformer('all-MiniLM-L6-v2')
playlists = pd.read_csv("data/filteredSample.csv")

for i, playlist in playlists.iterrows():
	playlists.loc[playlists['_id'] == playlist['_id'], ['_id']] = playlist['_id'].replace("{'$oid': '", "").replace("'}", "")
	playlists.loc[playlists['_id'] == playlist['_id'], ['_id']] = playlist['name'].replace('_', ' ')

# playlists['embedding'] = 0

# for index, row in playlists.iterrows():
# 	# print(row['_id'])
# 	row['embedding'] = model.encode(row['name'], convert_to_tensor=True)

topic_model = BERTopic(embedding_model="all-MiniLM-L6-v2")
topics, probs = topic_model.fit_transform(playlists['name'].replace('_', ' '))
print(topic_model.get_topic_info())

