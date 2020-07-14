import webbrowser
import requests
import sys
from main import speak
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import os

urls = [{'name': 'Google', 'url': 'http://www.google.com'},
        {'name': 'Youtube', 'url': 'http://www.youtube.com'},
        {'name': 'Spotify', 'url': 'https://www.spotify.com/in'},
        {'name': 'Gaana', 'url': 'https://gaana.com'},
        {'name': 'Stackoverflow', 'url': 'https://stackoverflow.com'},
        {'name': 'Google Maps', 'url': 'https://www.google.com/maps'},
        {'name': 'WhatsApp', 'url': 'https://web.whatsapp.com/'}]


def open_item(query):
    query1 = (''.join(query)).lower()
    for user in os.listdir("C:/Users"):
        if user not in ['All Users', 'Default', 'Default User', 'desktop.ini']:
            for file in os.listdir(f"C:/Users/{user}/Desktop"):
                if file.endswith(".lnk"):
                    name = file.replace(".lnk", "")
                    key = name.replace(" ", "").lower()
                    if query1 in key:
                        open_app(name, f"C:/Users/{user}/Desktop/{file}")
                        return
    for site in urls:
        if query1 in site['name'].replace(" ", "").lower():
            open_web(site['name'], site['url'])
            return
    open_additional(query, query1)


def open_app(name, Dir):
    speak(f"Opening {name}")
    os.startfile(Dir)


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
    speak("Opening related search results in new tab")
    webbrowser.get('windows-default').open(URL)


open_item(sys.argv[1:])
