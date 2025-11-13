
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
import threading
import socket
import sounddevice as sd
import numpy as np

UDP_PORT = 5005
clients = []
running = False

# إنشاء socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

CHUNK = 1024
RATE = 44100

def send_audio():
    global running
    def callback(indata, frames, time, status):
        if running:
            for addr in clients:
                sock.sendto(indata.tobytes(), addr)
    with sd.InputStream(channels=1, samplerate=RATE, blocksize=CHUNK, callback=callback):
        while running:
            sd.sleep(100)

def receive_audio():
    global running
    sock.bind(("", UDP_PORT))
    while running:
        try:
            data, addr = sock.recvfrom(CHUNK*2)
            if addr not in clients:
                clients.append(addr)
            audio_data = np.frombuffer(data, dtype=np.int16)
            sd.play(audio_data, RATE, blocking=False)
        except:
            pass

class VoiceChatApp(App):
    def build(self):
        self.root_layout = BoxLayout(orientation='vertical', padding=10, spac_
