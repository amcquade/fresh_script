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
        userId = sp.current_user()['id']
        ownedPlaylists = list(filter(lambda x: x['owner']['id'] == userId, spotifyPlaylists['items']))
        for i, playlist in enumerate(ownedPlaylists):
            print()
            print(f"{i+1}. {playlist['name']}")
            print('  total tracks', playlist['tracks']['total'])
        print()
        enteringPlaylists = True
        playlistsToAdd = []
        playlistsToAddIndices = []
        while enteringPlaylists:
            index = input('Enter the number of the playlist you would like to add: ').strip()
            try:
                index = int(index)
                if index < 1 or index > len(ownedPlaylists):
                    raise Exception('Input index out of bounds!')
                if index not in playlistsToAddIndices:
                    playlistsToAdd.append(ownedPlaylists[index-1]['id'])
                    playlistsToAddIndices.append(index)
            except:
                print("That playlist number doesn't exist!")
            enteringPlaylists = self.str2bool(input('Would you like to enter another playlist ID? [Y/N] ').strip())
        self.playlists.extend(playlistsToAdd)

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