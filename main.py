import pyttsx3
# import speech_recognition as sr
import re
import datetime
import os
import webbrowser
import wikipedia
from spellchecker import SpellChecker
# import smtplib

url_google = "http://www.google.com"
url_ganna = "https://gaana.com"
url_youtube = "http://www.youtube.com"
url_spotify = "https://www.spotify.com/in"
url_SOF = "https://stackoverflow.com"

"""
    List of neccesary global parameters
    that we need access throughout the code
"""

spell = SpellChecker()
new_wordlist = []
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

"""
    Functions for speech to text and vice versa
"""


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def takeCommand():
    return remove_repeat(input("Type your command: ").lower())
    # r = sr.Recognizer()
    # with sr.Microphone() as source:
    #     print("Listening...")
    #     r.adjust_for_ambient_noise(source)
    #     r.pause_threshold = 1
    #     audio = r.listen(source)
    # try:
    #     print("Recognizing...")
    #     query = r.recognize_google(audio, language='en-in')
    #     print(f"You Said: {query}\n")
    # except Exception as e:
    #     return None
    # return remove_repeat(query).lower()


"""
    autocorrect functions begins from here
"""


def remove_repeat(query):
    return re.sub("(.)\\1{2,}", "\\1", query)


def autocorrect(query):
    global spell
    sent = query.split()
    n = len(sent)
    for i in range(n):
        if spell[sent[i]] == 0:
            sent[i] = spell.correction(sent[i])
    s = ' '
    query = s.join(sent)
    print(query)
    return query


"""
    Loading and adding new keywords in memory
"""


def load_Keywords():
    global spell
    spell.word_frequency.load_text_file('./keywords.txt')


def add_keyword(keyword):
    global spell
    global new_keyword
    if spell[keyword] == 0:
        spell.word_frequency.add(keyword)
        new_wordlist.append(keyword)


def add_wordlist(query):
    speak("Adding keyword")
    for word in query:
        add_keyword(word)


"""
    all the functions that are to be performed begins from here
"""


class FuncClass():

    def __init__(self, inc_query, query):
        self.inc_query = inc_query
        self.query = query

    def execute():
        pass


class wishMe():

    def __init__(self, inc_query, query):
        self.inc_query = inc_query
        self.query = query

    def execute(self):
        hour = int(datetime.datetime.now().hour)
        if hour >= 5 and hour < 12:
            speak("Good Morning!")
        elif(hour >= 12 and hour < 18):
            speak("Good Afternoon!")
        else:
            speak("Good Evening!")


class TimeNow():

    def __init__(self, inc_query, query):
        self.inc_query = inc_query
        self.query = query

    def execute(self):
        if 'exact' in self.query or 'accurate' in self.query:
            timestr = datetime.datetime.now().strftime("%H:%M:%S")
        else:
            timestr = datetime.datetime.now().strftime("%H:%M")
        speak(f"Sir, it is {timestr}")


def hi():
    # speak("Hello. I am Beymax, your personal healthcare companion")
    speak("Hi Sir, I am Jarvis")


class openGoogle():

    def __init__(self, inc_query, query):
        self.inc_query = inc_query
        self.query = query

    def execute(self):
        speak("Opening Google")
        webbrowser.get('windows-default').open(url_google)


class openYtube():

    def __init__(self, inc_query, query):
        self.inc_query = inc_query
        self.query = query

    def execute(self):
        speak("Opening Youtube")
        webbrowser.get('windows-default').open(url_youtube)


class openSOF():

    def __init__(self, inc_query, query):
        self.inc_query = inc_query
        self.query = query

    def execute(self):
        speak("Opening StackOverFlow")
        webbrowser.get('windows-default').open(url_SOF)


class wikisearch():

    def __init__(self, inc_query, query):
        self.inc_query = inc_query
        self.query = query

    def execute(self):
        speak("searching wikipedia")
        query = self.query.replace("wikipedia", "")
        results = wikipedia.summary(query, sentences=2)
        speak("According to wikipedia")
        speak(results)
        speak("would you like to know more?")
        speak("Sorry sir, you have not added code to open wikipedia")


class playMusic():

    def __init__(self, inc_query, query):
        self.inc_query = inc_query
        self.query = query

    def execute(self):
        speak("Sir, where should i play from?...offline music, Ganna, YouTube or\
 Spotify")
        source = takeCommand()
        if "ganna" in source:
            speak("Opening Ganna")
            webbrowser.get('windows-default').open(url_ganna)
        elif "youtube" in source:
            openYtube()
        elif "spotify" in source:
            speak("Opening Spotify")
            webbrowser.get('windows-default').open(url_spotify)
        elif("offline" in source or "ofline" in source or "of line" in source
             or "off line" in source):
            music_dir = "D:/Music"
            songs = os.listdir(music_dir)
            print(songs)


class collect_words_from_book():

    def __init__(self, inc_query, query):
        self.inc_query = inc_query
        self.query = query

    def execute(self):
        speak("Copy paste the path. I can only read from text files for now")
        path = input("Enter the path: ")
        path = path.replace('\\', '/')
        print(path)
        speak("To-do list: you have not added method to capture the words yet")


class Add_wordlist():

    def __init__(self, inc_query, query):
        self.inc_query = inc_query
        self.query = query

    def execute(self):
        global spell
        wordlist = self.inc_query.split()
        correction = self.query.split()
        for i in range(len(wordlist)):
            correct = correction[i]
            if(correct == 'add' or correct == 'keyword'):
                wordlist[i] = correct
        add_wordlist(wordlist)


class Shut_Down():

    def __init__(self, inc_query, query):
        self.inc_query = inc_query
        self.query = query

    def execute(self):
        speak("Saving Changes...")
        self.save_words()
        self.turn_off()

    def save_words(self):
        s = '\n'
        new_words = s.join(new_wordlist)
        with open("./keywords.txt", "a") as f:
            f.write('\n')
            f.write(new_words)
            f.close()

    def turn_off(self):
        speak("Turning off...")
        exit()


"""
    Defining the type of command
"""


class Command():

    def __init__(self, inc_query):
        self.inc_query = inc_query
        self.query = autocorrect(self.inc_query)

    def typeDetect(self):
        if "hello jarvis" in self.query or "hey jarvis" in self.query:
            return wishMe(self.inc_query, self.query)
        elif "wikipedia" in self.query:
            return wikisearch(self.inc_query, self.query)
        elif "the time" in self.query:
            return TimeNow(self.inc_query, self.query)
        elif "open google" in self.query:
            return openGoogle(self.inc_query, self.query)
        elif "play music" in self.query:
            return playMusic(self.inc_query, self.query)
        elif "open youtube" in self.query:
            return openYtube(self.inc_query, self.query)
        elif "open stackoverflow" in self.query:
            return openSOF(self.inc_query, self.query)
        elif "add" in self.query and "keyword" in self.query:
            return Add_wordlist(self.inc_query, self.query)
        elif "read" in self.query and "book" in self.query:
            return collect_words_from_book()
        elif "shut down" in self.query or "shutdown" in self.query:
            return Shut_Down(self.inc_query, self.query)


def main():
    load_Keywords()
    hi()
    while(True):
        query = takeCommand()
        if query is None:
            print("Sorry, I didn't get it!")
        else:
            task = Command(query)
            tasktype = task.typeDetect()
            tasktype.execute()


if __name__ == "__main__":
    main()
