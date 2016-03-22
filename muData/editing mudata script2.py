import bs4
import requests
import time
import csv
import operator
import sys
import json
import threading
import pprint
import os

api_key = '41311834bebb507fda9e070db4a0904e'

def get_link(page, limit, lock, start):
    #print('Current page: {}' .format(page))
    
    url_page = "http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&extended=1" + "&user=" + username + "&page=" + str(page) + "&limit=" + str(limit) + "&from=" + str(start) + "&api_key=" + api_key
    #print(url_page)
    url_page_req = requests.get(url_page)
    url_page_req.raise_for_status()
    locks_acquired = 0
    # checks if the list is locked, if it is locked the thread waits, if it isnt locked the thread locks it and write to the list
    #print(lock.locked())
    while locks_acquired != 1:
        #print('Page {} trying to acquire lock' .format(page))
        if lock.locked() == False:
            lock.acquire()
            #print('Lock aquired, page {}' .format(page))
            pageRequests.append(url_page_req)
            locks_acquired = 1
            lock.release()
            #print('Page {} has released lock' .format(page))
        else:
            print('Page {} could not aquire lock' .format(page))
#
def remove_item(remList, artist, album):
    for item in remList:
        if item['artist'] == artist and item['album'] == album:
            #print('item found')
            remList.remove(item)
            break
        #else:
            #print('not found')
#

def addlistensAlbum(artist, album, givenList, mbid, imgID):
    Dict = next((item for item in givenList if item['artist'] == artist and item['album'] == album), None)
    #print(Dict)
    if Dict != None:
        #print('Already present')
        listens = Dict['listens']
        #print(listens)
        remove_item(givenList, artist, album)
        givenList.append({'listens': listens + 1, 'artist':artist, 'album': album, 'mbid':mbid, 'img id': imgID})
        #print(next((item for item in givenList if item['artist'] == artist), None))
    else:
        #print('Not Found')
        givenList.append({'listens': 1, 'artist':artist, 'album': album, 'mbid':mbid, 'img id': imgID})
        #print(next((item for item in givenList if item['artist'] == artist), None))



def addlistens(artist, givenList, mbid=None, imgID=None):
    Dict = next((item for item in givenList if item['artist'] == artist), None)
    if Dict != None:
        #print('Already present')
        listens = Dict['listens'] + 1
        #print(listens)
        givenList[:] = [d for d in givenList if d.get('artist') != artist]
        givenList.append({'artist':artist, 'mbid':mbid , 'img id':imgID, 'listens': listens})
    else:
        #print('Not Found')
        listens = 1
        givenList.append({'artist':artist, 'mbid':mbid , 'img id':imgID, 'listens': listens})


def get_tracks(start, limit):
    # finds total number of pages
    url = "http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&extended=1" + "&user=" + username + "&page=1" + "&limit=" + str(limit) + "&from=" + str(start) + "&api_key=" + api_key
    url_req = requests.get(url)
    url_req.raise_for_status()
    soup = bs4.BeautifulSoup(url_req.text, "html.parser")
    total_pages = int(soup.find('recenttracks')['totalpages'])
    print(total_pages)
    
    if int(start) == 0:
        # write to output file
        outputFile = open(filename, 'w', encoding="utf-8", newline='')
    else:
        # append to output file
        outputFile = open(filename, 'a', encoding="utf-8", newline='')
    
    # json files
    if start == 0:
        artistJson = []
        albumJson = []
    else:
        try:
            artistJson = json.loads(open('artistsINFO.json', 'r').read())
        except FileNotFoundError:
            print('Artist info file not found, creating new list')
            artistJson = []
        try:
            albumJson = json.loads(open('albumsINFO.json' , 'r').read())
        except FileNotFoundError:
            print('Album info file not found, creating new list')
            albumJson = []
    
    outputWriter = csv.writer(outputFile)
    
    num_tracksAdded = 0
    
    ###
    # num_Threads has to be a FACTOR of total_pages
    #num_Threads = 71
    CurrentPage = 1
    downloadThreads = []
    
    max_num_Threads = 10
    num_Threads = max_num_Threads
    pages_left = total_pages
    print(pages_left)
    
    #while CurrentPage < total_pages + 1:
    pages_time = time.clock()
    while pages_left > 0:
        print('CurrentPage {}' .format(CurrentPage))
        # number of threads to open
        # for loop with a range from the current page to (currentpage + num_Threads)
        # depending on the value of num_Threads, threads will be open simultanouesly
        
        if pages_left < num_Threads:
            num_Threads = pages_left
            print('----------------------------------------------------------')
            print('Number of threads has been decreased to {}' .format(num_Threads))
            print('----------------------------------------------------------')
        
        for i in range(CurrentPage, (CurrentPage + num_Threads)):
            print('for loop: cur page {}, num_thre {}, i {}' .format(CurrentPage, num_Threads, i))
            downloadThread = threading.Thread(target=get_link, args=(i, limit, lock, start))
            downloadThreads.append(downloadThread)
            downloadThread.start()
            print('Im here, {}' .format(CurrentPage))
        
        for downloadThread in downloadThreads:
            downloadThread.join()
        
        pages_left = total_pages - len(pageRequests)
        print('Pages left {}' .format(pages_left))
        CurrentPage += num_Threads
    ###
    print('----------------------------------------------------------')
    print('number of pages requested: {}' .format(len(pageRequests)))
    print('----------------------------------------------------------')
    print('Time to get all requests: {}' .format(time.clock() - pages_time))
    
    for page in range(len(pageRequests)):
        cur_page_time = time.clock()
        print("The soup's page: {}" .format(page))
        soup_time = time.clock()
        soup_page = bs4.BeautifulSoup(pageRequests[page].text, "html.parser")
        print("Time to make soup: {}" .format(time.clock() - soup_time))
        tag_time = time.clock()
        tag_allTracks = soup_page.find_all('track')
        num_tracks = len(tag_allTracks)
        #print('Number of tracks in current page: {}' .format(num_tracks))
        
        # checks if there is a track that is currently playing, in which case it skips it
        try:
            tag_allTracks[0]['nowplaying']
            print('hey')
            start = 1
        except:
            start = 0
        
        for track in range(start, num_tracks):
            tag_curTrack = tag_allTracks[track]
            tag_artist = tag_curTrack.artist
            artist = tag_artist.find('name').string.replace('&apos;', "'")
            #print(artist)
            artist_mbid = tag_artist.find('mbid').string
            #artist_lastfm_url = tag_artist.find('url').string
            images = tag_artist.find_all('image')
            # NOTE all images have similar urls
            # change???
            try:
                artist_img = images[0].string[-36:-4]
            except:
                print('-----------------------------------------------------------')
                print('Artist image not found, artist:{} track:{}' .format(artist, title))
                print('-----------------------------------------------------------')
                artist_img = ''
            #artist_img_sml = images[0].string
            #artist_img_mdm = images[1].string
            #artist_img_lrg = images[2].string
            #artist_img_extlrg = images[3].string
            loved = tag_curTrack.loved.string
            title = tag_curTrack.find_all('name')[1].string.replace('&apos;', "'")
            album = tag_curTrack.album.string
            try:
                album = album.replace('&apos;', "'")
            except:
                pass
            album_mbid = tag_curTrack.album['mbid']
            #track_url = tag_curTrack.find_all('url')[1].string
            # album images
            unix_timestamp = tag_curTrack.date['uts']
            album_images = tag_curTrack.find_all('image')[-4:]
            try:
                album_img = album_images[0].string[-36:-4]
            except:
                try:
                    print('-----------------------------------------------------------')
                    print('Album image not found, artist:{} track:{}' .format(artist, title))
                    print('-----------------------------------------------------------')
                    album_img = ''
                except:
                    print('-----------------------------------------------------------')
                    print('-----------------------------------------------------------')
                    print('-----------------------------------------------------------')
                    print('Could not print artist and track name')
                    print(unix_timestamp)
                    print('-----------------------------------------------------------')
                    print('-----------------------------------------------------------')
                    print('-----------------------------------------------------------')
                    
            #album_img_sml = album_images[0].string
            #album_img_mdm = album_images[1].string
            #album_img_lrg = album_images[2].string
            #album_img_extlrg = album_images[3].string
            
            addlistens(artist, artistJson, artist_mbid, artist_img)
            addlistensAlbum(artist, album, albumJson, album_mbid, album_img)
            
            #data = [artist, artist_mbid, artist_lastfm_url, artist_img_sml, artist_img_mdm, artist_img_lrg, artist_img_extlrg,loved, title, album, album_mbid, track_url, album_img_sml, album_img_mdm, album_img_lrg, album_img_extlrg, unix_timestamp]
            data = [artist, album, title, loved, unix_timestamp]
            newdata = []
            try:
                for item in range(len(data)):
                    if None == data[item]:
                        newdata.append(None)
                    elif '&apos;' in data[item]:
                        newdata.append(data[item].replace('&apos;', "'"))
                    elif '' == data[item]:
                        newdata.append('')
                    else:
                        newdata.append(data[item])
            except:
                pprint.pprint(data)
            outputWriter.writerow(newdata)
            
            num_tracksAdded += 1
            #pprint.pprint(data)
        print('Tag time {}' .format(time.clock() - tag_time))
        print('Page time {}' .format(time.clock() - cur_page_time))
    
    artistJson = sorted(artistJson, key=operator.itemgetter('listens'), reverse=True)
    json.dump(artistJson, open('artistsINFO.json', 'w'))
    albumJson = sorted(albumJson, key=operator.itemgetter('listens'), reverse=True)
    json.dump(albumJson, open('albumsINFO.json', 'w'))
    
    outputFile.close()
    sort_csv()
    return num_tracksAdded
#
def sort_csv():

    inputFile = open(filename, 'r', encoding="utf-8", newline='')
    inputReader = csv.reader(inputFile)
    inputList = list(inputReader)
    sortedList = sorted(inputList, key=operator.itemgetter(4), reverse=True)

    inputFile.close()

    sortedFile = open(filename, 'w', encoding="utf-8", newline='')
    sortedWriter = csv.writer(sortedFile)
    sortedWriter.writerows(sortedList)
    
    sortedFile.close()
#
def update_listens():
    
    inputFile = open(filename, 'r', encoding="utf-8")
    inputList = list(csv.reader(inputFile))
    inputFile.close()
    timestamp = int(inputList[0][4]) + 1
    
    limit = 50
    
    num_tracksAdded = get_tracks(timestamp, limit)
    print('Number of scrobbles added: {}' .format(num_tracksAdded))
    sort_csv()
#
username = 'povo_yeti'
filename = os.path.join('testing mudata2.csv')

while True:
    command = input('Enter command: ').lower()
    
    if command == 'update':
        lock = threading.Lock()
        pageRequests = []
        update_listens()
    elif command == 'start over':
        lock = threading.Lock()
        pageRequests = []
        startTime = time.clock()
        limit = 200
        get_tracks(0 , limit)
        print('Time taken: {}s' .format(time.clock() - startTime))
    elif command == '':
        break
        