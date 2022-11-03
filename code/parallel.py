import pandas as pd
from os import listdir
from os.path import isfile, join
import multiprocessing as mp
from ExtractAllPaths import extractAllPathsWihtInput

playlists = [f for f in listdir('data/PlaylistGraphs/') if isfile(join('data/PlaylistGraphs/', f))]
playlistsID = [f.replace(".ttl","") for f in playlists]

onlyfiles = [f for f in listdir('data/AllPaths/') if isfile(join('data/AllPaths/', f))]
playlists_done = [f.replace(".csv","") for f in onlyfiles]


playlistsClean = [i for i in playlistsID if i not in playlists_done]

total = len(playlistsClean)
part = round(total/4)

playlists1 = playlistsClean[0:part]
playlists2 = playlistsClean[(part+1):part*2]
playlists3 = playlistsClean[(part*2)+1:part*3]
playlists4 = playlistsClean[(part*3)+1: total]

p = mp.Pool(4)
p.map(extractAllPathsWihtInput, [playlists1, playlists2, playlists3, playlists4])