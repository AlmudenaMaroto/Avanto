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
        try:
            self.ids.list.clear_widgets()
        except:
            pass

    def goto_movimientos(self, *args):
        self.clear_widgets()
        self.current = 'db_movimientos'
        self.add_widget(DataBaseWid_movimientos())


class DataBaseWid_movimientos(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.Selectdb = Selectdb
        self.num_rows = 10
        self.ruta_APP_PATH = os.getcwd()
        self.ruta_DB_PATH_movimientos = self.ruta_APP_PATH + '/movimientos.db'
        self.ruta_DB_PATH_deporte = self.ruta_APP_PATH + '/deporte.db'
        self.ruta_DB_PATH_vblesglobales = self.ruta_APP_PATH + '/globales.db'
        self.check_memory()

    def goto_main(self):
        self.clear_widgets()
        self.current = 'selectdb'
        self.add_widget(Selectdb())

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

    def add_10_more(self):
        self.num_rows = self.num_rows + 10
        self.check_memory()

    def create_new_product(self):
        self.num_rows = 10
        self.clear_widgets()
        self.current = 'insert_movimientos'
        self.add_widget(InsertDataWid_movimientos())


class DataWid(BoxLayout):  # Usado en el check_memory para visualizar los registros en cada widget mini
    def __init__(self, **kwargs):
        super(DataWid, self).__init__()
        self.Selectdb = Selectdb

    def update_data(self, data_id):
        # WindowManager_select.load_updatedata_movimientos(self, data_id)
        pass


class InsertDataWid_movimientos(BoxLayout):
    def __init__(self, **kwargs):
        super(InsertDataWid_movimientos, self).__init__()
        today = date.today()
        d1 = today.strftime("%d/%m/%Y")
        self.ids.ti_fechao.text = d1
        self.ruta_APP_PATH = os.getcwd()
        self.ruta_DB_PATH_movimientos = self.ruta_APP_PATH + '/movimientos.db'
        self.ruta_DB_PATH_deporte = self.ruta_APP_PATH + '/deporte.db'
        self.ruta_DB_PATH_vblesglobales = self.ruta_APP_PATH + '/globales.db'

    def insert_data(self):
        con = sqlite3.connect(self.ruta_DB_PATH_movimientos)
        cursor = con.cursor()
        cursor.execute('select ID from movimientos ORDER BY ID DESC LIMIT 1')
        con.commit()
        #
        d1 = 1
        for i in cursor:
            d1 = i[0] + 1
        con.close()
        con = sqlite3.connect(self.ruta_DB_PATH_movimientos)
        cursor = con.cursor()
        d2 = self.ids.ti_fechao.text
        d3 = self.ids.ti_Concepto.text
        d4 = self.ids.ti_Categoria.text
        d5 = self.ids.ti_Importe.text
        d6 = self.ids.ti_Etapa.text
        d7 = self.ids.ti_Ubi.text
        a1 = (d1, d2, d3, d4, d5, d6, d7)
        s1 = 'INSERT INTO movimientos(ID,	[Fecha Operación],	Concepto,	Categoría,	Importe,	Etapa,	Ubicación)'
        s2 = 'VALUES(%s,"%s","%s","%s",%s,"%s","%s")' % a1
        try:
            cursor.execute(s1 + ' ' + s2)
            con.commit()
            con.close()
            self.back_to_dbw()
        except Exception as e:
            message = self.mainwid.Popup.ids.message
            self.mainwid.Popup.open()
            self.mainwid.Popup.title = "Data base error"
            if '' in a1:
                message.text = 'Uno o más campos están vacíos'
            else:
                message.text = str(e)
            con.close()

    def back_to_dbw(self):
        self.clear_widgets()
        self.current = 'db_movimientos'
        self.add_widget(DataBaseWid_movimientos())


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
                       
<InsertDataWid_movimientos>:
    name:"insert_movimientos"
    orientation: 'vertical'
    canvas:
        Color:
            rgb: .254,.556,.627
        Rectangle:
            pos: self.pos
            size: self.size

    Label: # ---------- Fecha
        text: ' Fecha Operación:'
    TextInput:
        id: ti_fechao
        multiline: False
        # hint_text: 'Fecha Operación:'
        # text: 'ids.ti_fechao'
    Label: # ---------- Concepto
        text: ' Concepto:'
    TextInput:
        id: ti_Concepto
        multiline: False
        hint_text: 'Concepto:'
    Label: # ---------- Categoría
        text: ' Categoría:'
    TextInput:
        id: ti_Categoria
        multiline: False
        hint_text: 'Categoría'
    Label: # ---------- Importe
        text: ' Importe:'
    TextInput:
        id: ti_Importe
        multiline: False
        hint_text: 'Importe'
    Label:  # ---------- Etapa
        text: ' Etapa:'
    TextInput:
        id: ti_Etapa
        multiline: False
    Label:  # ---------- Ubicación
        text: ' Ubicación:'
    TextInput:
        id: ti_Ubi
        multiline: False
    BoxLayout:
        size_hint_y: 5
    BoxLayout: # ---------- Crear Salir
        Button:
            text: 'Crear'
            on_press: root.insert_data()
        Button:
            text: 'Salir'
            on_press: root.back_to_dbw()
"""
)
