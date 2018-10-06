import praw
import re
import sys, os, json, webbrowser
import spotipy
from configparser import ConfigParser
import argparse
from models import User
from constants import pun_dict
from constants import ft_set


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


def filter_tags(title):
    """
    Removes tags from post title and adds them to a set.

    Any tags such as [FRESH], (feat. J-Bobby), etc. will be removed from the title
    and placed in a set (without surrounding punctuation). Titles are also lower-cased
    and any dashes/extra white space are removed.

    Parameters
    ----------
    title : str
        The non-spotify Reddit post title to be filtered.

    Returns
    -------
    filtered_title : str
        The filtered post title.
        
    tags : set
        Container for any removed tags.
    """

    tags = set()
    filtered_title = []

    # separate tags from title
    # assumes there are no erroneous parentheses/brackets
    # ex. [FRESH] Lil Pump - Nice 2 Yeet ya [prod. by D4NNY]
    # there may be issues if song name contains parentheses
    tag = []
    last_pun = None
    add_to_tag = False
    for character in title:
        character = character.lower()
        # beginning of tag
        if character == '[' or character == '(':
            if add_to_tag:
                tag.append(character)
            else:
                last_pun = character
                add_to_tag = True
        # end of tag
        elif character == ']' or character == ')':
            if add_to_tag:
                if pun_dict[character] == last_pun:
                    # separate multi-word tags
                    for add_tag in ''.join(tag).split():
                        tags.add(add_tag)
                    tag.clear()
                    add_to_tag = False
                else:
                    tag.append(character)
        # remove dashes if they occur outside of tags
        elif character != '-':
            if add_to_tag:
                tag.append(character)
            else:
                filtered_title.append(character)

    # remove extra spaces from title
    filtered_title = ''.join(filtered_title).split()

    # remove feat from end of title (if not in parentheses/brackets, improves Spotify search results)
    i = 0
    for i in range(len(filtered_title)):
        if filtered_title[i] in ft_set:
            i -= 1
            break
    filtered_title = filtered_title[:i+1]

    filtered_title = ' '.join(filtered_title)
    return filtered_title, tags


def extract_track_url(search):
    """
    Get the first Spotify track url from a given search.

    Extended description of function.

    Parameters
    ----------
    search : dict
        Contains information relating to Spotify API track search request.

    Returns
    -------
    url : str
        Spotify URL for the first track received from search query.
    """

    if 'tracks' in search:
        tracks = search['tracks']
        if 'items' in tracks:
            items = tracks['items']
            # take the first url we can find
            for item in items:
                if 'external_urls' in item:
                    external_urls = item['external_urls']
                    if 'spotify' in external_urls:
                        url = external_urls['spotify']
                        return url


def main():
    user = createUser()

    argparser = argparse.ArgumentParser()
    argparser.add_argument("-s", "--sort", help="sort by hot or new", type=int)
    argparser.add_argument("-l", "--limit", help="how many posts to grab", type=int)
    argparser.add_argument("-v", "--verbose", help="output songs being added and other info", action="store_true")
    args = argparser.parse_args()
    
    verbose = True if args.verbose else False
    l = args.limit if args.limit else False
    choice = args.sort if args.sort else None
            
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
        print("option not supplied")
        sys.exit()

    for sub in sub_choice:
        if sub.domain == "open.spotify.com":
            # check if post is a track or album
            isTrack = re.search('track', sub.url)
            if isTrack:
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
        else:
            # handle non-spotify posts
            title, tags = filter_tags(sub.title)
            if 'discussion' not in tags:
                if 'album' in tags or 'impressions' in tags:
                    # there is a pull request for this feature at the moment
                    # so I will leave it out for now
                    search = spotifyObj.search(title, type='album')
                else:
                    search = spotifyObj.search(title, type='track')
                    if search:
                        track_url = extract_track_url(search)
                        if track_url:
                            tracks.append(track_url)

    # handle remove duplicates of tracks before adding new tracks
    if tracks != []:
        try:
            spotifyObj.user_playlist_remove_all_occurrences_of_tracks(user.username, user.playlist, tracks)
            results = spotifyObj.user_playlist_add_tracks(user.username, user.playlist, tracks)
        except:
            if results == [] and verbose:
                print("no new tracks have been added.")
            else:
                print("an error has occurred removing or adding new tracks")
        if verbose:
            print(tracks)
            print(results)


if __name__ == '__main__':
    main()
