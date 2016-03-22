import os
import string
import urllib

artist = 'Arctic Monkeys'
size = 'small'
valid_chars = "&-_.() %s%s" % (string.ascii_letters, string.digits)

def get_artist_image(artist, size):
    valid_chars = "&-_.() %s%s" % (string.ascii_letters, string.digits)
    
    artist = artist.replace('/', ' ')

    folderpath = os.path.join('static' , 'images', 'ArtistImages')

    imgName = ''.join(c for c in artist if c in valid_chars)

    filename = os.path.join(folderpath, size, imgName + '.jpg')

    if os.path.isfile(filename):
        imgName = urllib.parse.quote(imgName, safe='')
        filename = os.path.join(folderpath, size, imgName + '.jpg')
        return filename
    else:
        print('File not found')
        return None

def get_album_image(artist, album, size):
    valid_chars = "&-_.() %s%s" % (string.ascii_letters, string.digits)
    
    artist = artist.replace('/', ' ')
    album = album.replace('/', ' ')

    folderpath = os.path.join('static' , 'images', 'AlbumImages')

    art_imgName = ''.join(c for c in artist if c in valid_chars)
    alb_imgName = ''.join(c for c in album if c in valid_chars)

    imgName = art_imgName + ' - ' + alb_imgName
    

    filename = os.path.join(folderpath, size, imgName + '.jpg')

    if os.path.isfile(filename):
        imgName = urllib.parse.quote(imgName, safe='')
        filename = os.path.join(folderpath, size, imgName + '.jpg')
        return filename
    else:
        print('File not found')
        return None

def get_image(artist, size, album=None):

    valid_chars = "&-_.() %s%s" % (string.ascii_letters, string.digits)

    if album != None:
        album = album.replace('/', ' ')
        artist = artist.replace('/', ' ')
        folderpath = os.path.join('static' , 'images', 'AlbumImages')
        alb_imgName = ''.join(c for c in album if c in valid_chars)
        art_imgName = ''.join(c for c in artist if c in valid_chars)
        imgName = art_imgName + ' - ' + alb_imgName
    else:
        artist = artist.replace('/', ' ')
        folderpath = os.path.join('static' , 'images', 'ArtistImages')
        imgName = ''.join(c for c in artist if c in valid_chars)
    
    filename = os.path.join(folderpath, size, imgName + '.jpg')

    if os.path.isfile(filename):
        imgName = urllib.parse.quote(imgName, safe='')
        filename = os.path.join(folderpath, size, imgName + '.jpg')
        return filename
    else:
        print('File not found')
        return None
