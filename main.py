import pyttsx3
# import speech_recognition as sr
import re
import datetime
import os
import webbrowser
import wikipedia
from spellchecker import SpellChecker
# import smtplib

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
    # return autocorrect(query).lower()


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


def add_wordlist():
    speak("Enter the keyword")
    query = input("Enter the keyword: ").lower()
    query = query.split()
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


def openGoogle():
    speak("Opening Google")
    webbrowser.get('windows-default').open("http://www.google.com")


def openYtube():
    speak("Opening Youtube")
    webbrowser.get('windows-default').open("http://www.youtube.com")


def openSOF():
    speak("Opening StackOverFlow")
    webbrowser.get('windows-default').open("https://stackoverflow.com")


def wikisearch(query):
    speak("searching wikipedia")
    query = query.replace("wikipedia", "")
    results = wikipedia.summary(query, sentences=2)
    speak("According to wikipedia")
    speak(results)
    speak("would you like to know more?")


def playMusic(query):
    speak("Sir, where should i play from?...offline music, Ganna, YouTube or\
 Spotify")
    source = takeCommand()
    if "ganna" in source:
        speak("Opening Ganna")
        webbrowser.get('windows-default').open("https://gaana.com")
    elif "youtube" in source:
        openYtube()
    elif "spotify" in source:
        speak("Opening Spotify")
        webbrowser.get('windows-default').open("https://www.spotify.com/in")
    elif("offline" in source or "ofline" in source or "of line" in source or
         "off line" in source):
        music_dir = "D:/Music"
        songs = os.listdir(music_dir)
        print(songs)


def collect_words_from_book():
    speak("Copy paste the path. I can only read from text files for now")
    path = input("Enter the path: ")
    path = path.replace('\\', '/')
    print(path)
    speak("To-do list: you have not added a method to capture the words yet")


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
        # elif "wikipedia" in query:
        #     return wikisearch(inc_query, query)
        elif "the time" in self.query:
            return TimeNow(self.inc_query, self.query)
        # elif "open google" in query:
        #     return openGoogle(inc_query, query)
        # elif "play music" in query:
        #     return playMusic(inc_query, query)
        # elif "open youtube" in query:
        #     return openYtube(inc_query, query)
        # elif "open stackoverflow" in query:
        #     return openSOF(inc_query, query)
        # elif "add keyword" in query:
        #     return add_wordlist(inc_query, query)
        # elif "read" in query and "book" in query:
        #     return collect_words_from_book(inc_query, query)
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
