import requests
from bs4 import BeautifulSoup
import os
import re

GENIUS_API_TOKEN="bs829ZO1VbzFfnS3ekjUmsIO6ZreP7hoIfO4cd3g00Nl_3-npF1Z-UXgV2jQ6uuL"

# Get artist object from Genius API
def request_artist_info(artist_name, page):
    base_url = 'https://api.genius.com'
    headers = {'Authorization': 'Bearer ' + GENIUS_API_TOKEN}
    search_url = base_url + '/search?per_page=10&page=' + str(page)
    data = {'q': artist_name}
    response = requests.get(search_url, data=data, headers=headers)
    return response


# Get Genius.com song url's from artist object
def request_song_url_from_artist(artist_name, song_cap=5):
    """This function get the url fo get lyrics given an artist name, the number of url you get is set to 20"""
    page = 1
    song_urls = []
    
    while True:
        response = request_artist_info(artist_name, page)
        json = response.json()
        # Collect up to song_cap song objects from artist
        song_info = []
        for hit in json['response']['hits']:
            if artist_name.lower() in hit['result']['primary_artist']['name'].lower():
                song_info.append(hit)
    
        # Collect song URL's from song objects
        for song in song_info:
            if (len(song_urls) < song_cap):
                url = song['result']['url']
                song_urls.append(url)
                #title=song['result']['title']
            
        if (len(song_urls) == song_cap):
            break
        else:
            page += 1

    return song_urls


def scrape_song_lyrics(url):

    """This function get the songs lyrics given the url that you can get with the function 'request_song_url_from_artist' """

    page = requests.get(url)
    html = BeautifulSoup(page.text, 'html.parser')
    lyrics = html.find('div', {'data-lyrics-container': 'true'}).get_text()
    # Use regex to insert a space before each capital letter
    lyrics=re.sub(r'(?<!\s)([A-Z])', r' \1', lyrics)
    #remove identifiers like chorus, verse, etc
    lyrics = re.sub(r'[\(\[].*?[\)\]]', '', lyrics)
    #remove empty lines
    lyrics = os.linesep.join([s for s in lyrics.splitlines() if s])     
    #get song title
    title=html.find("span", class_='SongHeaderdesktop__HiddenMask-sc-1effuo1-11 iMpFIj').text   
    return lyrics, title