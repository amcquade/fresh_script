import spotipy
import spotipy.util as util
import argparse
import crontab
from crontab import CronTab
import textwrap
import praw

# user object to hold the things
class User:
    def __init__(self, username, client_id, client_secret, redirect, playlists):
        self.username = username
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect = redirect
        self.playlists = playlists
        self.token = self.getToken()

    def getToken(self):
        try:
            token = util.prompt_for_user_token(self.username, 'playlist-modify-public', self.client_id, self.client_secret, self.redirect)

        except:
            # os.remove(f".cache-{username}")
            token = util.prompt_for_user_token(self.username, 'playlist-modify-public', self.client_id, self.client_secret, self.redirect)

        return token

    def getPlaylistsAsString(self):
        return ','.join(self.playlists)

    # convert a string to a bool
    def str2bool(self, v):
        if v.lower() in ('yes', 'true', 't', 'y', '1'):
            return True
        elif v.lower() in ('no', 'false', 'f', 'n', '0'):
            return False
        else:
            raise argparse.ArgumentTypeError('Boolean value expected.')

    # prompt user to add playlists
    def addPlaylists(self):
        offset = 0
        try:
            ownedPlaylists = self.fetchPlaylists(offset)
        except:
            print("You don't have any Spotify playlists!")
            return
        self.printOwnedPlaylists(ownedPlaylists)
        enteringPlaylists = True
        playlistsToAdd = []
        playlistsToAddIndices = []
        while enteringPlaylists:
            print()
            userInput = input('Enter the number of the playlist you would like to add, [N/B] to fetch more/previous playlists, or [Q] to quit: ').strip()
            try:
                index = int(userInput)
                if index < 1 or index > len(ownedPlaylists):
                    raise Exception('Input index out of bounds!')
                if index not in playlistsToAddIndices:
                    playlistsToAdd.append(ownedPlaylists[index-1]['id'])
                    playlistsToAddIndices.append(index)
            except ValueError:
                if userInput.lower() in ('next', 'n', 'more', 'm'):
                    offset = offset + 50
                    try:
                        ownedPlaylists = self.fetchPlaylists(offset)
                    except:
                        print()
                        print("No more playlists to view.")
                        offset = offset - 50
                    finally:
                        self.printOwnedPlaylists(ownedPlaylists)
                elif userInput.lower() in ('back', 'b', 'previous', 'prev', 'p'):
                    offset = offset - 50
                    try:
                        ownedPlaylists = self.fetchPlaylists(offset)
                    except:
                        print()
                        print("No previous playlists to view.")
                        offset = offset + 50
                    finally:
                        self.printOwnedPlaylists(ownedPlaylists)
                elif userInput.lower() in ('quit', 'q'):
                    enteringPlaylists = False
                    continue
                else:
                    print()
                    print("Unexpected input!")
                continue
            except:
                print("That playlist number doesn't exist!")
            enteringPlaylists = self.str2bool(input('Would you like to enter another playlist ID? [Y/N] ').strip())
        self.playlists.extend(playlistsToAdd)

    # fetch playlists given the provided offset
    def fetchPlaylists(self, offset):
        sp = spotipy.Spotify(auth=self.token)
        spotifyPlaylists = sp.current_user_playlists(50, offset)
        if len(spotifyPlaylists['items']) == 0:
            raise Exception('No more playlists to fetch!')
        userId = sp.current_user()['id']
        ownedPlaylists = list(filter(lambda x: x['owner']['id'] == userId and x['id'] not in self.playlists, spotifyPlaylists['items']))
        return ownedPlaylists

    # prints the Spotify playlists that are owned by the user
    def printOwnedPlaylists(self, ownedPlaylists):
        if len(ownedPlaylists) == 0:
            print()
            print("You do not own any playlists in this batch. Type 'n' or 'next' to go to the next one.")
        else:
            for i, playlist in enumerate(ownedPlaylists):
                print()
                print(f"{i+1}. {playlist['name']}")
                print('  total tracks', playlist['tracks']['total'])

    # prompt user to remove current playlists
    def removePlaylists(self):
        removingPlaylists = True
        while removingPlaylists:
            self.printPlaylists()
            index = input('Enter the number of the playlist you would like to remove: ').strip()
            try:
                index = int(index)
                del self.playlists[index-1]
            except:
                print("That playlist number doesn't exist!")
            removingPlaylists = self.str2bool(input('Would you like to remove another playlist? [Y/N] ').strip())

    # print out numbered list of the names of the playlists that are currently being added to
    def printPlaylists(self):
        sp = spotipy.Spotify(auth=self.token)
        print("\nYour current playlists are:")
        for index, playlist in enumerate(self.playlists):
            print(f"{index+1}. {sp.user_playlist(self.username, playlist, 'name')['name']}")
        print()

    # use python-crontab to write a cron task
    def setupCron(self):
        cron = CronTab()
        cron_setting = textwrap.dedent("""\
            ┌───────────── minute (0 - 59)
            │ ┌───────────── hour (0 - 23)
            │ │ ┌───────────── day of month (1 - 31)
            │ │ │ ┌───────────── month (1 - 12)
            │ │ │ │ ┌───────────── day of week (0 - 6) (Sunday to Saturday;
            │ │ │ │ │                                       7 is also Sunday on some systems)
            │ │ │ │ │
            │ │ │ │ │
            * * * * *  command to execute
        """)
        choice = input(cron_setting)

# Reddit class
class RedditData:
    reddit = ""
    sub_reddit = ""

    def __init__(self, sub_reddit, reddit=None):
        self.reddit = praw.Reddit('bot1')
        self.sub_reddit = self.reddit.subreddit(sub_reddit)
