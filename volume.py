from main import speak
from pynput.keyboard import Key, Controller
import sys
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
mnVol, mxVol, stepVol = volume.GetVolumeRange()

keyboard = Controller()


def convert(x):
    return(x)


def set_volume(n):
    if type(n) == int:
        volume.SetMasterVolumeLevel(n, None)
        speak(f"Volume is set to {n}")
    else:
        speak("Set volume attribute should be a number")


def get_volume():
    print(volume.GetMasterVolumeLevel())
    volLevel = convert(volume.GetMasterVolumeLevel())
    speak(f"Volume level is {volLevel} percent")


def sys_mute():
    print("System is on mute sir")
    keyboard.press(Key.media_volume_mute)
    keyboard.release(Key.media_volume_mute)


def sys_unmute():
    keyboard.press(Key.media_volume_mute)
    keyboard.release(Key.media_volume_mute)
    speak("System is unmuted")


def inc_vol():
    speak("I can't increase volume yet, maybe you can teach me")


def dec_vol():
    speak("I  can't decrease volume yet, maybe you can teach me")


def inc_vol_to(n):
    speak("I can't increase volume yet, maybe you can teach me")


def dec_vol_to(n):
    speak("I  can't decrease volume yet, maybe you can teach me")


if len(sys.argv) == 2:
    if sys.argv[1] == 'm':
        sys_mute()
    elif sys.argv[1] == 'u':
        sys_unmute()
    elif sys.argv[1] == 'g':
        get_volume()
    elif sys.argv[1] == 'i':
        inc_vol()
    elif sys.argv[1] == 'd':
        dec_vol()
elif len(sys.argv) >= 3:
    if sys.argv[1] == 's':
        set_volume(sys.argv[2])
    elif sys.argv[1] == 'in':
        inc_vol_to(sys.argv[2])
    elif sys.argv[1] == 'de':
        dec_vol_to(sys.argv[2])
