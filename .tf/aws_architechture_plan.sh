#!/usr/bin/env bash


terraform init

cp -r /Users/cdelv/AppData/Local/Programs/Python/Python3.8/lib/site-packages/requests ../lambda_payloads/avg_album_length_playlist_payload/
cp -r /Users/cdelv/AppData\Local/Programs/Python/Python3.8/lib/site-packages/spotipy ../lambda_payloads/avg_album_length_playlist_payload/


cp /PythonProjects/SpotifyDataDemo/avg_album_length_playlist.py ../lambda_payloads/avg_album_length_playlist_payload/
cp /PythonProjects/SpotifyDataDemo/config/playlists.py ../lambda_payloads/avg_album_length_playlist_payload/config/
cp /PythonProjects/SpotifyDataDemo/tools/playlists.py ../lambda_payloads/avg_album_length_playlist_payload/tools/

cd ../lambda_payloads/avg_album_length_playlist_payload/

zip -r ../../payload.zip *

cd ../../.tf/

terraform plan