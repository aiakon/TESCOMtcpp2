# python main.py -m screen:ipad
# Yapılacaklar: global stopflag'i self.variable yap.

from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from kivy.clock import Clock
import requests
import time
import threading
from kivy.properties import StringProperty, ObjectProperty
from datetime import datetime
import socket


green = (.5, 255, .5, 1)
red = (255, .5, .5, 1)


class MainPage(Screen):
    first = True
    second = True

    def on_enter(self, *args):
        Clock.schedule_once(self.getip, 0.01)

    def getip(self, dt):
        self.box.text = open("ip.txt", "r").read()

    def tick(self, dt):
        self.status.source = "tick.png"
        self.status2.source = "tick.png"

    def cross(self,dt):
        self.status.source = "cross.png"
        self.status2.source = "cross.png"

    def tcp(self, *args):
        y = threading.Thread(target=self.tcpthread, daemon=True)  # Setup thread
        y.start()  # Starts thread

    def tcpthread(self):
        global s
        try:
            host = self.box.text
            port = int(self.portt.text)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((host, port))
                # Eğer sorunsuz bağlandıysa
                Clock.schedule_once(self.tick)  # tik işareti koy.
                f = open("ip.txt", "w")     # ip adresini kaydet.
                f.write(self.box.text)
                f.close()
                while True:
                    data = s.recv(1024)
                    print(data)
                    datastr = data.decode("utf-8")

                    if 'a' in datastr:
                        self.onf.background_color = green
                    elif 'A' in datastr:
                        self.onf.background_color = red

                    if 'b' in datastr:
                        self.bir.background_color = green
                    elif 'B' in datastr:
                        self.bir.background_color = red

                    if 'c' in datastr:
                        self.iki.background_color = green
                    elif 'C' in datastr:
                        self.iki.background_color = red

                    if datastr == '':
                        break
                    time.sleep(0.1)
            Clock.schedule_once(self.cross)
        except Exception as e:
            print("crash", e)


class ControlPage(Screen):

    def send(self, x):
        try:
            s.sendall(bytes(x, 'utf-8'))

        except Exception as e:
            self.status2.source = "cross.png"
            print("fail,", e)

class MyApp(App):
    pass


if __name__ == '__main__':
    MyApp().run()