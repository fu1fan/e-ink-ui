import threading as _threading
import time

from .drivers import epd2in9_V2, icnt86
from .touchscreen import Clicked as _Clicked, \
    SlideX as _SlideX, \
    SlideY as _SlideY, \
    TouchRecoder as _TouchRecoder

import os as _os


class Env:
    def __init__(self):
        # screen
        self.Screen = epd2in9_V2.Screen()

        # touchscreen
        self.Touch = icnt86.TouchDriver()
        self.Touch.icnt_init()

    @staticmethod
    def poweroff():
        _os.system("sudo poweroff")

    @staticmethod
    def reboot():
        _os.system("sudo reboot")
