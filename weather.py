import sys
from bs4 import BeautifulSoup
import webbrowser
import requests
from main import speak


def weather_report(query):
    query = '+'.join(query).lower()
    if 'hey' in query:
        query = query.replace('hey', "")
    if 'jarvis' in query:
        query = query.replace('jarvis', "")
    base_url = "https://www.google.com/search?q="
    headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/\
537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}
    URL = base_url + query
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    try:
        result = {}
        result['region'] = soup.find("div", attrs={"id": "wob_loc"}).text
        result['weather_now'] = soup.find("span", attrs={"id": "wob_dc"}).text
        result['temp_now'] = soup.find("span", attrs={"id": "wob_tm"}).text
        result['precipitation'] = soup.find("span", attrs={"id": "wob_p\
p"}).text
        result['humidity'] = soup.find("span", attrs={"id": "wob_hm"}).text
        result['wind'] = soup.find("span", attrs={"id": "wob_ws"}).text
        speak(f"Currently in {result['region']} its {result['temp_now']} d\
egrees with {result['weather_now']}, precipitation is\
 {result['precipitation']}, humidity is {result['humidity']} and windspeed is\
 {result['wind']}")
    except AttributeError:
        webbrowser.get('windows-default').open(URL)


weather_report(sys.argv[1:])
