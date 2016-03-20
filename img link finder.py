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
    try:
        artistslist.append([subList[0],subList[3][-36:]])
    except:
        artistslist.append([subList[0],None])
    try:
        albumslist.append([subList[0], subList[9], subList[12][-36:]])
    except:
        albumslist.append([subList[0], subList[9], None])
#

url_beg = 'http://img2-ak.lst.fm/i/u/'
sizes = {'sml':'34s', 'mdm':'64s', 'lrg':'174s', 'extlrg':'300x300'}

uniqueArtists = []

for item in artistslist:
    if item in uniqueArtists:
        pass
    else:
        uniqueArtists.append(item)
#


artistImages = []

for entry in uniqueArtists:
    toAppend = {'artist':entry[0], 'img id': entry[1]}
    artistImages.append(toAppend)


# to search
def searchArtists(artist):
    print(next((item for item in artistImages if item['artist'] == artist), None))


uniqueAlbums = []

for item in albumslist:
    if item in uniqueAlbums:
        pass
    else:
        uniqueAlbums.append(item)


albumImages = []

for entry in uniqueAlbums:
    toAppend = {'artist':entry[0],'album': entry[1], 'img id': entry[2]}
    albumImages.append(toAppend)

# ###########################################################
# to search
def searchAlbums(artist, album):
    print(next((item for item in albumImages if item['artist'] == artist and item['album'] == album), None))

json.dump(artistImages, open('artistImgLinks.json', 'w'))
#to read
artistjson = json.loads(open('artistImgLinks.json', 'r').read())

json.dump(albumImages, open('albumImgLinks.json', 'w'))
albumjson = json.loads(open('albumImgLinks.json', 'r').read())

file.close()

print('----------------------------------------------')
print('Time taken: {}' .format(time.clock() - start_time))
print('----------------------------------------------')


# when using an updated csv file change script to include start time
# make script remeber last listen added to json files and update from there
