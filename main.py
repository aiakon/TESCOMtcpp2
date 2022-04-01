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
from kivy.properties import StringProperty
from datetime import datetime
import socket


class MainPage(Screen):
    first = True
    second = True

    def tcp(self, *args):
        y = threading.Thread(target=self.tcpthread, daemon=True)  # Setup thread
        y.start()  # Starts thread

    def tcpthread(self):
        global s
        host = self.box.text
        port = 10001
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            while True:
                # s.sendall(b'Hello, world')
                data = s.recv(1024)
                datastr = data.decode("utf-8")

    def test1(self):
        if self.first is True:
            s.sendall(b'a')
            print('a')
            self.first = False
        elif self.first is False:
            s.sendall(b'b')
            print('b')
            self.first = True

    def test2(self):
        if self.second is True:
            s.sendall(b'c')
            print('c')
            self.second = False
        elif self.second is False:
            s.sendall(b'd')
            print('d')
            self.second = True


class MyApp(App):
    pass


if __name__ == '__main__':
    MyApp().run()