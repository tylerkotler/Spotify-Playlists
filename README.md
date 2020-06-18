# Spotify-Playlists
Welcome! This repo allows you to do 2 things:
1. Automatically generate a new Spotify playlist of Billboard's top 50 EDM songs
2. Automatically generate a new Spotify playlist of your top songs from the past 4 weeks/month

# Steps to get started

1. Download Python if you don't already have it. Go to https://www.python.org/downloads/

2. Clone this repository - open Terminal and copy and paste this in: 
    git clone --bare https://github.com/tylerkotler/Spotify-Playlists.git    
    
3. Install requirements - in Terminal, copy and past this in: pip3 install -r requirements.txt

4. Get all Spotify information and edit the authenticate.py file to fill in all your information - follow steps below:

# Getting Spotify information

1. Get your username that you used for your Spotify account and add it to the authenticate.py file

2. Get your client ID, client secret, and redirect URI
a) Go to developer.spotify.com and login to your dashboard using your Spotify account
b) Click "Create an App", give it a name and a description, and agree to the terms
c) Once you've created the app, it should show you client ID and you can click "Show Client Secret" to get the secret. Copy and paste both of those into their spots in the authenticate.py file
d) Click "Edit Settings" for your app and add a redirect uri. It can be any website, but I recommend just using: http://localhost:8080 - then add this redirect uri to the authenticate.py file (it's preset to http://localhost:8080, so change it if you are using something else)

3. Get your Spotify ID
a) Open the spotify app on your computer and click your name in the top right
b) Click on the 3 dots below your profile photo -> share -> copy spotify uri
c) Paste the spotify uri in for spotify_id in authenticate.py. Then, from the uri you pasted in, delete: spotify:user: (leaving only the number)

4. If you want to create the playlist with your top songs from the previous month, the numTopSongs variable is preset to 20. Change that number if you want to generate a playlist with a different number of your top songs.

# Running the scripts

To get the top 50 EDM songs:
1. Open Terminal, enter: cd Spotify-Playlists
2. In Terminal, enter: python createEDMPlaylist.py

To get your top songs from the previous month:
1. Open Terminal, enter cd Spotify-Playlists
2. In Terminal, enter: python createTopsPlaylist.py
