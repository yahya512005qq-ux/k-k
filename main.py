# android_voice_chat_gui.py
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
import threading
import socket
import pyaudio

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
UDP_PORT = 5005
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clients = []

p = pyaudio.PyAudio()
stream_out = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)
stream_in = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
running = False

def send_audio():
    global running
    while running:
        try:
            data = stream_in.read(CHUNK)
            for addr in clients:
                sock.sendto(data, addr)
        except:
            pass

def receive_audio():
    global running
    sock.bind(("", UDP_PORT))
    while running:
        try:
            data, addr = sock.recvfrom(CHUNK*2)
            if addr not in clients:
                clients.append(addr)
            stream_out.write(data)
        except:
            pass

class VoiceChatApp(App):
    def build(self):
        self.root_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.ip_input = TextInput(hint_text="أدخل IP الجهاز الآخر", size_hint=(1,0.2))
        self.root_layout.add_widget(self.ip_input)
        add_button = Button(text="إضافة عميل", size_hint=(1,0.2))
        add_button.bind(on_press=self.add_client)
        self.root_layout.add_widget(add_button)
        start_button = Button(text="ابدأ المكالمة", size_hint=(1,0.3), background_color=(0,1,0,1))
        start_button.bind(on_press=self.start_call)
        self.root_layout.add_widget(start_button)
        stop_button = Button(text="إيقاف المكالمة", size_hint=(1,0.3), background_color=(1,0,0,1))
        stop_button.bind(on_press=self.stop_call)
        self.root_layout.add_widget(stop_button)
        return self.root_layout

    def add_client(self, instance):
        ip = self.ip_input.text
        if ip:
            clients.append((ip, UDP_PORT))
            self.ip_input.text = ""

    def start_call(self, instance):
        global running
        running = True
        threading.Thread(target=send_audio, daemon=True).start()
        threading.Thread(target=receive_audio, daemon=True).start()

    def stop_call(self, instance):
        global running
        running = False

if __name__ == "__main__":
    VoiceChatApp().run()
