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


class MainPage(Screen):
    first = True
    second = True

    def on_enter(self, *args):
        Clock.schedule_once(self.getip, 0.01)

    def getip(self, dt):
        self.box.text = open("ip.txt", "r").read()

    def tick(self, dt):
        self.status.source = "tick.png"

    def cross(self,dt):
        self.status.source = "cross.png"

    def tcp(self, *args):

        y = threading.Thread(target=self.tcpthread, daemon=True)  # Setup thread
        y.start()  # Starts thread

    def tcpthread(self):
        global s
        try:
            host = self.box.text
            port = 10001
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((host, port))
                Clock.schedule_once(self.tick)
                f = open("ip.txt", "w")
                f.write(self.box.text)
                f.close()
                while True:
                    data = s.recv(1024)
                    datastr = data.decode("utf-8")
                    if datastr == '':
                        break
                    time.sleep(0.1)
            Clock.schedule_once(self.cross)
        except:
            print("hülele")

    def test1(self):
        if self.first is True:
            self.led_1 = (.5, 255, .5, 1)
            s.sendall(b'a')
            print('a')
            self.first = False
        elif self.first is False:
            self.led_1 = (255, .5, .5, 1)
            s.sendall(b'b')
            print('b')
            self.first = True

    def test2(self):
        if self.second is True:
            self.led_2 = (.5, 255, .5, 1)
            s.sendall(b'c')
            print('c')
            self.second = False
        elif self.second is False:
            self.led_2 = (255, .5, .5, 1)
            s.sendall(b'd')
            print('d')
            self.second = True


class MyApp(App):
    pass


if __name__ == '__main__':
    MyApp().run()