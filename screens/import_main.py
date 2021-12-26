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
from kivy.uix.popup import Popup


class AnimatedBox(MDList, AKAddWidgetAnimationBehavior):
    pass


class MessagePopup(Popup):
    pass


class Eliminado(MDScreen):
    pass


class Actualizado(MDScreen):
    pass


class WindowManager_select(ScreenManager):
    def __init__(self, **kwargs):
        super(WindowManager_select, self).__init__()

    def refresh(self):
        pass


class Import_main(MDScreen):

    def on_enter(self):
        pass

    def on_leave(self):
        try:
            self.ids.list.clear_widgets()
        except:
            pass

    def goto_import(self, *args):
        pass

    def goto_export(self, *args):
        self.clear_widgets()
        self.current = 'selectDBWid_md'
        self.add_widget(SelectDBWid_md())


class SelectDBWid_md(BoxLayout):
    def __init__(self, **kwargs):
        super(SelectDBWid_md, self).__init__()
        self.name_db = ''

    def select_db(self):
        bbdd = self.ids.click_label.text
        self.name_db = bbdd  # Variable usable a nivel general
        if bbdd == 'movimientos':
            full_path = os.getcwd() + '/movimientos.db'
        elif bbdd == 'deporte':
            full_path = os.getcwd() + '/deporte.db'
        self.name_db = full_path

        self.clear_widgets()
        self.current = 'export_data'
        self.add_widget(Export_data(full_path, bbdd))

    def spinner_clicked(self, value):
        self.ids.click_label.text = value


class Export_data(BoxLayout):
    def __init__(self, full_path, bbdd, **kwargs):
        super(Export_data, self).__init__()
        self.num_rows = 10
        self.check_memory(full_path, bbdd)

    def check_memory(self, full_path, bbdd):
        self.ids.container.clear_widgets()

        con = sqlite3.connect(full_path)
        cursor = con.cursor()
        orden_execute = 'select * from ' + bbdd + ' ORDER BY ID DESC LIMIT ' + str(
            self.num_rows)
        cursor.execute(orden_execute)
        if bbdd == 'movimientos':
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
        elif bbdd == 'deporte':
            for i in cursor:
                wid = DataWid_deporte()
                r0 = 'ID: ' + str(i[0]) + ' '
                r1 = i[1] + ' \n'
                r2 = i[2] + '\n'
                r3 = str(i[3]) + ' '
                wid.data_id = str(i[0])
                wid.data = r0 + r1 + r2 + r3
                self.ids.container.add_widget(wid)
        con.close()

    def return_button(self):
        self.clear_widgets()
        self.current = 'selectDBWid_md'
        self.add_widget(SelectDBWid_md())

    def delete_all(self):
        if self.mainwid.name_db == 'movimientos':
            con = sqlite3.connect(self.mainwid.DB_PATH_movimientos)
            cursor = con.cursor()
            s1 = 'DELETE FROM movimientos'
            cursor.execute(s1)
        elif self.mainwid.name_db == 'deporte':
            con = sqlite3.connect(self.mainwid.DB_PATH_deporte)
            cursor = con.cursor()
            s1 = 'DELETE FROM deporte'
            cursor.execute(s1)
        con.commit()
        con.close()
        self.mainwid.goto_moddata()

    def white_button(self):
        con = sqlite3.connect(self.mainwid.DB_PATH_movimientos)
        cur = con.cursor()
        if platform == 'android':
            os.chdir('/storage/emulated/0/')
        if self.mainwid.name_db == 'movimientos':
            data = cur.execute("SELECT * FROM movimientos")
            with open('movimientos.csv', 'w') as f:
                writer = csv.writer(f, delimiter=';')
                writer.writerows(data)

        elif self.mainwid.name_db == 'deporte':
            data = cur.execute("SELECT * FROM deporte")
            with open('deporte.csv', 'w') as f:
                writer = csv.writer(f)
                writer.writerows(data)
        con.commit()
        con.close()
        message = self.mainwid.Popup.ids.message
        self.mainwid.Popup.open()
        self.mainwid.Popup.title = "Csv guardado"
        message.text = "Se ha guardado el csv en \n" + str(os.getcwd())


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

    def goto_deporte(self, *args):
        self.clear_widgets()
        self.current = 'db_deporte'
        self.add_widget(DataBaseWid_deporte())

    def goto_vblesglobales(self, *args):
        self.clear_widgets()
        self.current = 'db_vblesglob'
        self.add_widget(Vbles_globalesWid())


class DataWid(BoxLayout):  # Usado en el check_memory para visualizar los registros en cada widget mini
    def __init__(self, **kwargs):
        super(DataWid, self).__init__()
        self.Selectdb = Selectdb

    def update_data(self, data_id):
        self.clear_widgets()
        self.current = 'update_movimientos'
        self.add_widget(UpdateDataWid_movimientos(data_id))


class DataWid_deporte(BoxLayout):  # Usado en el check_memory para visualizar los registros en cada widget mini
    def __init__(self, **kwargs):
        super(DataWid_deporte, self).__init__()
        self.Selectdb = Selectdb

    def update_data(self, data_id):
        self.clear_widgets()
        self.current = 'update_deporte'
        self.add_widget(UpdateDataWid_deporte(data_id))


Builder.load_string(
    """
WindowManager_select:
    import_main:
    selectDBWid_md:
    export_data:

<Import_main>:
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
                    text:'Importación'
                    on_release:root.goto_import()
                Button:
                    size_hint_y: 0.1
                    text:'Exportación'
                    on_release:root.goto_export()

<SelectDBWid_md>:
    name:"selectDBWid_md"
    orientation: 'vertical'
    canvas:
        Color:
            rgb: .254,.556,.627
        Rectangle:
            pos: self.pos
            size: self.size
    MDBoxLayout:
        orientation: "vertical"

        MyToolbar:
            id: _toolbar
        Button:
            size_hint_y: .1
            text: 'Modificación masiva de datos'
            on_press: root.select_db()
    
        Label:
            id: click_label
            text: 'Elige BBDD'
    
        Spinner:
            id: spinner_id
            text: 'Elige la base de datos'
            values: ["movimientos", "deporte"]
            size_hint_y: .1
    
            on_text: root.spinner_clicked(spinner_id.text)

<Export_data>:
    name: "export_data"
    orientation:'vertical'
    canvas:
        Color:
            rgb: .254,.556,.627
        Rectangle:
            pos: self.pos
            size: self.size
    
    MDBoxLayout:
        orientation: "vertical"

        MyToolbar:
            id: _toolbar
        BoxLayout:
            size_hint_y: 0.1
            Button: # -----------Go back
                font_size: self.height*0.3
                text: 'Atrás'
                pos: 1, 1
                size: 10, 50
                on_press: root.return_button()
            Button: #
                font_size: self.height*0.3
                text: 'Eliminar todo'
                pos: 1, 1
                size: 10, 50
                on_press: root.delete_all()
            Button: # ---------Save
                font_size: self.height*0.3
                text: 'Guardar csv'
                pos: 1, 1
                size: 10, 50
                on_press: root.white_button()
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
        
<DataWid_deporte>:
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
