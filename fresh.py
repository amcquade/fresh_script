import praw
import re
import sys, os, json, webbrowser
import spotipy
import spotipy.util as util
from configparser import ConfigParser

import argparse

# convert a string to a bool
def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

# user obejct to hold the things 
class User:
    def __init__(self, username, client_id, client_secret, redirect, playlist):
        self.username = username
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect = redirect
        self.playlist = playlist
        self.token = getToken(username, client_id, client_secret, redirect)

def createUser():
    # read config file
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

    return User(username, client_id, client_secret, redirect, playlist)
            

def getToken(username, client_id, client_secret, redirect):
    try:
        token = util.prompt_for_user_token(username, 'playlist-modify-public', client_id, client_secret , redirect)

    except:
        #os.remove(f".cache-{username}")
        token = util.prompt_for_user_token(username, 'playlist-modify-public', client_id, client_secret, redirect)

    return token


def main():
    user = createUser()
    choice = None
    l = None
    verbose = True
    # token = getToken(user.username, user.client_id, user.client_secret, user.redirect)    

    argparser = argparse.ArgumentParser()
    argparser.add_argument("-s", "--sort", help="sort by hot or new", type=int)
    argparser.add_argument("-l", "--limit", help="how many posts to grab", type=int)
    argparser.add_argument("-v", "--verbose", help="output songs being added and other info", type=str2bool)
 
    if(len(sys.argv) > 1):
        args = argparser.parse_args()
        if args.sort is not None:
            choice = args.sort
        if args.limit is not None:
            l = args.limit            
        if args.verbose is not None:
            verbose = args.verbose
            
    # connect to reddit bot
    reddit = praw.Reddit('bot1')
    subreddit = reddit.subreddit('hiphopheads')

    # create spotipy obj
    spotifyObj = spotipy.Spotify(auth=user.token)
    spotifyObj.trace = False
    tracks = []


    if verbose:
        print('Welcome to the HipHopHeads Fresh Script')
    
    if choice is None:
        choice = int(input('Enter 1 to sort by hot, 2 to sort by new: '))

    if l is None:    
        l = int(input('enter post limit: '))
        
    if choice == 1:
        sub_choice = subreddit.hot(limit=l)
    elif choice == 2:
        sub_choice = subreddit.new(limit=l)
    else:
        print ("option not supplied")
        sys.exit()

    for sub in sub_choice:
        #print(sub.domain)
        if sub.domain == "open.spotify.com":

            # check if post is a track or album
            isTrack = re.search('track', sub.url)
            print(isTrack)
            if isTrack != None:
                if verbose:
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
    if tracks != []:
        try:
            #retrive information of the tracks in user's playlist
            existing_tracks = spotifyObj.user_playlist_tracks(user.username,user.playlist)
            #count the number of tracks in the playlist
            n_old_tracks =len(existing_tracks['items'])
            spotifyObj.user_playlist_remove_all_occurrences_of_tracks(user.username, user.playlist, tracks)
            results = spotifyObj.user_playlist_add_tracks(user.username, user.playlist, tracks)
            #retrieve the information of the tracks after adding them
            current_tracks = spotifyObj.user_playlist_tracks(user.username,user.playlist)
            #count the number of new tracks 
            n_new_tracks = abs(n_old_tracks - len(current_tracks['items']))
            print('New Tracks:')
            print(n_new_tracks)
        except: 

            if results == [] and verbose:
                print("no new tracks have been added.")
            else:
                print("an error has occured removing or adding new tracks")
        if verbose:
            print(tracks)
            
            print(results)
            
if __name__ == '__main__':
    main()