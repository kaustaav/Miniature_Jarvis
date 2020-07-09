import pyttsx3
import re
import os
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
spell = SpellChecker(case_sensitive=True)
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
    return response


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
    global new_wordlist
    global spell
    if spell[keyword] == 0:
        spell.word_frequency.add(keyword)
        new_wordlist.append(keyword)


def add_wordlist(query):
    speak("Adding keyword")
    for word in query:
        add_keyword(word)


def initiate():
    load_Keywords()
    speak("Hello Sir, I am Jarvis.")


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


def response_execute(response):
    if response == "system shut down":
        Shut_Down()
    elif 'adding keyword ' in response:
        response = response.replace('adding keyword ', '')
        add_wordlist(response.split())
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
    initiate()
    while True:
        query = takeCommand(mode)
        response = kernel.respond(query)
        response_execute(response)


if __name__ == "__main__":
    main()
