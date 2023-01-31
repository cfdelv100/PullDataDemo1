# Pull Demo Project
# Carlos Del Valle
# Purpose: As we want to pull data from an API we have access to, we want to assess the quality of the data,
# therefore, we must pull data and make it accessible via an AWS storage cloud for other systems to obtain acccess to.

import spotipy
import csv
import boto3
from datetime import datetime


from config.playlists import spotify_playlists
from tools.playlists import get_artists_from_playlists

spotipy_object = spotipy.Spotify(client_credentials_manager=spotipy.oauth2.SpotifyClientCredentials())

final_data_directory = {
    'Year Released': [],
    'Album Length': [],
    'Album Name': [],
    'Artist': []
}

PLAYLIST  = 'rap_caviar'


# For every artist we search for
def gather_data_local():
    with open("rapcaviar_albums.csv", 'w') as file:
        header = list(final_data_directory.keys())
        writer = csv.DictWriter(file, fieldnames=header) # binary to csv
        writer.writeheader()
        albums_obtained = []

        artists = get_artists_from_playlists(spotify_playlists()[PLAYLIST])

        # for each arist in artists.keys()
        for artist in list(artists.keys()):
            print(artist)
            artist_albums = spotipy_object.artist_albums(artist, album_type='album', limit=50)
            # for all the albums
            for album in artist_albums['items']:
                if 'GB' and 'US' in album['available_markets']:
                    key = album['name'] + album['artists'][0]['name'] + album['release_date'][:4]
                    if key not in albums_obtained:
                        albums_obtained.append(key)
                        album_data = spotipy_object.album(album['uri'])
                        # for every song on the album
                        for song in album_data['tracks']['items']:
                            album_length_ms = song['duration_ms'] + album_length_ms
                        writer.writerow({'Year Released': album_data['release date'][:4],
                                         'Album Length': album_length_ms,
                                         'Album Name': album_data['name'],
                                         'Artist': album_data['artists'][0]['name']})
                        final_data_directory['Year Released'].append(album_data['release date'][:4])
                        final_data_directory['Album Length'].append(album_length_ms)
                        final_data_directory['Album Name'].append(album_data['name'])
                        final_data_directory['Artist'].append(album_data['artists'][0]['name'])

        return final_data_directory



def gather_data():
    # For every arist we are looking for
    with open("/tmp/rapcaviar_albums.csv", 'w') as file:
        header = ['Year Released', 'Album Length', 'Album Name', 'Artist']
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()
        artists = get_artists_from_playlists(spotify_playlists()[PLAYLIST])
        for artist in artists.keys():
            artist_albums = spotipy_object.artist_albums(artist, album_type='album', limit=50)
            # for all the artist albums
            for album in artist_albums['items']:
                if 'GB' in artist_albums['items'][0]['available_markets']:
                    album_data = spotipy_object.album(album['uri'])
                    # for every song on the album
                    album_length_ms = 0
                    for song in album_data['tracks']['items']:
                        album_length_ms = song['duration_ms'] + album_length_ms
                    writer.writerow({'Year Released' : album_data['release date'][:4],
                                     'Album Length' : album_length_ms,
                                     'Album Name': album_data['name'],
                                     'Artist': album_data['artists'][0]['name']})

    # create a s3 resource
    s3_resource = boto3.resource('s3')
    date = datetime.now()
    filename = f'{date.year}/{date.month}/{date.day}/rapcaviar_albums.csv'
    response = s3_resource.Object('spotify-analysis-data',filename).upload_file("/tmp/rapcaviar_albums.csv")

    return response


# takes in two arguments to run data
def lambda_handler(event, context):
    gather_data()


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
   data = gather_data_local()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
