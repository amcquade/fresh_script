import praw
import re
import sys, os, json, webbrowser
import spotipy
import spotipy.util as util
from configparser import ConfigParser
''' 
# testing with one track
t = []
if len(sys.argv) > 1:
    t.append(sys.argv[1])
    print(t)
else:
    print ("no track supplied")
    sys.exit()
'''
# config 
try:
    if not os.path.isfile('.config.ini'):
        client_id = input('Enter your Client ID: ').strip()
        client_secret = input('Enter your Client Secret: ').strip()
        username = input('Enter your Username: ').strip()
        playlist = input('Enter your Playlist ID: ').strip()        
        redirect = input('Enter your Redirect URI: ').strip()

        config = ConfigParser()
        config['spotify'] = {
            'client_id': client_id,
            'client_secret': client_secret,
            'username': username,
            'playlist_id': playlist,
            'redirect_uri': redirect
        }

        with open('.config.ini', 'w') as f:
            config.write(f)

    else:
        # parse config 
        parser = ConfigParser()
        parser.read('.config.ini')

        # spotify info
        username = parser.get('spotify', 'username')
        playlist = parser.get('spotify', 'playlist_id')
        client_id = parser.get('spotify', 'client_id')
        client_secret = parser.get('spotify', 'client_secret')
        redirect = parser.get('spotify', 'redirect_uri')


    '''
    TODO
    config['youtube'] = {}
    config['soundcloud'] = {}
    '''
except:
    print('config failure')

finally:
    # read config file

    # connect to reddit bot
    reddit = praw.Reddit('bot1')
    subreddit = reddit.subreddit('hiphopheads')

    try:
        token = util.prompt_for_user_token(username, 'playlist-modify-public', client_id, client_secret , redirect)

    except:    
        #os.remove(f".cache-{username}")
        token = util.prompt_for_user_token(username, 'playlist-modify-public', client_id, client_secret, redirect)

    # create spotipy obj
    spotifyObj = spotipy.Spotify(auth=token)
    spotifyObj.trace = False
    tracks = []

    print('Welcome to the HipHopHeads Fresh Script')
    choice = input('Enter 1 to sort by hot, 2 to sort by new: ').strip()
    l = int(input('enter post limit: '))

    if choice == '1':
        sub_choice = subreddit.hot(limit=l)
    elif choice == '2':
        sub_choice = subreddit.new(limit=l)
    else:
        print ("option not supplied")
        sys.exit()    

    for sub in sub_choice:
        if sub.domain == "open.spotify.com":

            # check if post is a track or album
            isTrack = re.search('track', sub.url)
            if isTrack != None:
                print("Post: ", sub.title)
                print("URL: ", sub.url)
                print("Score: ", sub.score)
                print("------------------------\n")

                # handle possible query string in url
                url = sub.url.split('?')
                if url != None:
                    tracks.append(url[0])
                else:
                    tracks.append(sub.url)    
        

    # handle remove duplicates of tracks before adding new tracks
    if tracks is not None:
        try:
            spotifyObj.user_playlist_remove_all_occurrences_of_tracks(username, playlist, tracks)          
            results = spotifyObj.user_playlist_add_tracks(username, playlist, tracks)
        except:
            print("an error has occured removing or adding new tracks")    
        print(tracks)
        print(results)
