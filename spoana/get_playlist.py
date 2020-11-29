import spotipy
import sys
import os
import json
from pprint import pprint
from time import sleep
from spotipy.oauth2 import SpotifyClientCredentials
from collections import namedtuple

class Track:
    def __init__(self, track_name, album_name, release_date, album_uri, artists, artist_uri, duration_ms, popularity, track_number, track_uri):
        self.track_name = track_name
        self.album_name = album_name
        self.release_date = release_date
        self.album_uri = album_uri
        self.artists = artists
        self.artist_uri = artist_uri
        self.duration_ms = duration_ms
        self.popularity = popularity
        self.track_number = track_number
        self.track_uri = track_uri
        self.danceability = 0
        self.energy = 0
        self.key = 0
        self.mode = 0
        self.loudness = 0
        self.speechiness = 0
        self.acousticness = 0
        self.instrumentalness = 0
        self.liveness = 0
        self.valence = 0
        self.tempo = 0
        self.time_signature = 0

    def populate_features(self, da, en, ke, mo, lo, sp, ac, ins, li, va, te, ti):
        self.danceability = da
        self.energy = en
        self.key = ke
        self.mode = mo
        self.loudness = lo
        self.speechiness = sp
        self.acousticness = ac
        self.instrumentalness = ins
        self.liveness = li
        self.valence = va
        self.tempo = te
        self.time_signature = ti


#setup
playlist_uri = 'spotify:playlist:0Cat7SXwGpQlxAzueXcELF'

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())

total_songs = sp.playlist_tracks(playlist_uri)
print(total_songs['total'])
print(total_songs)

name = sp.playlist(playlist_uri, fields='name')
playlist_name = name['name']

offset = 0

file = open("output.json", "w+")

list_tracks = []

tracks = []

def parse_features(response, offset, total_songs):
    #print("\n\n" + str(response[0]))
    for i in range(0, len(response)):
        #print(i + offset)
        r = response[i]
        if i + offset < total_songs:
            list_tracks[i + offset].populate_features(r['danceability'], r['energy'], r['key'], r['mode'], r['loudness'], r['speechiness'], r['acousticness'], r['instrumentalness'], r['liveness'], r['valence'], r['tempo'], r['time_signature'])

#create track object
def create_track(track_string):
    #print(track_string)
    s = track_string['track']
    new_track = Track(s['name'], s['album']['name'], s['album']['release_date'], s['album']['uri'], s['artists'][0]['name'], s['artists'][0]['uri'], s['duration_ms'], s['popularity'], s['track_number'], s['uri'])
    list_tracks.append(new_track)

#loop to fetch tracks
while True:
    response = sp.playlist_tracks(playlist_uri, fields='items(track(id,album(name,release_date,uri),artists,duration_ms,explicit,name,popularity,track_number,uri))', limit=100, offset=offset, additional_types=['track'])
    #x = json.loads(json.dumps(response), object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
    #tracks.append(x)
    offset = offset + len(response['items'])
    #print(offset, "/", total_songs)

    for i in range(0, len(response['items'])):
        create_track(response['items'][i])

    sleep(0.1) #avoid being rate limited

    if len(response['items']) == 0:
        break

#file.write(json.dumps(ltracks))
file.close()

#loop over tracks and request audio features
list_track_uris = []

#create track uri list
for i in range(0, len(list_tracks)):
    list_track_uris.append(list_tracks[i].track_uri)

offset = 0
length = 100
while True:
    response = sp.audio_features(list_track_uris[offset:offset+length])
    print(response)
    print(offset, "/", total_songs)
    parse_features(response, offset, total_songs['total'])
    offset = offset + length

    if offset > len(list_track_uris):
        break

features = open(playlist_name + ".csv", "w+")

attrs = vars(list_tracks[0])
features.write('; '.join("%s" % item[0] for item in attrs.items()) + "\n")

for t in list_tracks:
    attrs = vars(t)
    features.write('; '.join("%s" % item[1] for item in attrs.items()) + "\n")

features.close()

#analysis = sp.audio_analysis(list_tracks[0].track_uri)
analysis = sp.audio_analysis("spotify:track:6DxKG8EHEqkWdKrFQSvm32")

ana = open('track.json', "w+")
ana.write(json.dumps(analysis))
ana.close()

print(analysis)

#print(len(ltracks))

