from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
from os import listdir
from os.path import isfile, join

onlyfiles = [f for f in listdir('data/categories/') if isfile(join('data/categories/', f))]
categories_done = [f.replace(".csv", "") for f in onlyfiles]

sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

cat = {}
categories1 = sp.categories(limit=50, country='IT')
categories2 = sp.categories(limit=50, offset=50, country='IT')
categories3 = sp.categories(limit=50, country='US')
categories4 = sp.categories(limit=50, offset=50, country='US')
categories5 = sp.categories(limit=50, country='NL')
categories6 = sp.categories(limit=50, offset=50, country='NL')
categories7 = sp.categories(limit=50, country='FR')
categories8 = sp.categories(limit=50, offset=50, country='FR')
categories9 = sp.categories(limit=50, country='DE')
categories10 = sp.categories(limit=50, offset=50, country='DE')
categories11 = sp.categories(limit=50, country='AU')
categories12 = sp.categories(limit=50, offset=50, country='AU')
categories13 = sp.categories(limit=50, country='GR')
categories14 = sp.categories(limit=50, offset=50, country='GR')

for c in categories1['categories']['items']:
    cat[c['id']] = c['name']
for c in categories2['categories']['items']:
    cat[c['id']] = c['name']
for c in categories3['categories']['items']:
    cat[c['id']] = c['name']
for c in categories4['categories']['items']:
    cat[c['id']] = c['name']
for c in categories5['categories']['items']:
    cat[c['id']] = c['name']
for c in categories6['categories']['items']:
    cat[c['id']] = c['name']
for c in categories7['categories']['items']:
    cat[c['id']] = c['name']
for c in categories8['categories']['items']:
    cat[c['id']] = c['name']
for c in categories9['categories']['items']:
    cat[c['id']] = c['name']
for c in categories10['categories']['items']:
    cat[c['id']] = c['name']
for c in categories11['categories']['items']:
    cat[c['id']] = c['name']
for c in categories12['categories']['items']:
    cat[c['id']] = c['name']
for c in categories13['categories']['items']:
    cat[c['id']] = c['name']
for c in categories14['categories']['items']:
    cat[c['id']] = c['name']



playlistXcat = {}
print(categories_done)
for c in cat.keys():
    cat_name = cat[c].replace('/', '-')
    if cat_name not in categories_done:
        print(cat_name)
        filename = "data/categories/%s.csv" % cat_name
        out = open(filename, 'w', encoding='utf-8')
        playlistXcat[cat[c]] = []
        try:
            playlists = sp.category_playlists(category_id=c, limit=50, offset=0)['playlists']['items']
            for playlist in playlists:
                try:
                    row = "%s,%s\n" % (c, sp.playlist(playlist['id'])['name'])
                    out.write(row)
                except:
                    continue
            out.close()
        except:
            continue

