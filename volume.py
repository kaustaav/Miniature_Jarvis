from main import speak
from pynput.keyboard import Key, Controller
import sys

keyboard = Controller()


def sys_mute():
    print("System is on mute sir")
    keyboard.press(Key.media_volume_mute)
    keyboard.release(Key.media_volume_mute)


def sys_unmute():
    speak("System is unmuted")
    keyboard.press(Key.media_volume_mute)
    keyboard.release(Key.media_volume_mute)


if len(sys.argv) == 2:
    if sys.argv[1] == 'm':
        sys_mute()
    elif sys.argv[1] == 'u':
        sys_unmute()
