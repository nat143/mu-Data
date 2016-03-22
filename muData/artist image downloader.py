import os
import requests
import bs4
import string
import json

os.makedirs('Artist Images small', exist_ok=True)

Artists = json.loads(open('artistImgLinks.json', 'r').read())

for item in Artists:
    if '/' in item['artist']:
        item['artist'] = item['artist'].replace('/', ' ')
    else:
        pass
#
valid_chars = "&-_.() %s%s" % (string.ascii_letters, string.digits)
# !£$%^&()_+{}@~[];'#,.¬`
notfound = []

for item in Artists:
    artist = ''.join(c for c in item['artist'] if c in valid_chars)
    filename = os.path.join('Artist Images small', artist + '.jpg')
    if os.path.isfile(filename) == True:
        pass
    else:
        try:
            print(item['artist'])
            imgUrl = 'http://img2-ak.lst.fm/i/u/' + '34s/' + item['img id']
            print(imgUrl)
            resImg = requests.get(imgUrl)
            resImg.raise_for_status()
            imageFile = open(filename, 'wb')
            for chunk in resImg.iter_content(100000):
                imageFile.write(chunk)
            imageFile.close()
        except:
            notfound.append(artist)
            print('Image not found')
