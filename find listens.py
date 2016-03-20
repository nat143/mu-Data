import os
import csv
import operator
import json
import time

start_time = time.clock()

file = open('C:\\Users\\PC\\Desktop\\VirtualEnvironment\\testing mudata.csv', 'r', encoding="utf-8")

fileReader = csv.reader(file)
fileData = list(fileReader)

artistslist = []
albumslist = []
for subList in fileData:
    artistslist.append(subList[0])
    albumslist.append([subList[0], subList[9]])

# finding artists

uniqueArtists = list(set(artistslist))

artistListens = {}
artistListensList = []

for artist in uniqueArtists:
    listens = 0
    for listen in fileData:
        if listen[0] == artist:
            listens += 1
        else:
            pass
    #artistListens[artist] = listens
    toAppend = {'artist':artist, 'listens':listens}
    artistListensList.append(toAppend)

sortedArtistListens = sorted(artistListensList, key=operator.itemgetter('listens'), reverse=True)

# to search
def searchArtists(artist):
    print(next((item for item in artistListensList if item['artist'] == artist), None))


# finding albums

uniqueAlbums = []

for item in albumslist:
    if item in uniqueAlbums:
        pass
    else:
        uniqueAlbums.append(item)

albumListens = {}
albumListensList = []

for album in uniqueAlbums:
    listens = 0
    for listen in fileData:
        if listen[0] == album[0] and listen[9] == album[1] :
            listens += 1
        else:
            pass
    toAppend = {'artist':album[0], 'album': album[1], 'listens':listens}
    albumListensList.append(toAppend)

sortedAlbumListens = sorted(albumListensList, key=operator.itemgetter('listens'), reverse=True)

# to search
def searchAlbums(artist, album):
    print(next((item for item in albumListensList if item['artist'] == artist and item['album'] == album), None))

json.dump(sortedArtistListens, open('artistListens.json', 'w'))
#to read
artistjson = json.loads(open('artistListens.json', 'r').read())

json.dump(sortedAlbumListens, open('albumListens.json', 'w'))
albumjson = json.loads(open('albumListens.json', 'r').read())

file.close()

print('----------------------------------------------')
print('Time taken: {}' .format(time.clock() - start_time))
print('----------------------------------------------')


# when using an updated csv file change script to include start time
# make script remeber last listen added to json files and update from there
