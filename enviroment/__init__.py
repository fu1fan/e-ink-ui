import threading as _threading
import time as _time
from queue import LifoQueue as _LifoQueue


from PIL import Image as _Image, \
    ImageFont as _ImageFont

from system import threadpool as _threadpool
from system import logger as _logger
from .touchscreen import Clicked as _Clicked, \
    SlideY as _SlideY, \
    TouchHandler as _TouchHandler, \
    TouchRecoder as _TouchRecoder
from .touchscreen.events import SlideX as _SlideX
import os as _os
from framework.struct import Base as _Base
from system import configurator


example_config = {
    "theme": "默认（黑）",
    "docker": ["天气"]
}

from enviroment.drivers import epd2in9_V2 as _epd2in9_V2, icnt86


class Env:
    def __init__(self):
        self.config = configurator.Configurator()
        self.config.check(example_config, True)

        # locks
        self.display_lock = _threading.Lock()

        # fonts
        self.fonts = {}

        # screen
        self.Screen = _epd2in9_V2.Screen()

        # logger
        self.Logger = _logger.Logger(0)

        # threadpool
        self.Pool = _threadpool.ThreadPool(20, self.Logger.warn)
        self.Pool.start()

        """
        
        # touchscreen
        self.Touch = self.simulator

        self.Touch.icnt_init()
        """

        # touchscreen
        self.Touch = icnt86.TouchDriver()
        self.Touch.icnt_init()

        self.TouchHandler = _TouchHandler(self)

        # themes
        self.themes = {}
        self.now_theme = "default"

        # applications
        self.apps = {}

        # plugins
        self.plugins = {}

        self.Now = None

        self.back_stack = _LifoQueue()

        # show
        self._show_left_back = False
        self._show_right_back = False
        self._update_temp = False
        self._home_bar = False
        self._home_bar_temp = 0

        # images
        self.none18px_img = _Image.open("resources/images/None18px.jpg")
        self.none20px_img = _Image.open("resources/images/None20px.jpg")
        self.docker_img = _Image.open("resources/images/docker.jpg")
        self.left_img = _Image.open("resources/images/back_left.png").convert("RGBA")
        self.left_img_alpha = self.left_img.split()[3]
        self.right_img = _Image.open("resources/images/back_right.png").convert("RGBA")
        self.right_img_alpha = self.right_img.split()[3]
        self.bar_img = _Image.open("resources/images/home_bar.png").convert("RGBA")
        self.bar_img_alpha = self.bar_img.split()[3]
        self.list_img = _Image.open("resources/images/list.png")
        self.list_more_img = _Image.open("resources/images/more_items_dots.jpg")
        self.app_control_img = _Image.open("resources/images/app_control.png")
        self.app_control_alpha = self.app_control_img.split()[3]
        self.page_with_title_img = _Image.open("resources/images/page_with_title.png")
        self.ok_img = _Image.open("resources/images/ok.png")
        self.ok_alpha = self.ok_img.split()[3]

    def __getattr__(self, name):
        if name in self.plugins:
            return self.plugins[name]
        else:
            raise AttributeError("plugins no found.")

    def display(self, image=None, refresh="a"):
        if not image:
            self.Now.display()
            return
        if self.display_lock.acquire(blocking=False):
            self.Screen.wait_busy()
            self.display_lock.release()

            self._update_temp = False

            if self._show_left_back:
                image.paste(self.left_img, mask=self.left_img_alpha)
            if self._show_right_back:
                image.paste(self.right_img, mask=self.right_img_alpha)
            if self._home_bar:
                image.paste(self.bar_img, mask=self.bar_img_alpha)

            if refresh == "a":
                self.Screen.display_auto(image)
            elif refresh == "t":
                self.Screen.display(image)
            elif refresh == "f":
                self.Screen.display_partial(image)

    def get_font(self, size=12):
        if size in self.fonts:
            return self.fonts[size]
        elif not size % 12:
            self.fonts[size] = _ImageFont.truetype("resources/fonts/VonwaonBitmap-12px.ttf", size)
        elif not size % 16:
            self.fonts[size] = _ImageFont.truetype("resources/fonts/VonwaonBitmap-16px.ttf", size)
        else:
            raise ValueError("It can only be a multiple of 12 or 16.")
        return self.fonts[size]

    def back_home(self) -> bool:
        self.back_stack.queue.clear()
        if self.Now is not self.themes[self.now_theme]:
            self.Now.pause()
            self.Now = self.themes[self.now_theme]
            self.Now.active()
            return True

    def open_app(self, target: str, to_stack=True, refresh=True):
        if target in self.apps:
            if self.apps[target] is not self.Now:
                self.Now.pause()
                if to_stack:  # TODO:在这里添加异常处理
                    self.back_stack.put(self.Now)
                self.Now = self.apps[target]
                self.Now.active(refresh)
        else:
            raise KeyError("The targeted application is not found.")

    def back(self) -> bool:
        self._update_temp = self._show_left_back or self._show_right_back
        self._show_left_back = False
        self._show_right_back = False
        if self.back_stack.empty():
            if self._update_temp:
                self.display()
            return self.Now.back()
        else:
            i = self.back_stack.get()
            if callable(i):
                i()
                if self._update_temp:
                    self.display()
                return True
            elif isinstance(i, _Base):
                if self.Now.back():
                    self.back_stack.put(i)
                else:
                    self.Now.pause()
                    self.Now = i
                    self.Now.active()
                if self._update_temp:
                    self.display()
                return True
            else:
                if self._update_temp:
                    self.display()
                return False

    def add_back(self, item):
        self.back_stack.put(item)

    def back_left(self, show: bool):
        if show:
            self._show_left_back = True
            self.display(refresh="f")
        else:
            self._show_left_back = False
            self.display(refresh="f")

    def back_right(self, show: bool):
        if show:
            self._show_right_back = True
            self.display(refresh="f")
        else:
            self._show_right_back = False
            self.display(refresh="f")

    def home_bar(self):
        if self._home_bar:
            self._home_bar = False
            if not self.back_home():
                self.display()
        else:
            self._home_bar = True
            self._home_bar_temp = _time.time()
            self.display()
            _time.sleep(1.5)
            if self._home_bar and _time.time() - self._home_bar_temp >= 1:
                self._home_bar = False
                self.display()

    def quit(self):
        for i in self.apps.values():
            self.Pool.add(i.shutdown)
        for i in self.plugins.values():
            self.Pool.add(i.shutdown)
        for i in self.themes.values():
            self.Pool.add(i.shutdown)
        _time.sleep(2)
        self.Screen.quit()

    def start(self):
        self.now_theme = self.config.read("theme")
        try:
            self.Now = self.themes[self.now_theme]
        except KeyError:
            self.now_theme = "默认（黑）"
            self.Now = self.themes["默认（黑）"]
            self.config.set("theme", "默认（黑）")
        self.Now.active()

    def poweroff(self):
        self.Logger.info("关机")
        self.Screen.display(_Image.open("resources/images/raspberry.jpg"))
        self.quit()
        _os.system("sudo poweroff")

    def reboot(self):
        self.Logger.info("重启")
        self.Screen.display(_Image.open("resources/images/raspberry.jpg"))
        self.quit()
        _os.system("sudo reboot")

    @staticmethod
    def clean_logs():
        _os.system("rm -f logs/*")

    def screenshot(self):
        return self.Now.Book.render()
