
import os, sys, csv
from os import path
from dataclasses import dataclass
import datetime
import pickle

from itertools import islice

def take(n, iterable):
    return list(islice(iterable, n))

@dataclass
class Song:
    title: str
    album: str
    artist: str

    def __hash__(self):
        return (hash(self.title) ^ hash(self.album)) ^ hash(self.artist)

@dataclass
class Entry:
    song: Song
    time: datetime.datetime
    n: int

#if path.exists(filename + ".pkl"):
#    with open(filename + ".pkl", "rb") as ifstream:
#        data = pickle.load(ifstream)
    
#else:

items = [("My last year:", "output_1yr"), ("All-time:", "output")]

def run(item):
    data = []
    total_ms = 0

    song_dict = {}

    with open(item[1] + ".csv", "r+") as f:
        if f.readable():
            print("Had to parse csv file")
            data = list(csv.reader(f, delimiter='\t'))[1:]
            print("Data read")
        with open(item[1] + ".pkl", "wb") as out:
            print("Saved to pickle file")
            pickle.dump(data, out, pickle.HIGHEST_PROTOCOL)

    for s in data:
        # s[11] = title, s[9] = album, s[10] = artist
        new_song = Song("", "", s[10])

        if new_song in song_dict and s[10] != "":
            song_dict[new_song] += int(s[13])
        else:
            song_dict[new_song] = int(s[13])

        total_ms += int(s[13])

    top_ten = []
    for k in sorted(song_dict, key=song_dict.get, reverse=True):
        top_ten.append("\u001b[33m" + str(k.artist) + "\u001b[0m: " + str(int(song_dict[k] / 60000)) + " \u001b[32mmin\u001b[0m")

    for k in sorted(song_dict, key=song_dict.get, reverse=True):
        top_ten.append("\u001b[33m" + str(k.artist) + "\u001b[0m: " + str(int(song_dict[k] / 60000)) + " \u001b[32mmin\u001b[0m")

    print("\u001b[1m" + item[0] + "\u001b[0m")

    for i in range(0, 25):
        print(str(i+1) + ".\t" + top_ten[i])

    print(len(data))

    print("\u001b[1mTotal in ms: \u001b[0m" + str(total_ms))

if __name__ == '__main__':
    for t in items:
        run(t)