import os
import requests
import bs4
import string
import json

os.makedirs('Album Images', exist_ok=True)

Albums = json.loads(open('albumImgLinks.json', 'r').read())

for item in Albums:
    if '/' in item['artist']:
        item['artist'] = item['artist'].replace('/', ' ')
    if '/' in item['album']:
        item['album'] = item['album'].replace('/', ' ')
    else:
        pass
#
valid_chars = "&-_.() %s%s" % (string.ascii_letters, string.digits)
notfound = []

for item in Albums:
    artist = ''.join(c for c in item['artist'] if c in valid_chars)
    album = ''.join(c for c in item['album'] if c in valid_chars)
    filename = os.path.join('Album Images', artist + ' - ' + album + '.jpg')
    if os.path.isfile(filename) == True:
        pass
    else:
        try:
            print(item['artist'])
            print(item['album'])
            imgUrl = 'http://img2-ak.lst.fm/i/u/' + '174s/' + item['img id']
            print(imgUrl)
            resImg = requests.get(imgUrl)
            resImg.raise_for_status()
            imageFile = open(filename, 'wb')
            for chunk in resImg.iter_content(100000):
                imageFile.write(chunk)
            imageFile.close()
        except:
            notfound.append([artist, album])
            print('Image not found')
