import os
import requests
import bs4
import string
import json

def get_images(size):
    
    if size == 'small':
        sizeLink = '34s/'
    elif size == 'medium':
        sizeLink = '64s/'
    elif size == 'large':
        sizeLink = '174s/'
    elif size == 'extralarge':
        sizeLink = '300x300/'
    elif size == 'full':
        sizeLink = ''
    
    os.makedirs('Album Images ' + str(size), exist_ok=True)
    valid_chars = "&-_.() %s%s" % (string.ascii_letters, string.digits)
    
    Albums = json.loads(open('albumsINFO.json', 'r').read())
    print(len(Albums))

    for item in Albums:
        if item['album'] == None:
            pass
        else:
            if '/' in item['artist']:
                item['artist'] = item['artist'].replace('/', ' ')
                
                print('I made it')
            if '/' in item['album']:
                item['album'] = item['album'].replace('/', ' ')
            else:
                pass
            notfound = []
            
            artist = ''.join(c for c in item['artist'] if c in valid_chars)
            album = ''.join(c for c in item['album'] if c in valid_chars)
            filename = os.path.join('Album Images ' + str(size), artist + ' - ' + album + '.jpg')
            if os.path.isfile(filename) == True:
                pass
            else:
                try:
                    print(item['artist'])
                    print(item['album'])
                    imgUrl = 'http://img2-ak.lst.fm/i/u/' + sizeLink + item['img id']
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
#

com = input('Enter size of images required: ')
get_images(com)
