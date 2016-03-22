from flask import Flask, render_template
import json
import os
import string
import math
import urllib

app = Flask(__name__)

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
#

@app.route("/testing")
def index():
    filepath = os.path.join('static', 'json', 'artistsINFO.json')
    artists = json.loads(open(filepath, 'r').read())
    mostListened = artists[0]['listens']
    for item in range(len(artists)):
        artists[item]['percentage'] = artists[item]['listens'] / artists[0]['listens'] * 100
    return render_template("testingartists.html", artists=artists)
#
@app.route("/bootstrap/<int:page_no>")
def bootstrap(page_no):
    valid_chars = "&-_.() %s%s" % (string.ascii_letters, string.digits)
    filepath = os.path.join('static', 'json', 'artistsINFO.json')
    artists = json.loads(open(filepath, 'r').read())
    
    mostListened = artists[0]['listens']
    
    artistsPerPage = 50
    
    total_pages = math.ceil(len(artists) / artistsPerPage)
    
    start_entry = (artistsPerPage*page_no) - artistsPerPage
    end_entry = (artistsPerPage*page_no) - 1
    artists = artists[start_entry:end_entry]
    
    #filenames = []
    
    for entry in artists:
        
        #entry['artist'] = entry['artist']
        currentArtist = entry['artist']
        '''
        if '/' in currentArtist:
            currentArtist = currentArtist.replace('/', ' ')
            #pass
        else:
            pass
            
        imgName = ''.join(c for c in currentArtist if c in valid_chars)
        filename = os.path.join('static', 'images', "ArtistImages", 'small', imgName + '.jpg')
        
        if os.path.isfile(filename):
            # makes sure that the program gets the right filename
            partPath = 'ArtistImages'.replace(' ', '%20')
            artistPath = ''.join(c for c in currentArtist if c in valid_chars)
            artistPath = artistPath.replace(' ', '%20')
            filename = os.path.join('static', 'images', partPath, 'small',  artistPath + '.jpg')
            entry['filename'] = filename
        else:
            #filenames.append(None)
            entry['filename'] = None
        #filename = urllib.parse.quote_plus(filename)
        '''
        entry['filename'] = get_image(currentArtist, 'small')
        
    for item in range(len(artists)):
        artists[item]['percentage'] = artists[item]['listens'] / mostListened * 100
        
    return render_template("testingBootstrap.html", artists=artists, total_pages=total_pages, page_no=page_no)
#
@app.route("/bootstrap/<artist>")
def artist_page(artist):
    valid_chars = "&-_.() %s%s" % (string.ascii_letters, string.digits)
    
    filepath = os.path.join('static', 'json', 'artistsINFO.json')
    artists = json.loads(open(filepath, 'r').read())
    
    filepath = os.path.join('static', 'json', 'albumsINFO.json')
    albums = json.loads(open(filepath, 'r').read())
    
    albumlist = []
    
    getEXTLarge = 0
    
    for entry in albums:
        if entry['artist'] == artist:
            
            if len(albumlist) == 0:
                percentage = 100
            else:
                mostListened = albumlist[0]['listens']
                percentage = entry['listens'] / mostListened * 100
            
            if getEXTLarge == 0:
                filename = get_image(artist, 'extralarge', entry['album'])
                getEXTLarge += 1
            else:
                filename = get_image(artist, 'large', entry['album'])
            
            albumlist.append({'album': entry['album'], 'listens':entry['listens'], 'percentage':percentage, 'filename':filename})
    
    
    artist = {'artist': artist, 'filename': get_image(artist, 'extralarge')}
    
    max_albums = 7
    
    if len(albumlist) < max_albums:
        numAlbums = len(albumlist)
    elif len(albumlist) >= max_albums:
        numAlbums = max_albums
    
    #return render_template("testingalbums.html", albumlist = albumlist ,artist=artist, numAlbums=numAlbums)
    return render_template("Artist-View.html", albumlist = albumlist ,artist=artist, numAlbums=numAlbums)
#

@app.route('/grid')
def grid():
    return render_template("grid.html")

if __name__ == "__main__":
    app.run(debug=True)