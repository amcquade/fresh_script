from flask import Flask, jsonify, render_template, request
from fresh import filter_tags, extract_track_url, addSpotifyTrack, createUser, process_subreddit
from models import RedditData
import spotipy
import prawcore

from xml.sax import saxutils as su

# global objects
app = Flask(__name__)
User = createUser()
Spotify = spotipy.Spotify(auth=User.token)
Spotify.trace = False


'''
Views: Manage all views here
'''
@app.route('/')
def home(Name=None):
  return render_template('index.html', Name=User.username)


@app.route('/tracks', methods=['GET', 'POST'])
def tracks(Name=None):
    sub_reddit = request.form.get('inputvalue').strip()
    tag_choice = request.form.get('taglist')
    reddit_data = ""
    if sub_reddit:
        reddit_data = RedditData(sub_reddit)
        sub_choice = process_subreddit(reddit_data.sub_reddit, tag_choice, 25)
        tracks = []
        titles = []
        images = []
        tracks_array = []
        try:
            for sub in sub_choice:
                if sub.domain == "open.spotify.com":

                    addSpotifyTrack(True, False, False,
                                    False, sub, tracks)
                    titles.append(sub.title)
                    media = sub.media_embed
                    images.append(su.unescape(media['content']))
                    print("spotify media:", media)

                else:
                    # handle non-spotify posts
                    title, tags = filter_tags(sub.title)
                    if 'discussion' not in tags:
                        if 'album' in tags or 'impressions' in tags:
                            # there is a pull request for this feature at the moment
                            # so I will leave it out for now
                            search = Spotify.search(title, type='album')
                        else:
                            search = Spotify.search(title, type='track')
                            if search:
                                track_url = extract_track_url(search)
                                if track_url:
                                    tracks.append(track_url)
                                    titles.append(sub.title)

                                    media = sub.media_embed
                                    print("other media:", media)
                                    if 'content' in media:
                                      s = su.unescape(media['content'])
                                      images.append(s)

                                      print("content media:", s)
                                    else:
                                      images.append(media)
                                      print("other media:", media)

        # zip tracks and info together to be rendered on the tracks page
            track_info = zip(titles, tracks, images)
            return render_template('tracks.html', Name=User.username,
                track_info=track_info, subreddit=reddit_data.sub_reddit)
        except prawcore.exceptions.Redirect:
            track_info = ""
            return render_template('tracks.html', Name=User.username,
                track_info=track_info, subreddit=reddit_data.sub_reddit)
    else:
        track_info = ""
        return render_template('tracks.html', Name=User.username,
            track_info=track_info, subreddit=None)



# @App.route('/get-tracks', methods=['GET', 'POST'])
# def get_tracks():
#   if(request.method == 'GET'):


@app.route('/manage-playlists')
def manage_playlists(Name=None, Playlists=None):
    return render_template('playlists.html', Name=User.username, Playlists=User.playlists)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')
# @App.route('/about')
#   return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True, host='0.0.0.0', port=8300)
