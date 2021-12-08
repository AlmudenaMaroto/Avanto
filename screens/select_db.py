from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen
from kivymd.uix.list import MDList, OneLineListItem

from kivymd_extensions.akivymd.uix.behaviors.addwidget import (
    AKAddWidgetAnimationBehavior,
)
from main import DemoApp
from kivymd.uix.screen import MDScreen
from kivy.uix.screenmanager import ScreenManager, Screen


class AnimatedBox(MDList, AKAddWidgetAnimationBehavior):
    pass


class DataBaseWid_movimientos(MDScreen):
    pass


class WindowManager_select(ScreenManager):

    def load_screen(self, screen_name):
        self.clear_widgets()
        self.current = screen_name
        self.add_widget(DataBaseWid_movimientos())


class Selectdb(MDScreen):
    def __init__(self, **kwargs):
        super().__init__()
        self.WindowManager_select = WindowManager_select

    def on_enter(self):
        self.update()

    def update(self, *args):
        items = []
        # Añadimos todas las Bases de Datos que vamos a emplear a la lista
        items.append(OneLineListItem(text=f"movimientos", on_release=self.goto_movimientos))
        items.append(OneLineListItem(text=f"deporte", on_release=self.goto_deporte))
        items.append(OneLineListItem(text=f"variables globales", on_release=self.goto_vblesglobales))
        self.ids.list.items = items

    def on_leave(self):
        self.ids.list.clear_widgets()

    def goto_movimientos(self, *args):
        WindowManager_select.load_screen(self, 'db_movimientos')

    def goto_deporte(self, *args):
        pass

    def goto_vblesglobales(self, *args):
        pass


Builder.load_string(
    """
WindowManager_select:
    db_movimientos:
    selectdb:

<Selectdb>:
    name:"selectdb"
    MDBoxLayout:
        orientation: "vertical"

        MyToolbar:
            id: _toolbar

        ScrollView:

            AnimatedBox:
                id: list
                transition: "fade_size"

<DataBaseWid_movimientos>:
    name:"db_movimientos"
    MDLabel:
        text:"movimientos!!!"
"""
)
