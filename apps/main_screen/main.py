import os
from datetime import datetime
from threading import Event
from cProfile import Profile
#from cProfile import runcall as profile

from mock import Mock
from apps import ZeroApp
from ui import Menu, PrettyPrinter, Canvas

from zerophone_hw import is_charging
from PIL import ImageFont

from __main__ import input_processor, cm # TODO: dirty hack, to be removed

class App(ZeroApp):

    menu_name = "Main screen"

    def __init__(self, *args, **kwargs):
        ZeroApp.__init__(self, *args, **kwargs)
        #input_processor.set_global_callback("KEY_HANGUP", self.switch_to_self)

    #def switch_to_self(self):
    #    cm.switch_to_context("apps/main_screen")

    def on_start(self, *args, **kwargs):
        screen = MainScreen([], self.i, self.o, "Main screen")
        screen.activate()
        screen.p.print_stats(2)

class MainScreen(Menu):
    is_numbered = False

    def set_view(self, config):
        self.view = Mock()

    def idle_loop(self):
        Menu.idle_loop(self)
        self.refresh()

    #def switch_to_main_menu(self):
    #    cm.switch_to_context("main")

    #def switch_to_stopwatch(self):
    #    cm.switch_to_context("stopwatch")

    #def generate_keymap(self):
    #    keymap = {"KEY_F1":self.switch_to_main_menu, "KEY_F2":self.switch_to_stopwatch}
    #    Menu.generate_keymap(self)
    #    self.keymap.update(keymap)

    def validate_contents(self, contents):
        self.p = Profile()
        self.default_font = ImageFont.load_default()
        self.clock_font = ImageFont.truetype("ui/fonts/Fixedsys62.ttf", 32)
        pass

    def process_contents(self):
        pass

    def draw_battery_icon(self, c):
        c.rectangle((c.width-20, 0, c.width-2, 7), fill=None, outline="white")
        c.rectangle((c.width-16, 0, c.width-2, 7), fill="white")
        c.rectangle((c.width-22, 1, c.width-20, 6), fill="white", outline="white")
        if is_charging():
            c.text((c.width-15, -2), "Ch", font=self.default_font, fill="black")

    def draw_network_icon(self, c):
        c.line((3, 1, 3, 6), fill="white")
        c.line((1, 1, 5, 1), fill="white")
        c.point(((1, 2), (5, 2)), fill="white")
        offset = 7
        for x in reversed(range(6)):
            c.line((x*2+offset, 6-x, x*2+offset, 6), fill="white")
        

    def refresh(self):
        now = datetime.now()
        hhmm = now.strftime("%H:%M")
        ss = now.strftime("%S")
        ddmmyy = now.strftime("%d%m%y")
        c = Canvas(self.o)
        #c.line((0, 8, c.width, 8), fill="white")
        c.text((5, 8), hhmm, font=self.clock_font, fill="white")
        c.text((87, 23), ss, font=self.default_font, fill="white")
        c.text((90, 12), ddmmyy, font=self.default_font, fill="white")
        c.text((10, 39), "0 notifications", font=self.default_font, fill="white")
        self.draw_battery_icon(c)
        self.draw_network_icon(c)
        image = c.get_image()
        self.p.runcall( self.o.display_image, image )
        
        