import bs4
import requests
import time
import csv
import operator
import sys
import json
import threading
import pprint

api_key = '41311834bebb507fda9e070db4a0904e'

def get_link(page, limit, lock):
    print('Current page: {}' .format(page))
    
    url_page = "http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&extended=1" + "&user=" + username + "&page=" + str(page) + "&limit=" + str(limit) + "&from=" + str(start_time) + "&api_key=" + api_key
    #print(url_page)
    url_page_req = requests.get(url_page)
    url_page_req.raise_for_status()
    acq = 0
    # checks if the list is locked, if it is locked the thread waits, if it isnt locked the thread locks it and write to the list
    print(lock.locked())
    while acq != 1:
        print('Page {} trying to acquire lock' .format(page))
        if lock.locked() == False:
            lock.acquire()
            print('Lock aquired, page {}' .format(page))
            pageRequests.append(url_page_req)
            acq = 1
            lock.release()
            print('Page {} has released lock' .format(page))
        else:
            print('Page {} could not aquire lock' .format(page))
        

def get_tracks(start_time, limit):
    # finds total number of pages
    url = "http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&extended=1" + "&user=" + username + "&page=1" + "&limit=" + str(limit) + "&from=" + str(start_time) + "&api_key=" + api_key
    url_req = requests.get(url)
    url_req.raise_for_status()
    soup = bs4.BeautifulSoup(url_req.text, "html.parser")
    total_pages = int(soup.find('recenttracks')['totalpages'])
    print(total_pages)
    
    #if int(start_time) == 0:
        # write to output file
    #else:
        # append to output file
    
    num_tracksAdded = 0
    
    ###
    # num_Threads has to be a FACTOR of total_pages
    num_Threads = 71
    CurrentPage = 1
    downloadThreads = []
    while CurrentPage != total_pages + 1:
        print('CurrentPage {}' .format(CurrentPage))
        # number of threads to open
        # for loop with a range from the current page to (currentpage + num_Threads)
        # depending on the value of num_Threads, threads will be open simultanouesly
        
        for i in range(CurrentPage, (CurrentPage + num_Threads)):
            print('for loop: cur page {}, num_thre {}, i {}' .format(CurrentPage, num_Threads, i))
            downloadThread = threading.Thread(target=get_link, args=(i, limit, lock))
            downloadThreads.append(downloadThread)
            downloadThread.start()
            print('Im here, {}' .format(CurrentPage))
        
        for downloadThread in downloadThreads:
            downloadThread.join()
        
        CurrentPage += num_Threads
    ###
    print('----------------------------------------------------------')
    print('number of pages requested: {}' .format(len(pageRequests)))
    print('----------------------------------------------------------')
    
    for page in range(len(pageRequests)):
        print("The soup's page: {}" .format(page))
        soup_page = bs4.BeautifulSoup(pageRequests[page].text, "html.parser")
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
            artist = tag_artist.find('name').string
            #print(artist)
            artist_mbid = tag_artist.find('mbid').string
            artist_lastfm_url = tag_artist.find('url').string
            images = tag_artist.find_all('image')
            # NOTE all images have similar urls
            # change???
            artist_img_sml = images[0].string
            artist_img_mdm = images[1].string
            artist_img_lrg = images[2].string
            artist_img_extlrg = images[3].string
            loved = tag_curTrack.loved.string
            title = tag_curTrack.find_all('name')[1].string
            album = tag_curTrack.album.string
            album_mbid = tag_curTrack.album['mbid']
            track_url = tag_curTrack.find_all('url')[1].string
            # album images
            album_images = tag_curTrack.find_all('image')[-4:]
            album_img_sml = album_images[0].string
            album_img_mdm = album_images[1].string
            album_img_lrg = album_images[2].string
            album_img_extlrg = album_images[3].string
            unix_timestamp = tag_curTrack.date['uts']
            
            data = [artist, artist_mbid, artist_lastfm_url, artist_img_sml, artist_img_mdm, artist_img_lrg, artist_img_extlrg,loved, title, album, album_mbid, track_url, album_img_sml, album_img_mdm, album_img_lrg, album_img_extlrg, unix_timestamp]
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
#
def sort_csv():

    inputFile = open(filename, 'r', encoding="utf-8", newline='')
    inputReader = csv.reader(inputFile)
    inputList = list(inputReader)
    sortedList = sorted(inputList, key=operator.itemgetter(16), reverse=True)

    inputFile.close()

    sortedFile = open(filename, 'w', encoding="utf-8", newline='')
    sortedWriter = csv.writer(sortedFile)
    sortedWriter.writerows(sortedList)
    
    sortedFile.close()
#
username = 'povo_yeti'
#limit = 200
start_time = 0
filename = 'testing mudata.csv'

outputFile = open(filename, 'w', encoding="utf-8", newline='')
outputWriter = csv.writer(outputFile)

lock = threading.Lock()
pageRequests = []
get_tracks(0, 200)
outputFile.close()
sort_csv()