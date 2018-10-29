from flask import Flask
from flask import render_template
from fresh import createUser

# global objects
App = Flask(__name__)
User = createUser()

@App.route('/')
def hello_world(Name=None):
	return render_template('index.html', Name=User.username)

# @App.route('/tracks')

@App.route('/manage-playlists')
def manage_playlists(Name=None, Playlists=None):
  return render_template('playlists.html', Name=User.username, Playlists=User.playlists)

