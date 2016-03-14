import requests, bs4, threading, time

downloadThreads = []
api_key = '41311834bebb507fda9e070db4a0904e' # nathan_api

def down_link(page):
    #print('Page {} started' .format(page))
    url = "http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks" + "&user=" + username + "&page=" + str(page) + "&limit=" + str(limit) + "&api_key=" + api_key
    url_req = requests.get(url)
    all_reqs.append(url_req)
    #print('Finished page {}' .format(page))


start_time = time.clock()
print('Requesting links')
page = 1
#url = "http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks" + "&user=povo_yeti&page=" + str(page) + "&limit=1000&from=0&api_key=" + api_key
#print(url)
downloadTreads = []
all_reqs = []

limit = 200
username = 'povo_yeti'
url = "http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks" + "&user=" + username + "&page=1" + "&limit=" + str(limit) + "&api_key=" + api_key
url_req = requests.get(url)
soup = bs4.BeautifulSoup(url_req.text, "html.parser")
tag_info = soup.find('recenttracks')
total_pages = int(tag_info['totalpages'])

n = 1
m = total_pages + 2
print(m)
testing = 0

for i in range(n, m ):
    testing = testing + limit
    downloadThread = threading.Thread(target=down_link, args=[i])
    downloadThreads.append(downloadThread)
    downloadThread.start()

for downloadThread in downloadThreads:
    downloadThread.join()
#
print('Total time taken: {}s' .format(time.clock() - start_time))
'''
start_time = time.clock()
print('Making soups')
grandtag = []
total = 0
for i in range(n - 1,m - 1):
    soup = bs4.BeautifulSoup(all_reqs[i].text, "html.parser")
    tag_allTracks = soup.find_all('track')
    try:
        tag_allTracks[0]['nowplaying']
        print('hey')
        total = total + len(tag_allTracks) - 1
        print('im here')
    except:
        total = total + len(tag_allTracks)
    grandtag.append(tag_allTracks)
    #print('Page {} has {} tracks' .format((i+1), (len(tag_allTracks))))
print('Total time taken: {}s' .format(time.clock() - start_time))
'''
'''
grandtag2 = []

def make_soup(page):
    soup = bs4.BeautifulSoup(all_reqs[page].text, "html.parser")
    tag_allTracks2 = soup.find_all('track')
    grandtag2.append(tag_allTracks2)
    
start_time = time.clock()
print('Making soups')
total = 0
soups = []

for i in range(n - 1,m - 1):
    soupthread = threading.Thread(target=make_soup, args=[i])
    soups.append(soupthread)
    soupthread.start()
    #print('Page {} has {} tracks' .format((i+1), (len(tag_allTracks))))

for sou in soups:
    soupthread.join()
print('Total time taken: {}s' .format(time.clock() - start_time))
'''
num_tracksAdded = 0

import csv

filename = 'testing multithreading.csv'

outputFile = open(filename, 'w', encoding="utf-8", newline='')
outputWriter = csv.writer(outputFile)
parsing = obwrdata = pages = 0
for page in range(0, m - 1):
    time_page = time.clock()
    #print('Current page: {}\r' .format(page))
    #all_reqs
    time_soup = time.clock()
    soup = bs4.BeautifulSoup(all_reqs[page].text, "html.parser")
    parsing = parsing + time.clock() - time_soup
    tim2 = round((time.clock() - time_soup), 3)
    #print('Time take to parse url: {}s' .format(tim2))

    time_data = time.clock()

    tag_allTracks = soup.find_all('track')
    num_tracks = len(tag_allTracks)

    #print('')

    #print(num_tracks)
    
    
    # try tp find the element 'nowplaying' in the first tag. if that element is present the next for loop will skip that track (its the track that is currently playing), otherwise start at the first track
    try:

        tag_allTracks[0]['nowplaying']
        print('hey')
        start = 1
        print('im here')

    except:

        start = 0

    for track in range(start, num_tracks):

        #print('current track: ' + str(track + 1))

        tag_curTrack = tag_allTracks[track]
        track_artist = tag_curTrack.artist.string
        track_album = tag_curTrack.album.string
        track_title = tag_curTrack.find('name').string
        track_curTrackdate = tag_curTrack.date
        track_timestamp_nor = track_curTrackdate.string   # gets the readable timestamp of the track from the tag
        track_timestamp_uts = track_curTrackdate['uts']   # gets the unix time timestamp of the track from the tag
        outputWriter.writerow([track_artist, track_album, track_title, track_timestamp_nor, track_timestamp_uts])
        num_tracksAdded += 1
        
    obwrdata = obwrdata + time.clock() - time_data
    tim3 = round((time.clock() - time_data), 3)
    #print('Time take to obtain and write data: {}s' .format(tim3))

    pages = pages + time.clock() - time_page
    tim_2 = round((time.clock() - time_page), 3)
    #print('Time take to complete page: {}s' .format(tim_2))

outputFile.close()
