# user obejct to hold the things 
class User:
    def __init__(self, username, client_id, client_secret, redirect, playlist):
        self.username = username
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect = redirect
        self.playlist = playlist
        self.token = getToken(username, client_id, client_secret, redirect)