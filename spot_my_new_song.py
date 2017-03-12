# Slightly modified spotipy tutorial code. Just making sure this works. :)

import spotipy
sp = spotipy.Spotify()

max = 10

results = sp.search(q='Animal Collective', limit=max)
for i, t in enumerate(results['tracks']['items']):
    print(' %2d' % (i + 1), t['name'])