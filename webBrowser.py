import webbrowser
import requests
import sys
from main import speak
from bs4 import BeautifulSoup
from urllib.parse import urlparse

urls = [{'name': 'google', 'url': 'http://www.google.com'},
        {'name': 'youtube', 'url': 'http://www.youtube.com'},
        {'name': 'spotify', 'url': 'https://www.spotify.com/in'},
        {'name': 'gaana', 'url': 'https://gaana.com'},
        {'name': 'stackoverflow', 'url': 'https://stackoverflow.com'},
        {'name': 'googlemaps', 'url': 'https://www.google.com/maps'}]


def open_item(query):
    query1 = (''.join(query)).lower()
    for site in urls:
        if query1 in site['name']:
            open_web(site['name'], site['url'])
            return
    open_additional(query, query1)


def open_web(name, url):
    speak(f"Opening {name}")
    webbrowser.get('windows-default').open(url)


def open_additional(query, query1):
    base_URL = "https://www.google.com/search?q="
    query2 = ('+'.join(query)).lower()
    speak("Searching for webpage")
    headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/\
537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}
    URL = base_URL + query2
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find_all("div", class_="g")
    for i in results:
        try:
            j = i.find("div", class_='r')
            site = j.find("a")['href']
            domain = urlparse(site).netloc
            if query1 in domain.lower():
                speak("Opening webpage")
                webbrowser.get('windows-default').open(site)
                exit()
        except AttributeError:
            pass
    speak("No results found sir")


open_item(sys.argv[1:])
