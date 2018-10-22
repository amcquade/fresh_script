import spotipy
import spotipy.util as util

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

    # this is just a copy of the function from the other file. 
    # it probably should be pulled out into a utility class
    def str2bool(self, v):
        if v.lower() in ('yes', 'true', 't', 'y', '1'):
            return True
        elif v.lower() in ('no', 'false', 'f', 'n', '0'):
            return False
        else:
            raise argparse.ArgumentTypeError('Boolean value expected.')

    # prompt user to add playlists
    def addPlaylists(self):
        sp = spotipy.Spotify(auth=self.token)
        spotifyPlaylists = sp.current_user_playlists()
        for playlist in spotifyPlaylists['items']:
            #if playlist['owner']['id'] == self.username:
            print()
            print(playlist['owner']['id'])
            print(playlist['name'])
            print('  total tracks', playlist['tracks']['total'])
        enteringPlaylists = True
        while enteringPlaylists:
            self.playlists.append(input('Enter your Playlist ID: ' ).strip())
            enteringPlaylists = self.str2bool(input('Would you like to enter another playlist ID? [Y/N] ').strip())

    # prompt user to remove playlists
    def removePlaylists(self):
        removingPlaylists = True
        while removingPlaylists:
            self.printPlaylists(playlistsCopy)
            index = input('Enter the number of the playlist you would like to remove: ').strip()
            try:
                index = int(index)
                del self.playlists[index-1]
            except:
                print("That playlist number doesn't exist!")
            removingPlaylists = self.str2bool(input('Would you like to remove another playlist? ').strip())

    # print out numbered list of playlists
    def printPlaylists(self):
        print("\nYour current playlists are:")
        for index, playlist in enumerate(self.playlists):
            print(f"{index+1}. {playlist}")
        print()