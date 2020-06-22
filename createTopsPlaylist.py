from authenticate import *
import spotipy
import spotipy.util as util
import requests
import json
import re
from datetime import date
import operator
import pandas as pd


#Gets a token for the user based on the scope
def get_token(scope):
    return util.prompt_for_user_token(username,
                            scope,
                        client_id=client_id,
                        client_secret=client_secret,
                        redirect_uri=redirect_uri)


#Gets all of the user's top songs from the past 4 weeks or so
#(It uses the Spotify API's short_term range condition, and they estimate it to be about 4 weeks of data)
def get_top_monthly_songs(numTopSongs):
    token = get_token('user-top-read')
    query = "https://api.spotify.com/v1/me/top/tracks?time_range=short_term&limit={}".format(numTopSongs)
    response = requests.get(
        query,
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(token)
        }
    )
    response_json = response.json()
    return response_json


#Creates a new playlist titled Top Songs {month} {year}
def create_playlist(numSongs, token):
    today = date.today()
    lastMonth = pd.to_datetime(today) - pd.DateOffset(months=1)
    monthYear = lastMonth.strftime("%B %Y")
    request_body = json.dumps({
        "name": "Top Songs {}".format(monthYear),
        "description": "Top {} songs I listened to last month".format(numSongs)
    })
    query = "https://api.spotify.com/v1/users/{}/playlists".format(spotify_id)

    response = requests.post(
        query,
        data=request_body,
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(token)
        }
    )
    response_json = response.json()
    print("New playlist!")
    return response_json["id"]


#Adds the top songs from the past month to the new playlist
def add_top_monthly_songs(songs, playlist_ID, token):
    topSongs = {}
    for item in songs['items']:
        print(item['name'])
        topSongs[item['uri']] = item['popularity']
    sortedSongs = sorted(topSongs.items(), key=operator.itemgetter(1), reverse=True)
    songURIs = []
    for song in sortedSongs:
        songURIs.append(song[0])
    
    request_body = json.dumps(songURIs)
    query = "https://api.spotify.com/v1/users/{}/playlists/{}/tracks".format(spotify_id, playlist_ID)
    
    response = requests.post(
        query, 
        data = request_body,
        headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(token)
            }
    )
    response_json = response.json()
    return response_json


if __name__=='__main__':
    songs = get_top_monthly_songs(numTopSongs)
    createToken = get_token('playlist-modify-public')
    playlist_ID = create_playlist(numTopSongs, createToken)
    add_top_monthly_songs(songs, playlist_ID, createToken)