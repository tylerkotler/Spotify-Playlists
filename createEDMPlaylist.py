import spotipy
import spotipy.util as util
from authenticate import *
from bs4 import BeautifulSoup
import requests
import json
import re
from datetime import date
import pandas as pd


song_IDs = []

token = get_token('playlist-modify-public')
#Gets a token for user for all playlist modifying abilities
def get_token(scope):
    return util.prompt_for_user_token(username,
                            scope,
                        client_id=client_id,
                        client_secret=client_secret,
                        redirect_uri=redirect_uri)


#Scrapes the top 50 songs off Billboard's Hot Electic/Dance Songs page using Beautiful Soup
def scrapeSongs():
    try:
        source = requests.get('https://www.billboard.com/charts/dance-electronic-songs')
        topSongsHtml = source.text
    except:
        print('Error getting top EDM list html')

    soup = BeautifulSoup(topSongsHtml, 'html.parser')
    count = 1
    for songHtml in soup.find_all('div', class_='chart-list-item'):
        name = songHtml['data-title']
        artists = songHtml['data-artist']
        parsedArtists = re.split(' Featuring | & | With | X | x |, ', artists)
        print("{}. {} by {}".format(count, name, parsedArtists))
        count = count+1
        artistList = re.split(" Featuring | & | With | X | x |, ", artists)
        artistList = [artist.lower() for artist in artistList]
        song_ID = find_song(name, artistList)
        if(song_ID!=None):
            song_IDs.append(song_ID)

    create_playlist()


#Finds each song on spotify given the name and list of artists
#Looks for exact matches first - name is exact and all artists are the same
#If that doesn't give a result, looks for exact name and at least one of the same artist for the songs
def find_song(name, artistList):
    query = 'https://api.spotify.com/v1/search?q={}&type=track&market=US&limit=5'.format(name)
    response = requests.get(
        query,
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(token)
        }
    )
    response_json = response.json()

    trackAndArtists = {}
    for result in response_json['tracks']['items']:
        trackArtists = result['artists']
        nameList = []
        for item in trackArtists:
            nameList.append(item['name'].lower())
        trackAndArtists[result['id']] = nameList
    
    for key, value in trackAndArtists.items():
        if set(value) == set(artistList):
            return key
    for key, value in trackAndArtists.items():
        for artist in artistList:
            if artist in value:
                return key
    return None


#Creates a new playlist titled EDM {month} {year}
def create_playlist():
    today = date.today()
    lastMonth = pd.to_datetime(today) - pd.DateOffset(months=1)
    monthYear = lastMonth.strftime("%B %Y")
    request_body = json.dumps({
        "name": "EDM {}".format(monthYear),
        "description": "Top 50 EDM Songs - scraped from Billboard's website"
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
    print()
    print("New playlist!")
    print(response_json["id"])
    addSongs(response_json["id"])


#Adds all songs to the new playlist
def addSongs(playlist_ID):
    uris = []
    for song_ID in song_IDs:
        uri = "spotify:track:{}".format(song_ID)
        uris.append(uri)
    request_body = json.dumps(uris)
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


if __name__ == '__main__':
   scrapeSongs()