from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
import pynput
import pythoncom
from threading import Thread
from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw

mute = True
oldVol = 0
active = True

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

def vol_mute():
    pythoncom.CoInitialize()
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        volume = session._ctl.QueryInterface(ISimpleAudioVolume)
        if session.Process and session.Process.name() == "Spotify.exe":
            global mute
            if mute:
                global oldVol
                oldVol = volume.GetMasterVolume()
                print(oldVol)
                volume.SetMasterVolume(0.0, None)
                mute = False
            else:
                volume.SetMasterVolume(oldVol, None)
                mute = True

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

def active_app(item):
    global active
    active = not active
    icon.update_menu()
    print(active)

def win32_event_filter(msg, data):
    if msg == 0x0100 and active:
        if data.vkCode == 0xAF:
            thread = Thread(target=vol_up)
            thread.start()
            listener.suppress_event()
        elif data.vkCode == 0xAE:
            thread = Thread(target=vol_down)
            thread.start()
            listener.suppress_event()
        elif data.vkCode == 0xAD:
            thread = Thread(target=vol_mute)
            thread.start()
            listener.suppress_event()

listener = pynput.keyboard.Listener(win32_event_filter=win32_event_filter)
listener.start()

menu = Menu(
    MenuItem('Active', active_app, checked=lambda item: active),
    MenuItem('Quit', quit_app)
)

icon = Icon("Spotify Volume Controller", create_image(), "Spotify Volume Controller", menu)
icon.run()

listener.stop()

