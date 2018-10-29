
def getTracks():
    tracks = []
    tracks_array = []
    for sub in sub_choice:
        if sub.domain == "open.spotify.com":
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
                    continue

                # If fresh flag given, discard post if not tagged [FRESH]
                if fresh and "[FRESH]" not in sub.title:
                    continue

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
        # handle overflow
        if len(tracks) > 90:
            tracks_array.append(tracks)
            tracks = []

    if len(tracks) > 0:
        tracks_array.append(tracks)


def addTracks(tracks, tracks_array):
        # handle remove duplicates of tracks before adding new tracks
    if tracks != [] or tracks_array != []:
        try:
            if len(tracks_array) >= 1:
                for tr in tracks_array:
                    for playlist in user.playlists:
                            # retrive information of the tracks in user's
                            # playlist
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
                print("no new tracks have been added.")
            else:
                print("an error has occured removing or adding new tracks")
        # if verbose:
        #     print(tracks)
