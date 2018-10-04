import spotipy.util as util

# user object to hold the things


class User:
    def __init__(self, username, client_id, client_secret, redirect, playlist):
        self.username = username
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect = redirect
        self.playlist = playlist
        self.token = self.getToken()

    def getToken(self):
        try:
            token = util.prompt_for_user_token(self.username, 'playlist-modify-public', self.client_id, self.client_secret, self.redirect)

        except:
            # os.remove(f".cache-{username}")
            token = util.prompt_for_user_token(self.username, 'playlist-modify-public', self.client_id, self.client_secret, self.redirect)

        return token
