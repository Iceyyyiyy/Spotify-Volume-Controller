from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
import pynput
import pythoncom
from threading import Thread
import tkinter as tk
from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw
from plyer import notification

def vol_down():
    pythoncom.CoInitialize()
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        volume = session._ctl.QueryInterface(ISimpleAudioVolume)
        if session.Process and session.Process.name() == "Spotify.exe":
            print("Current Volume: " + str(volume.GetMasterVolume()))
            vol = volume.GetMasterVolume() - 0.05
            print(f"New Volume: {vol}")
            if not vol <= 0.0:
                volume.SetMasterVolume(vol, None)
            elif vol <= 0.0:
                volume.SetMasterVolume(0.0, None)
            else:
                print("Volume out of bounds")

def vol_up():
    pythoncom.CoInitialize()
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        volume = session._ctl.QueryInterface(ISimpleAudioVolume)
        if session.Process and session.Process.name() == "Spotify.exe":
            print("Current Volume: " + str(volume.GetMasterVolume()))
            vol = volume.GetMasterVolume() + 0.05
            print(f"New Volume: {vol}")
            if not vol >= 1.0:
                volume.SetMasterVolume(vol, None)
            elif vol >= 1.0:
                volume.SetMasterVolume(1.0, None)
            else:
                print("Volume out of bounds")

def on_release(key):
    key_str = str(key)
    if '<141>' in key_str:
        thread = Thread(target=vol_down)
        thread.start()
    if '<140>' in key_str:
        thread = Thread(target=vol_up)
        thread.start()

def create_image():
    width = 64
    height = 64
    image = Image.new('RGB', (width, height), color=(0, 0, 0))
    draw = ImageDraw.Draw(image)
    speaker_coords = [
        (10, 20), 
        (25, 20),  
        (35, 10),  
        (35, 54),  
        (25, 44),  
        (10, 44)   
    ]
    draw.polygon(speaker_coords, fill=(255, 255, 255))

    draw.arc([36, 16, 60, 48], start=310, end=50, fill=(255, 255, 255), width=2)
    draw.arc([40, 12, 64, 52], start=310, end=50, fill=(255, 255, 255), width=2)

    return image

def quit_app(icon, item):
    icon.stop()

listener = pynput.keyboard.Listener(on_release=on_release)
listener.start()

menu = Menu(
    MenuItem('Quit', quit_app)
)

icon = Icon("Spotify Volume Controller", create_image(), "Spotify Volume Controller", menu)
icon.run()

listener.stop()



