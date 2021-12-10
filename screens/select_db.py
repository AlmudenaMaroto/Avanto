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
import sqlite3
import os
from datetime import date
from datetime import datetime


class AnimatedBox(MDList, AKAddWidgetAnimationBehavior):
    pass


class WindowManager_select(ScreenManager):

    def load_movimientos(self, screen_name):
        self.clear_widgets()
        self.current = screen_name
        self.add_widget(DataBaseWid_movimientos())

    def load_insertmovimientos(self, screen_name):
        self.clear_widgets()
        self.current = screen_name
        self.add_widget(InsertDataWid())

    def load_selectdb(self, screen_name):
        self.clear_widgets()
        self.current = screen_name
        self.add_widget(Selectdb())

    def load_updatedata_movimientos(self):
        self.clear_widgets()
        self.current = 'update_movimientos'
        self.add_widget(Selectdb())


class Selectdb(MDScreen):

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
        WindowManager_select.load_movimientos(self, 'db_movimientos')

    def goto_deporte(self, *args):
        pass

    def goto_vblesglobales(self, *args):
        pass


class DataBaseWid_movimientos(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.num_rows = 10
        self.ruta_APP_PATH = os.getcwd()
        self.ruta_DB_PATH_movimientos = self.ruta_APP_PATH + '/movimientos.db'
        self.ruta_DB_PATH_deporte = self.ruta_APP_PATH + '/deporte.db'
        self.ruta_DB_PATH_vblesglobales = self.ruta_APP_PATH + '/globales.db'
        self.check_memory()

    def goto_movimientos(self, *args):
        WindowManager_select.load_movimientos(self, 'db_movimientos')

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
        # elif self.mainwid.name_db == 'deporte':
        #     for i in cursor:
        #         wid = DataWid(self.mainwid)
        #         r0 = 'ID: ' + str(i[0]) + ' '
        #         r1 = i[1] + ' \n'
        #         r2 = i[2] + '\n'
        #         r3 = str(i[3]) + ' '
        #         wid.data_id = str(i[0])
        #         wid.data = r0 + r1 + r2 + r3
        #         self.ids.container.add_widget(wid)
        con.close()

    def create_new_product(self):
        self.num_rows = 10
        self.goto_insertdata()

    def add_10_more(self):
        self.num_rows = self.num_rows + 10
        self.check_memory()
        self.goto_movimientos()


class DataWid(BoxLayout):  # Usado en el check_memory para visualizar los registros en cada widget mini
    def __init__(self, **kwargs):
        super(DataWid, self).__init__()

    def update_data(self, data_id):
        # self.mainwid.goto_updatedata(data_id)
        pass


class InsertDataWid(BoxLayout):
    def __init__(self, **kwargs):
        super(InsertDataWid, self).__init__()
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
        WindowManager_select.load_movimientos(self, 'selectdb')


class UpdateDataWid(BoxLayout):
    def __init__(self, data_id, **kwargs):
        super(UpdateDataWid, self).__init__()
        self.data_id = data_id
        self.ruta_APP_PATH = os.getcwd()
        self.ruta_DB_PATH_movimientos = self.ruta_APP_PATH + '/movimientos.db'
        self.ruta_DB_PATH_deporte = self.ruta_APP_PATH + '/deporte.db'
        self.ruta_DB_PATH_vblesglobales = self.ruta_APP_PATH + '/globales.db'
        self.check_memory()

    def check_memory(self):
        con = sqlite3.connect(self.ruta_DB_PATH_movimientos)
        cursor = con.cursor()
        s = 'select ID,	[Fecha Operación],	Concepto,	Categoría,	Importe,	Etapa,	Ubicación from movimientos where ID='
        cursor.execute(s + self.data_id)
        for i in cursor:
            # self.ids.ti_id.text = i[0]
            self.ids.ti_fechao.text = i[1]
            self.ids.ti_Concepto.text = i[2]
            self.ids.ti_Categoria.text = i[3]
            self.ids.ti_Importe.text = str(i[4])
            self.ids.ti_Etapa.text = i[5]
            self.ids.ti_Ubi.text = i[6]
        con.close()

    def update_data(self):
        con = sqlite3.connect(self.mainwid.DB_PATH)
        cursor = con.cursor()
        d2 = self.ids.ti_fechao.text
        d3 = self.ids.ti_Concepto.text
        d4 = self.ids.ti_Categoria.text
        d5 = self.ids.ti_Importe.text
        d6 = self.ids.ti_Etapa.text
        d7 = self.ids.ti_Ubi.text
        a1 = (d2, d3, d4, d5, d6, d7)
        s1 = 'UPDATE movimientos SET'
        s2 = '[Fecha Operación]="%s",Concepto="%s",Categoría="%s",Importe=%s,Etapa="%s",Ubicación="%s"' % a1
        s3 = 'WHERE ID=%s' % self.data_id
        try:
            cursor.execute(s1 + ' ' + s2 + ' ' + s3)
            con.commit()
            con.close()
            self.mainwid.goto_database()
        except Exception as e:
            message = self.mainwid.Popup.ids.message
            self.mainwid.Popup.open()
            self.mainwid.Popup.title = "Data base error"
            if '' in a1:
                message.text = 'Uno o más campos están vacíos'
            else:
                message.text = str(e)
            con.close()

    def delete_data(self):
        con = sqlite3.connect(self.mainwid.DB_PATH)
        cursor = con.cursor()
        s = 'delete from movimientos where ID=' + self.data_id
        cursor.execute(s)
        con.commit()
        con.close()
        self.mainwid.goto_database()

    def back_to_dbw(self):
        self.mainwid.goto_database()


Builder.load_string(
    """
WindowManager_select:
    db_movimientos:
    selectdb:
    insert_movimientos:
    datawid:

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
    MDBoxLayout:
        orientation: "vertical"

        MyToolbar:
            id: _toolbar
        MDBoxLayout:
            size_hint_y: 0.1
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
                
<InsertDataWid>:
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
