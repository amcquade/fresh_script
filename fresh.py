import praw
import re
import sys, os, json, webbrowser
import spotipy
import spotipy.util as util
from configparser import ConfigParser
import argparse
from models import User

# convert a string to a bool
def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

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
    # token = getToken(user.username, user.client_id, user.client_secret, user.redirect)    

    argparser = argparse.ArgumentParser()
    argparser.add_argument("-s", "--sort", help="sort by hot or new", type=int)
    argparser.add_argument("-l", "--limit", help="how many posts to grab", type=int)
    argparser.add_argument("-t", "--threshold", help="only post with score above threshold", type=int)
    argparser.add_argument("-v", "--verbose", help="output songs being added and other info", action="store_true")
    args = argparser.parse_args()
    
    verbose = True if args.verbose else False
    l = args.limit if args.limit else False
    choice = args.sort if args.sort else None
    threshold = args.threshold if args.threshold else None
            
    # connect to reddit bot
    reddit = praw.Reddit('bot1')
    subreddit = reddit.subreddit('hiphopheads')

    # create spotipy obj
    spotifyObj = spotipy.Spotify(auth=user.token)
    spotifyObj.trace = False
    tracks = []

    if verbose:
        print('Welcome to the HipHopHeads Fresh Script')
    
    if not choice:
        choice = int(input('Enter 1 to sort by hot, 2 to sort by new: '))

    if not l:    
        l = int(input('enter post limit: '))

    if choice == 1:
        sub_choice = subreddit.hot(limit=l)
    elif choice == 2:
        sub_choice = subreddit.new(limit=l)
    else:
        print ("option not supplied")
        sys.exit()

    for sub in sub_choice:
        if sub.domain == "open.spotify.com":

            # check if post is a track or album
            isTrack = re.search('track', sub.url)
            if isTrack != None:
                if verbose:
                    print("Post: ", sub.title)
                    print("URL: ", sub.url)
                    print("Score: ", sub.score)
                    print("------------------------\n")
		
                # Discard post below threshold if given
                if threshold and sub.score < threshold:
                    continue

                # handle possible query string in url
                url = sub.url.split('?')
                if url != None:
                    tracks.append(url[0])
                else:
                    tracks.append(sub.url)


    # handle remove duplicates of tracks before adding new tracks
    if tracks != []:
        try:
            spotifyObj.user_playlist_remove_all_occurrences_of_tracks(user.username, user.playlist, tracks)
            results = spotifyObj.user_playlist_add_tracks(user.username, user.playlist, tracks)
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
