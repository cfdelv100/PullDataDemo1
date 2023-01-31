import spotipy

spotify = spotipy.Spotify(client_credentials_manager=spotipy.oauth2.SpotifyClientCredentials())


def get_artists_from_playlists(playlist_url):
    """
    :param playlist_url: A playlist to analyze
    :return: A dictionary of all primary artists in a playlist.
    """
    artists = {}
    playlist_tracks = spotify.playlist_tracks(playlist_id=playlist_url)
    for song in playlist_tracks['items']:
        if song['track']:
            print(song['track']['artists'][0]['name'])  # [0] is the main artist of the track
            artists[song['track']['artists'][0]['uri']] = song['track']['artists'][0]['name']
    return artists
