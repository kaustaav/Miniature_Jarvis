import pyttsx3
import re
import datetime
import os
import webbrowser
import wikipedia
from spellchecker import SpellChecker
import argparse
import aiml
# import sys
# import smtplib

"""
    List of URL's
"""

url_google = "http://www.google.com"
url_ganna = "https://gaana.com"
url_youtube = "http://www.youtube.com"
url_spotify = "https://www.spotify.com/in"
url_SOF = "https://stackoverflow.com"

"""
    List of neccesary global parameters
    that we need access throughout the code
"""

mode = "text"
spell = SpellChecker()
new_wordlist = []
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

"""
    Set input mode (text/voice) for jarvis
    to activate voice mode type '--voice' in command line
    text mode is set as default
"""


def get_args():
    parser = argparse.ArgumentParser()
    optional = parser.add_argument_group('params')
    optional.add_argument('-v', '--voice', action='store_true', required=False,
                          help="Enable voice mode")
    arguments = parser.parse_args()
    return arguments


"""
    Functions for speech to text and vice versa
"""


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = r.listen(source)
    try:
        query = r.recognize_google(audio)
        print(query)
        return query
    except sr.UnknownValueError:
        return listen()
    except sr.RequestError as e:
        print("Could not request results from " +
              "Google Speech Recognition service; {0}".format(e))


def text_input():
    query = input("Type your command: ")
    return autocorrect(re.sub("(.)\\1{2,}", "\\1", query))


def takeCommand(mode):
    if mode == "voice":
        response = listen()
    else:
        response = text_input()
    return response.lower()


"""
    autocorrect functions begins from here
"""


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

    def __init__(self, query):
        self.query = query

    def execute():
        pass


class wishMe():

    def __init__(self, query):
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

    def __init__(self, query):
        self.query = query

    def execute(self):
        if 'exact' in self.query or 'accurate' in self.query:
            timestr = datetime.datetime.now().strftime("%H:%M:%S")
        else:
            timestr = datetime.datetime.now().strftime("%H:%M")
        speak(f"Sir, it is {timestr}")


def hi():
    # speak("Hello. I am Beymax, your personal healthcare companion")
    speak("Hello Sir, I am Jarvis.")


class openGoogle():

    def __init__(self, query):
        self.query = query

    def execute(self):
        speak("Opening Google")
        webbrowser.get('windows-default').open(url_google)


class openYtube():

    def __init__(self, query):
        self.query = query

    def execute(self):
        speak("Opening Youtube")
        webbrowser.get('windows-default').open(url_youtube)


class openSOF():

    def __init__(self, query):
        self.query = query

    def execute(self):
        speak("Opening StackOverFlow")
        webbrowser.get('windows-default').open(url_SOF)


class wikisearch():

    def __init__(self, query):
        self.query = query

    def execute(self):
        speak("searching wikipedia")
        query = self.query.replace("wikipedia", "")
        query = self.query.replace("search", "")
        results = wikipedia.summary(query, sentences=2)
        speak("According to wikipedia")
        speak(results)
        # speak("would you like to know more?")
        speak("Sorry sir, you have not added further code to open wikipedia")


class playMusic():

    def __init__(self, query):
        self.query = query

    def execute(self):
        speak("Sir, where should i play from?...offline music, Ganna, YouTube or\
 Spotify")
        source = takeCommand(mode)
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

    def __init__(self, query):
        self.query = query

    def execute(self):
        speak("Copy paste the path. I can only read from text files for now")
        path = input("Enter the path: ")
        path = path.replace('\\', '/')
        print(path)
        speak("To-do list: you have not added method to capture the words yet")


class Add_wordlist():

    def __init__(self, query):
        self.query = query

    def execute(self):
        # wordlist = self.inc_query.split()
        # correction = self.query.split()
        # for i in range(len(wordlist)):
        #     correct = correction[i]
        #     if(correct == 'add' or correct == 'keyword'):
        #         wordlist[i] = correct
        # add_wordlist(wordlist)
        add_wordlist(self.query)


def Shut_Down():

    speak("Saving Changes...")

    def save_words():
        if len(new_wordlist) > 0:
            s = '\n'
            new_words = s.join(new_wordlist)
            with open("./keywords.txt", "a") as f:
                f.write('\n')
                f.write(new_words)
                f.close()

    def turn_off():
        speak("Turning off...")
        exit()
    save_words()
    turn_off()


"""
    Defining the type of command
"""


class Command():

    def __init__(self, query):
        self.query = query

    def typeDetect(self):
        if "hello jarvis" in self.query or "hey jarvis" in self.query:
            return wishMe(self.query)
        elif "wikipedia" in self.query:
            return wikisearch(self.query)
        elif "the time" in self.query:
            return TimeNow(self.query)
        elif "open google" in self.query:
            return openGoogle(self.query)
        elif "play music" in self.query:
            return playMusic(self.query)
        elif "open youtube" in self.query:
            return openYtube(self.query)
        elif "open stackoverflow" in self.query:
            return openSOF(self.query)
        elif "add" in self.query and "keyword" in self.query:
            return Add_wordlist(self.query)
        elif "read" in self.query and "book" in self.query:
            return collect_words_from_book(self.query)
        elif "shut down" in self.query or "shutdown" in self.query:
            return Shut_Down(self.query)


def response_execute(response):
    if response == "system shut down":
        Shut_Down()
    else:
        speak(response)


def main():
    global mode
    args = get_args()
    if args.voice:
        try:
            import speech_recognition as sr
            global sr
            mode = "voice"
        except ImportError:
            print("\nInstall SpeechRecognition to use this feature." +
                  "\nInitiating text mode\n")
    kernel = aiml.Kernel()

    if os.path.isfile("jarvis_brain.brn"):
        kernel.bootstrap(brainFile="jarvis_brain.brn")
    else:
        kernel.bootstrap(learnFiles="std-startup.xml", commands="load aiml b")
        kernel.saveBrain("jarvis_brain.brn")
    hi()
    load_Keywords()
    while True:
        query = takeCommand(mode)
        response = kernel.respond(query)
        response_execute(response)


if __name__ == "__main__":
    main()
