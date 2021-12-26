from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen
from kivymd.uix.list import MDList, OneLineListItem

from kivymd_extensions.akivymd.uix.behaviors.addwidget import (
    AKAddWidgetAnimationBehavior,
)
from main import DemoApp
from kivymd.uix.screen import MDScreen
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
import sqlite3
import os
from datetime import date
from datetime import datetime


class AnimatedBox(MDList, AKAddWidgetAnimationBehavior):
    pass


class MessagePopup(Popup):
    pass


class WindowManager_select(ScreenManager):
    pass


class Selectdb(MDScreen):

    def on_enter(self):
        pass

    def on_leave(self):
        self.ids.list.clear_widgets()

    def goto_movimientos(self, *args):
        self.clear_widgets()
        self.current = 'db_movimientos'
        self.add_widget(DataBaseWid_movimientos())



class DataBaseWid_movimientos(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.Selectdb = Selectdb


    def goto_main(self):
        self.clear_widgets()
        self.current = 'selectdb'
        self.add_widget(Selectdb())


Builder.load_string(
    """
WindowManager_select:
    db_movimientos:
    selectdb:
    insert_movimientos:
    datawid:
    update_movimientos:

<Selectdb>:
    name:"selectdb"
    MDBoxLayout:
        orientation: "vertical"

        MyToolbar:
            id: _toolbar

        ScrollView:
            BoxLayout:
                orientation: "vertical"
                Label:
                    size_hint_y: 0.1
                    text:'Prueba'
                Button:
                    size_hint_y: 0.1
                    text:'Movimientos'
                    on_release:root.goto_movimientos()

<DataBaseWid_movimientos>:
    name:"db_movimientos"
    MDBoxLayout:
        orientation: "vertical"

        MyToolbar:
            id: _toolbar
        MDBoxLayout:
            size_hint_y: 0.1
            Button: # -----------Back
                font_size: self.height*0.35
                text: 'Atrás'
                on_press: root.goto_main()
            Button: # -----------Add 10 rows
                font_size: self.height*0.35
                text: 'Añadir 10 filas'
                on_press: root.add_10_more()
            Button: # ---------Add
                font_size: self.height*0.35
                text: '+'
                on_press: root.create_new_product()
        MDBoxLayout:
            size_hint_y:0.9
                

"""
)
