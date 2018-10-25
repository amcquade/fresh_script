from flask import Flask
from flask import render_template
from fresh import createUser
app = Flask(__name__)
user = createUser()

@app.route('/')
def hello_world(Name=None):
	return render_template('index.html', Name=user.username)

@app.route('/manage-playlists')
def manage_playlists(Name=None, Playlists=None):
  return render_template('playlists.html', Name=user.username, Playlists=user.playlists)
