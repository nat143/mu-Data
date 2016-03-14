import bs4, requests, time, datetime, csv, operator, sys




api_key = '41311834bebb507fda9e070db4a0904e' # nathan_api



def get_tracks(start_time, limit):

    timmy = time.clock()
    
    url = "http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks" + "&user=" + username + "&page=1" + "&limit=" + str(limit) + "&from=" + str(start_time) + "&api_key=" + api_key
    url_req = requests.get(url, stream=True)
    soup = bs4.BeautifulSoup(url_req.text, "html.parser")
    tag_info = soup.find('recenttracks')
    #page_no = tag_info['page']
    #total_pages = tag_info['totalpages'] # total number of pages for a given username
    total_pages = int(tag_info['totalpages']) # converts to int
    #total_pages = 5
    
    # if the start time is 0 the .csv file will be opened in write mode (erase all previous data and start writing the first row)
    # if the start time is not 0 the file will be opened for appending (new data will be added to the rows at the end)
    if int(start_time) == 0:
        outputFile = open(android_dir + filename, 'w', encoding="utf-8", newline='')
    else:
        outputFile = open(android_dir + filename, 'a', encoding="utf-8", newline='')
    
    outputWriter = csv.writer(outputFile)
    print('start time: {}s' .format(time.clock() - timmy))
    
    num_tracksAdded = 0
    
    for page in range(1, total_pages + 1):
        print('Current page: {}' .format(page))
        time_url_req = time.clock()
        time_page = time_url_req
        url = "http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks" + "&user=" + username + "&page=" + str(page) + "&limit=" + str(limit) + "&from=" + str(start_time) + "&api_key=" + api_key
        url_req = requests.get(url)
        tim = round((time.clock() - time_url_req), 3)
        print('Time take to request url: {}s' .format(tim))
        time_soup = time.clock()
        soup = bs4.BeautifulSoup(url_req.text, "html.parser")
        tim2 = round((time.clock() - time_soup), 3)
        print('Time take to parse url: {}s' .format(tim2))

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
            
        
        tim3 = round((time.clock() - time_data), 3)
        print('Time take to obtain and write data: {}s' .format(tim3))

        tim_2 = round((time.clock() - time_page), 3)
        print('Time take to complete page: {}s' .format(tim_2))

    outputFile.close()
    return num_tracksAdded

#

def sort_csv():

    inputFile = open(android_dir + filename, 'r', encoding="utf-8", newline='')
    inputReader = csv.reader(inputFile)
    inputList = list(inputReader)
    sortedList = sorted(inputList, key=operator.itemgetter(4), reverse=True)

    inputFile.close()

    sortedFile = open(android_dir + filename, 'w', encoding="utf-8", newline='')
    sortedWriter = csv.writer(sortedFile)
    sortedWriter.writerows(sortedList)
    
    sortedFile.close()

#

def update_scrobbles():

    inputFile = open(android_dir + filename, 'r', encoding="utf-8")
    inputList = list(csv.reader(inputFile))
    no_scrobbles = str(len(inputList))
    #print(inputList[0][4])
    #print(type(inputList[0][4]))
    
    # the uts time obtained is increased by 1 second so that the get_tracks function doesn't fetch the last track scrobbled again
    timestamp = int(inputList[0][4]) + 1

    # limit is small value since user is likely fetching a small amout of tracks
    limit = 50

    num_tracksAdded = get_tracks(timestamp, limit)
    print('Number of scrobbles added: {}' .format(num_tracksAdded))
    sort_csv()
#

def scrobbles_viewing(query, title):

    inputFile = open(android_dir + filename, 'r', encoding="utf-8")
    inputReader = csv.reader(inputFile)
    inputData = list(inputReader)
    
    print('Total scrobbles ' + str(len(inputData)))

    if query == 'album artist':
        q = 0
    elif query == 'album':
        q = 1
    elif query == 'track':
        q = 2

    scrobbles = []
    inputFile.seek(0) # restarts the pointer ?
    
    n = 0 # row that is being checked

    for row in inputReader:

        elem = inputData[n][q] # element in the list that is needed
        if title == elem: # n is the row and q is the column
        # if the title is equal to the element of the list append the element to the scrobbles list
            scrobbles.append(elem)

        else:
            pass

        n += 1 # increment the value of n in every iteration of the for loop

    print(len(scrobbles)) # print the length of the list scrobbles

#

def idle():

    while True:
        print('system is idle')
        idle_t = 0
        while idle_t < 600:
            time.sleep(300)
            idle_t += 300
            #print(idle_t)
        
        print('scrobbles are being updated')
        update_scrobbles()
        print('scrobbles have been updated')
#

print('Please enter Last.fm username')
username = input() # asks user for username and inserts given string into variable username
#username = 'povo_yeti'
print('Input filename')
filename = input()
#filename = 'backup.csv'

# if the filename inputted by tge user does not contain the file extension .csv the following lines include it in the string
if filename[(len(filename) - 4):] != '.csv':
    filename = filename + '.csv'

else:
    pass
#

#print(filename)

#filename = 'csv testing update script.csv'

android_dir = ''

while True:
    print('enter command')
    #test_idle = time.clock()
    command = input().lower()
    #command = 'start over'

    if command == 'update':
        update_scrobbles()
    elif command == 'start over':
        start_time = time.clock()
        limit = 1000
        get_tracks(0, limit)
        print('')
        print('finished')
        print("--- %s seconds ---" % (time.clock() - start_time))
    elif command == 'view':
        print('enter query')
        query = input().lower()
        print('enter title')
        title = input().lower()
        scrobbles_viewing(query, title)
    elif command == '':
        break
    elif command == 'idle':
        idle()
    elif command == 'android':
        android_dir =  '/sdcard/'
