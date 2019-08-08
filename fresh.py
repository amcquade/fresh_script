import praw
import re
import sys
import os
import json
import webbrowser
import textwrap
import spotipy
from configparser import ConfigParser, RawConfigParser
import argparse
from constants import pun_dict
from constants import ft_set
from models import User
import cutie

def createUserConfig(user, config_path='.config.ini'):
    """
    Create .config.ini file for Spotify credentials.

    Parameters
    ----------
    user: User object
        Spotify user object.

    config_path: str
        Path to .config.ini.

    """
    s_config = ConfigParser()
    s_config['spotify'] = {
        'client_id': user.client_id,
        'client_secret': user.client_secret,
        'username': user.username,
        'playlist_id': user.getPlaylistsAsString(),
        'redirect_uri': user.redirect
    }

    with open(config_path, 'w') as f:
        s_config.write(f)

def createPrawConfig(client_id, client_secret,
                     praw_path='praw.ini'):
    """
    Create praw.ini file for Reddit credentials.

    Parameters
    ----------
    client_id: str
        Reddit app client id.
    client_secret: str
        Reddit app client secret.
    praw_path: str
        Path to praw.ini.
    """
    r_config = ConfigParser()
    r_config['bot1'] = {
        'client_id': client_id,
        'client_secret': client_secret,
        'user_agent': 'FreshScript'
    }

    with open(praw_path, 'w') as p:
        r_config.write(p)

def createUser():
    user = None
    # read config file
    try:
        if os.path.exists('credentials.json') and not os.path.isfile('.config.ini'):
            # load credentials file
            with open('credentials.json', 'r') as f:
                credentials = json.load(f)

            s_credentials = credentials['spotify']
            p_credentials = credentials['reddit']

            user = User(s_credentials['username'],
                        s_credentials['client_id'],
                        s_credentials['client_secret'],
                        s_credentials['redirect'],
                        []
            )

            user.addPlaylists()

            # write config files
            createUserConfig(user)

            createPrawConfig(p_credentials['client_id'],
                             p_credentials['client_secret'])

        elif not os.path.isfile('.config.ini'):
            print('Credentials file not found!')

            # get credentials
            s_client_id = input('Enter your Spotify Client ID: ').strip()
            s_client_secret = input(
                'Enter your Spotify Client Secret: ').strip()
            username = input('Enter your Username: ').strip()
            redirect = input('Enter your Redirect URI: ').strip()
            r_client_id = input('Enter your Reddit Client ID: ').strip()
            r_client_secret = input(
                'Enter your Reddit Client Secret: ').strip()
            user = User(username, s_client_id, s_client_secret, redirect, [])
            user.addPlaylists()

            # write config files
            createUserConfig(user)
            createPrawConfig(r_client_id, r_client_secret)

        else:
            # parse config
            parser = ConfigParser()
            parser.read('.config.ini')

            # spotify info
            username = parser.get('spotify', 'username')
            playlists = parser.get('spotify', 'playlist_id').split(',')
            s_client_id = parser.get('spotify', 'client_id')
            s_client_secret = parser.get('spotify', 'client_secret')
            redirect = parser.get('spotify', 'redirect_uri')
            user = User(username, s_client_id,
                        s_client_secret, redirect, playlists)

            '''
            TODO
            config['youtube'] = {}
            config['soundcloud'] = {}
            '''
    except Exception as e:
        print(f'config failure: {e}')

    return user


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

    # remove feat from end of title (if not in parentheses/brackets, improves
    # Spotify search results)
    i = 0
    for i in range(len(filtered_title)):
        if filtered_title[i] in ft_set:
            i -= 1
            break
    filtered_title = filtered_title[:i + 1]

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


def manage_playlists(user):
    """
    List, add, and remove playlists.
    Parameters
    ----------
    user : user object
        Object containing all user data.
    """
    user.printPlaylists()

    if cutie.prompt_yes_or_no('Would you like to remove a playlist?'):
        user.removePlaylists()

    if cutie.prompt_yes_or_no('Would you like to add a playlist?'):
        user.addPlaylists()

    user.printPlaylists()
    playlistStr = user.getPlaylistsAsString()

    config = ConfigParser()
    config.read('.config.ini')
    config['spotify']['playlist_id'] = playlistStr
    with open('.config.ini', 'w') as f:
        config.write(f)


def process_args(args, u):
    processed_args = (
        True if args.verbose else False,
        args.limit if args.limit else cutie.get_number('Enter post limit:', 0, 999, False),
        args.sort if args.sort else process_choice_input(),
        args.threshold if args.threshold else None,
        True if args.include_albums else False,
        args.fresh if args.fresh else process_fresh()
    )
    manage_playlists(u) if args.playlists else False
    return processed_args

# process choice selection
def process_choice_input():
    inputPrompt = [
        'Enter your desired sorting method:',
        'hot',
        'new',
        'rising',
        'random_rising',
        'controversial',
        'top'
        ]

    captions = [0]

    prompt = inputPrompt[
        cutie.select(inputPrompt, caption_indices=captions, selected_index=6)]
    return prompt
# process input for fresh arg


def process_fresh():
    return cutie.prompt_yes_or_no('Would you like to only add tracks tagged as [FRESH]?')

def process_subreddit(subreddit, choice, l):
    if choice.lower() == 'hot':
        sub_choice = subreddit.hot(limit=l)
    elif choice.lower() == 'new':
        sub_choice = subreddit.new(limit=l)
    elif choice.lower() == 'rising':
        sub_choice = subreddit.rising(limit=l)
    elif choice.lower() == 'random_rising':
        sub_choice = subreddit.random_rising(limit=l)
    elif choice.lower() == 'controversial':
        sub_choice = subreddit.controversial(limit=l)
    elif choice.lower() == 'top':
        sub_choice = subreddit.top(limit=l)
    else:
        print("Unsupported sorting method")
        sys.exit()
    return sub_choice


def addSpotifyTrack(fresh, threshold, includeAlbums, verbose, sub, tracks):
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
            return

        # If fresh flag given, discard post if not tagged [FRESH]
        if fresh and "[FRESH]" not in sub.title:
            return

        # handle possible query string in url
        url = sub.url.split('?')
        formattedUrl = url[0] if url != None else sub.url

        # handle adding tracks from albums
        if includeAlbums and isMatch.group(1) == 'album':
            tracksInAlbum = spotifyObj.album_tracks(formattedUrl)
            trackIds = [item['external_urls']['spotify']
                        for item in tracksInAlbum['items']]
            tracks.extend(trackIds)
        # handle adding tracks
        elif isMatch.group(1) == 'track':
            tracks.append(formattedUrl)


def main():
    user = createUser()

    argparser = argparse.ArgumentParser(
        formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=40))
    argparser.add_argument("-s", "--sort", help="sort by hot, new, rising, random_rising, controversial or top", type=str,
                           choices=['hot', 'new', 'rising', 'random_rising', 'controversial', 'top'])
    argparser.add_argument(
        "-l", "--limit", help="how many posts to grab", type=int)
    argparser.add_argument(
        "-t", "--threshold", help="only post with score above threshold", type=int)
    argparser.add_argument("-ia", "--include-albums",
                           help="include tracks from albums", action="store_true")
    argparser.add_argument(
        "-v", "--verbose", help="output songs being added and other info", action="store_true")
    argparser.add_argument(
        "-f", "--fresh", help="only add tracks with the [FRESH] tag", action="store_true")
    argparser.add_argument("-p", "--playlists",
                           help="add or remove playlists", action="store_true")

    args = argparser.parse_args()

    # connect to reddit bot
    reddit = praw.Reddit('bot1')
    subreddit = reddit.subreddit('hiphopheads')

    # create spotipy obj
    spotifyObj = spotipy.Spotify(auth=user.token)
    spotifyObj.trace = False
    if args.verbose:
        print('Welcome to the HipHopHeads Fresh Script')
    verbose, l, choice, threshold, includeAlbums, fresh = process_args(
        args, user)
    sub_choice = process_subreddit(subreddit, choice, l)

    tracks = []
    tracks_array = []
    for sub in sub_choice:
        if sub.domain == "open.spotify.com":
            addSpotifyTrack(fresh, threshold, includeAlbums, verbose, sub, tracks)

        else:
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
                            otherDomainList = ['youtu.be', 'youtube.com', 'soundcloud.com']
                            # handle non-spotify posts
                            if sub.domain in otherDomainList and verbose:
                                print("Post: ", sub.title)
                                print("URL: ", sub.url)
                                print("Score: ", sub.score)
                                print("------------------------\n")

                            tracks.append(track_url)
        # handle overflow
        if len(tracks) > 90:
            tracks_array.append(tracks)
            tracks = []

    if len(tracks) > 0:
        tracks_array.append(tracks)

    # handle remove duplicates of tracks before adding new tracks
    if tracks != [] or tracks_array != []:
        try:
            if len(tracks_array) >= 1:
                for tr in tracks_array:
                    for playlist in user.playlists:
                        # retrive information of the tracks in user's playlist
                        existing_tracks = spotifyObj.user_playlist_tracks(
                            user.username, playlist)
                        spotifyObj.user_playlist_remove_all_occurrences_of_tracks(
                            user.username, playlist, tr)
                        results = spotifyObj.user_playlist_add_tracks(
                            user.username, playlist, tr)
                        if verbose:
                            print('New Tracks added to ', spotifyObj.user_playlist(user.username, playlist, 'name')['name'], ': ', abs(
                                existing_tracks['total'] - spotifyObj.user_playlist_tracks(user.username, playlist)['total']))
                            print()
        except:
            if results == [] and verbose:
                print("No new tracks have been added.")
            else:
                print("An error has occured removing or adding new tracks")
        # if verbose:
        #     print(tracks)

if __name__ == '__main__':
    main()
