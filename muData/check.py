import json
import sys
import csv

file = open('testing mudata2.csv' ,'r')
read = csv.reader(file)
listens = list(read)
file.close()

print('{} in csv file' .format(len(listens)))

testingArtists = json.loads(open('artistsINFO.json', 'r').read())
totalListens = 0
for item in testingArtists:
    totalListens += int(item['listens'])
print('{} in artists file' .format(totalListens))
#

testingAlbums = json.loads(open('albumsINFO.json', 'r').read())
totalListens = 0
for item in testingAlbums:
    totalListens += int(item['listens'])
#
print('{} in albums files' .format(totalListens))

inp = input()
if inp == '':
    sys.exit()
else:
    sys.exit()
