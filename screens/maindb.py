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
    def __init__(self, **kwargs):
        super(WindowManager_select, self).__init__()
        self.Maindb = Maindb()

    def load_movimientos(self):
        # Al clickar en movimientos: self = Maindb screenname=maindb
        self.clear_widgets()
        self.current = 'startwid'
        self.add_widget(StartWid(self))

    def load_main(self):
        # Al clickar en movimientos: self = Maindb screenname=maindb
        self.clear_widgets()
        self.current = 'maindb'
        self.add_widget(Maindb())


class Maindb(MDScreen):

    def on_enter(self):
        # self = Maindb screenname maindb
        self.update()

    def update(self, *args):
        items = []
        # Añadimos todas las Bases de Datos que vamos a emplear a la lista
        items.append(OneLineListItem(text=f"movimientos", on_release=self.goto_movimientos))
        items.append(OneLineListItem(text=f"deporte", on_release=self.goto_deporte))
        items.append(OneLineListItem(text=f"variables globales", on_release=self.goto_vblesglobales))
        self.ids.list.items = items
        a = 'stop'

    def on_leave(self):
        self.ids.list.clear_widgets()

    def goto_movimientos(self, *args):
        WindowManager_select.load_movimientos(self)

    def goto_deporte(self, *args):
        WindowManager_select.load_deporte(self, 'db_deporte')

    def goto_vblesglobales(self, *args):
        pass

    def goto_main(self):
        # Al ir "Atrás"
        WindowManager_select.load_main(self)


class StartWid(BoxLayout):
    def __init__(self, mainwid, **kwargs):
        super(StartWid, self).__init__()
        self.mainwid = mainwid

    def create_database(self):  # Esta funcion no está siendo usada
        name = self.ids.click_label.text
        if self.mainwid.name_db == 'moviemientos':
            self.mainwid.DB_PATH_movimientos = connect_to_database(self.mainwid.DB_PATH_movimientos, name)
        elif self.mainwid.name_db == 'deporte':
            self.mainwid.DB_PATH_deporte = connect_to_database(self.mainwid.DB_PATH_deporte, name)
        self.mainwid.goto_database()

    def open_browser(self):
        self.mainwid.goto_selectdb_fb()

    def mod_data(self):
        self.mainwid.goto_selectdb_md()

    def data_analysis(self):
        self.mainwid.goto_data_analysis()

    def select_database(self):
        self.mainwid.goto_selectdb()

    def global_vbles(self):
        self.mainwid.goto_vbles_globales()

    def nevera(self):
        pass

    def calorias(self):
        pass

    def deporte(self):
        pass


class DataBaseWid_movimientos(MDScreen):
    def __init__(self, Maindb, **kwargs):
        super().__init__(**kwargs)
        self.num_rows = 10
        self.ruta_APP_PATH = os.getcwd()
        self.ruta_DB_PATH_movimientos = self.ruta_APP_PATH + '/movimientos.db'
        self.ruta_DB_PATH_deporte = self.ruta_APP_PATH + '/deporte.db'
        self.ruta_DB_PATH_vblesglobales = self.ruta_APP_PATH + '/globales.db'
        self.check_memory()
        self.Maindb = Maindb

    def goto_movimientos(self, *args):
        WindowManager_select.load_movimientos(self)

    def goto_insertdata(self, *args):
        WindowManager_select.load_insertmovimientos(self, 'insert_movimientos')

    def check_memory(self):
        self.ids.container.clear_widgets()

        con = sqlite3.connect(self.ruta_DB_PATH_movimientos)
        cursor = con.cursor()
        orden_execute = 'select * from movimientos ORDER BY ID DESC LIMIT ' + str(
            self.num_rows)
        cursor.execute(orden_execute)
        for i in cursor:
            wid = DataWid()
            r0 = 'ID: ' + str(i[0]) + ' '
            r1 = i[1] + ' \n'
            r2 = i[2] + '\n'
            r3 = str(i[3]) + ' '
            r4 = i[5] + '\n'
            r5 = str(i[4]) + ' €\n'
            r6 = i[6][0:20] + '...\n'
            wid.data_id = str(i[0])
            wid.data = r0 + r1 + r2 + r3 + r4 + r5 + r6
            self.ids.container.add_widget(wid)
        con.close()

    def create_new_product(self):
        self.num_rows = 10
        self.goto_insertdata()

    def add_10_more(self):
        self.num_rows = self.num_rows + 10
        self.check_memory()
        self.goto_movimientos()

    def return_button(self):
        self.num_rows = 10
        self.Maindb.goto_main()


class DataWid(BoxLayout):  # Usado en el check_memory para visualizar los registros en cada widget mini
    def __init__(self, **kwargs):
        super(DataWid, self).__init__()
        self.Maindb = Maindb

    def update_data(self, data_id):
        WindowManager_select.load_updatedata_movimientos(self, data_id)


Builder.load_string(
    """
WindowManager_select:
    maindb:
    startwid:
    db_movimientos:
    insert_movimientos:
    datawid:
    update_movimientos:

<Maindb>:
    name:"maindb"
    MDBoxLayout:
        orientation: "vertical"
        MyToolbar:
            id: _toolbar
        ScrollView:
            AnimatedBox:
                id: list
                transition: "fade_size"
<StartWid>:
    name:"startwid"
    MDBoxLayout:
        orientation: "vertical"

        MyToolbar:
            id: _toolbar
        MDBoxLayout:
            orientation: 'vertical'
            canvas:
                Color:
                    rgb: .254,.556,.627
                Rectangle:
                    pos: self.pos
                    size: self.size
            Label:
                id: texto_inicial
                size_hint_y: .1
                rgb: 0.2, 0.2, 0.2
                text: '¡Bienvenid@ a Avanto!'
            Label:
                id: texto_inicial
                size_hint_y: .2
                rgb: 0.2, 0.2, 0.2
                text: 'Inicie los ficheros en "Seleccionar base de datos"'
        
            Button:
                size_hint_y: .1
                text: 'Seleccionar base de datos'
                on_press: root.select_database()
            Button:
                size_hint_y: .1
                text: 'Modificar variables globales'
                on_press: root.global_vbles()
        
            BoxLayout:
                size_hint_y: .1
                Label:
                    text:'Para realizar cambios de forma masiva:'
        
            Button:
                size_hint_y: .1
                text: 'Modificación masiva de datos'
                on_press: root.mod_data()
            Button:
                size_hint_y: .1
                text: 'Importación masiva de datos'
                on_press: root.open_browser()
        
            BoxLayout:
                size_hint_y: .1
                Label:
                    text:'Visualizaciones: '



            
<DataBaseWid_movimientos>:
    name:"db_movimientos"
    MDBoxLayout:
        orientation: "vertical"

        MyToolbar:
            id: _toolbar
        MDBoxLayout:
            size_hint_y: 0.1
            Button: # -----------Go back
                font_size: self.height*0.25
                text: 'Atrás'
                on_press: root.return_button()
            Button: # -----------Add 10 rows
                font_size: self.height*0.35
                text: 'Añadir 10 filas'
                on_press: root.add_10_more()
            Button: # ---------Add
                font_size: self.height*0.35
                text: '+'
                on_press: root.create_new_product()
        ScrollView:
            size: self.size
            GridLayout:
                id: container
                padding: [10,10,10,10]
                spacing: 5
                size_hint_y: None
                cols: 1
                row_default_height: root.height*0.2
                height: self.minimum_height

<DataWid>:
    name:"datawid"
    data: ''
    data_id: ''
    canvas:
        Color:
            rgb: 0.2,0.2,0.2
        Rectangle:
            size: self.size
            pos: self.pos
    Label:
        size_hint_x: 0.9
        size_font: self.width*0.4
        text: root.data
    Button:
        size_hint_x: 0.1
        text: 'Edit'
        on_press: root.update_data(root.data_id)

"""
)
