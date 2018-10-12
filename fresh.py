import praw
import re
import sys, os, json, webbrowser, textwrap
import spotipy
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
                #request playlist ids, store as array and then set the playlist variable to a comma separated list
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
            playlist = parser.get('spotify', 'playlist_id') #returns a comma separated list of playlists
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

    return User(username, client_id, client_secret, redirect, playlist) #playlist represents c.s. list of playlists


def main():
    user = createUser()

    argparser = argparse.ArgumentParser()
    argparser.add_argument("-s", "--sort", help="sort by hot or new", type=int)
    argparser.add_argument("-l", "--limit", help="how many posts to grab", type=int)
    argparser.add_argument("-t", "--threshold", help="only post with score above threshold", type=int)
    argparser.add_argument("-ia", "--include-albums", help="include tracks from albums", action="store_true")
    argparser.add_argument("-v", "--verbose", help="output songs being added and other info", action="store_true")
    args = argparser.parse_args()

    verbose = True if args.verbose else False
    l = args.limit if args.limit else False
    choice = args.sort if args.sort else None
    threshold = args.threshold if args.threshold else None
    includeAlbums = True if args.include_albums else False

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
        inputPrompt = textwrap.dedent("""\
        Enter the number of your desired sorting method:
            1 - Hot
            2 - New
            3 - Rising
            4 - Random Rising
            5 - Controversial
            6 - Top
        """)
        choice = int(input(inputPrompt))

    if not l:
        l = int(input('enter post limit: '))

    if choice is 1:
        sub_choice = subreddit.hot(limit=l)
    elif choice is 2:
        sub_choice = subreddit.new(limit=l)
    elif choice is 3:
        sub_choice = subreddit.rising(limit=l)
    elif choice is 4:
        sub_choice = subreddit.random_rising(limit=l)
    elif choice is 5:
        sub_choice = subreddit.controversial(limit = l)
    elif choice is 6:
        sub_choice = subreddit.top(limit=l)
    else:
        print ("option not supplied")
        sys.exit()

    for sub in sub_choice:
        if sub.domain == "open.spotify.com":

            # check if post is a track or album
            isMatch = re.search('(track|album)', sub.url)
            if isMatch != None:
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
                formattedUrl = url[0] if url != None else sub.url

                # handle adding tracks from albums
                if includeAlbums and isMatch.group(1) == 'album':
                    tracksInAlbum = spotifyObj.album_tracks(formattedUrl)
                    trackIds = [item['external_urls']['spotify'] for item in tracksInAlbum['items']]
                    tracks.extend(trackIds)
                # handle adding tracks
                elif isMatch.group(1) == 'track':
                    tracks.append(formattedUrl)

    # handle remove duplicates of tracks before adding new tracks
    if tracks != []:
        try:
            #convert comma separated list of laylists to array then for loop for every playlist
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
