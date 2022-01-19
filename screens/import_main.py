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
from kivy.utils import platform
import csv
from kivy.uix.label import Label

# Permisos de acceso a las carpetas del movil para poder importar y exportar
if platform == 'android':
    from android.permissions import request_permissions, Permission

    request_permissions([Permission.WRITE_EXTERNAL_STORAGE])


class AnimatedBox(MDList, AKAddWidgetAnimationBehavior):
    pass


class MessagePopup_import(Popup):
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
    def __init__(self, **kwargs):
        super(Import_main, self).__init__()
        self.name_db = ''

    def export_db(self):
        bbdd = self.ids.click_label.text
        self.name_db = bbdd  # Variable usable a nivel general
        if bbdd == 'Movimientos bancarios':
            bbdd = 'movimientos'
            full_path = os.getcwd() + '/movimientos.db'
            self.clear_widgets()
            self.current = 'export_data'
            self.add_widget(Export_data(full_path, bbdd))
        elif bbdd == 'Registro deporte':
            bbdd = 'deporte'
            full_path = os.getcwd() + '/deporte.db'
            self.clear_widgets()
            self.current = 'export_data'
            self.add_widget(Export_data(full_path, bbdd))
        elif bbdd == 'Variables globales':
            bbdd = 'globales'
            full_path = os.getcwd() + '/globales.db'
            self.clear_widgets()
            self.current = 'export_data'
            self.add_widget(Export_data(full_path, bbdd))

    def import_db(self):
        bbdd = self.ids.click_label.text
        self.name_db = bbdd  # Variable usable a nivel general
        if bbdd == 'Movimientos bancarios':
            bbdd = 'movimientos'
            full_path = os.getcwd() + '/movimientos.db'
            self.clear_widgets()
            self.current = 'import_data'
            self.add_widget(Import_data(full_path, bbdd))
        elif bbdd == 'Registro deporte':
            bbdd = 'deporte'
            full_path = os.getcwd() + '/deporte.db'
            self.clear_widgets()
            self.current = 'import_data'
            self.add_widget(Import_data(full_path, bbdd))
        elif bbdd == 'Variables globales':
            bbdd = 'globales'

    def spinner_clicked(self, value):
        self.ids.click_label.text = value


class Export_data(BoxLayout):
    def __init__(self, full_path, bbdd, **kwargs):
        super(Export_data, self).__init__()
        self.num_rows = 10
        self.full_path = full_path
        self.bbdd = bbdd
        self.Popup = MessagePopup_import()
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
                wid = DataWid_import()
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
                wid = DataWid_import_deporte()
                r0 = 'ID: ' + str(i[0]) + ' '
                r1 = i[1] + ' \n'
                r2 = i[2] + '\n'
                r3 = str(i[3]) + ' '
                wid.data_id = str(i[0])
                wid.data = r0 + r1 + r2 + r3
                self.ids.container.add_widget(wid)
        elif bbdd == 'globales':
            self.ids.container.add_widget(Label(text="¿Desea guardar en un csv las variables globales?"), index=0)
        con.close()

    def return_button(self):
        self.clear_widgets()
        self.current = 'import_main'
        self.add_widget(Import_main())

    def delete_all(self):
        if self.bbdd == 'movimientos':
            con = sqlite3.connect(self.full_path)
            cursor = con.cursor()
            s1 = 'DELETE FROM movimientos'
            cursor.execute(s1)
        elif self.bbdd == 'deporte':
            con = sqlite3.connect(self.full_path)
            cursor = con.cursor()
            s1 = 'DELETE FROM deporte'
            cursor.execute(s1)
        con.commit()
        con.close()

        self.clear_widgets()
        self.current = 'export_data'
        self.add_widget(Export_data(self.full_path, self.bbdd))

    def save_csv(self):
        con = sqlite3.connect(self.full_path)
        cur = con.cursor()
        if platform == 'android':
            os.chdir('/storage/emulated/0/')
        if self.bbdd == 'movimientos':
            data = cur.execute("SELECT * FROM movimientos")
            with open('movimientos.csv', 'w', newline='', encoding='latin') as f:
                writer = csv.writer(f, delimiter=';')
                writer.writerows(data)

        elif self.bbdd == 'deporte':
            data = cur.execute("SELECT * FROM deporte")
            with open('deporte.csv', 'w', newline='', encoding='latin') as f:
                writer = csv.writer(f, delimiter=';')
                writer.writerows(data)
        elif self.bbdd == 'globales':
            data = cur.execute("SELECT * FROM globales")
            with open('globales.csv', 'w', newline='', encoding='latin') as f:
                writer = csv.writer(f, delimiter=';')
                writer.writerows(data)
        con.commit()
        con.close()
        message = self.Popup.ids.message
        self.Popup.open()
        self.Popup.title = "Csv guardado"
        message.text = "Se ha guardado el csv en \n" + str(os.getcwd())


class Import_data(BoxLayout):
    def __init__(self, full_path, bbdd, **kwargs):
        super(Import_data, self).__init__()
        self.file_name = ''
        self.Popup = MessagePopup_import()
        self.full_path = full_path
        self.bbdd = bbdd

    def open_file(self, path, filename):
        if ".csv" in filename[0]:
            with open(os.path.join(path, filename[0]), encoding='latin') as f:
                row = f.read()
                row2 = row.split('\n')
                i = 0
                incorrectas = 0
                for each_row in row2:
                    try:
                        string_list = each_row.split(";")
                        string_list[0] = string_list[0].replace("ï»¿", "")
                        if self.bbdd == 'movimientos':
                            string_list[4] = round(float(string_list[4].replace(",", ".")), 2)
                            string_list = tuple(string_list)
                            con = sqlite3.connect(self.full_path)
                            cursor = con.cursor()
                            s1 = 'INSERT INTO movimientos(ID, [Fecha Operación], Concepto, Categoría, Importe, Etapa, Ubicación)'
                            s2 = 'VALUES(%s,"%s","%s","%s",%s,"%s","%s")' % string_list
                            cursor.execute(s1 + ' ' + s2)
                        elif self.bbdd == 'deporte':
                            string_list[3] = round(float(string_list[3].replace(",", ".")), 2)
                            string_list = tuple(string_list)
                            con = sqlite3.connect(self.full_path)
                            cursor = con.cursor()
                            s1 = 'INSERT INTO deporte(ID,	[Fecha Operación],	Concepto, Tiempo)'
                            s2 = 'VALUES(%s,"%s","%s",%s)' % string_list
                            cursor.execute(s1 + ' ' + s2)
                        con.commit()
                        con.close()
                    except:
                        incorrectas = incorrectas + 1
                    i = i + 1
                # print("Hay", incorrectas, "líneas incorrectas")
                message = self.Popup.ids.message
                self.Popup.open()
                self.Popup.title = "Líneas generadas"
                message.text = "Hay " + str(incorrectas - 1) + " con formato incorrecto o ID repetido"
        else:
            message = self.Popup.ids.message
            self.Popup.open()
            self.Popup.title = "Error de formato"
            message.text = 'El fichero no es un csv'

    def selectfile(self, filename):
        self.file_name = filename

    def return_button(self):
        self.clear_widgets()
        self.current = 'import_main'
        self.add_widget(Import_main())


class UpdateDataWid_import_movimientos_import(BoxLayout):
    def __init__(self, data_id, **kwargs):
        super(UpdateDataWid_import_movimientos_import, self).__init__()
        self.data_id = data_id
        self.ruta_APP_PATH = os.getcwd()
        self.ruta_DB_PATH_movimientos = self.ruta_APP_PATH + '/movimientos.db'
        self.ruta_DB_PATH_deporte = self.ruta_APP_PATH + '/deporte.db'
        self.ruta_DB_PATH_vblesglobales = self.ruta_APP_PATH + '/globales.db'
        self.check_memory()
        self.WindowManager_select = WindowManager_select
        self.Popup = MessagePopup_import()

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
        con = sqlite3.connect(self.ruta_DB_PATH_movimientos)
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

        except Exception as e:
            message = self.Popup.ids.message
            self.Popup.open()
            self.Popup.title = "Data base error"
            if '' in a1:
                message.text = 'Uno o más campos están vacíos'
            else:
                message.text = str(e)
            con.close()
        self.clear_widgets()
        self.add_widget(Actualizado())

    def delete_data(self):
        con = sqlite3.connect(self.ruta_DB_PATH_movimientos)
        cursor = con.cursor()
        s = 'delete from movimientos where ID=' + self.data_id
        cursor.execute(s)
        con.commit()
        con.close()
        self.back_to_dbw()

    def back_to_dbw(self):
        self.clear_widgets()
        self.add_widget(Eliminado())


class UpdateDataWid_import_deporte_import(BoxLayout):
    def __init__(self, data_id, **kwargs):
        super(UpdateDataWid_import_deporte_import, self).__init__()
        self.data_id = data_id
        self.ruta_APP_PATH = os.getcwd()
        self.ruta_DB_PATH_movimientos = self.ruta_APP_PATH + '/movimientos.db'
        self.ruta_DB_PATH_deporte = self.ruta_APP_PATH + '/deporte.db'
        self.ruta_DB_PATH_vblesglobales = self.ruta_APP_PATH + '/globales.db'
        self.check_memory()
        self.WindowManager_select = WindowManager_select
        self.Popup = MessagePopup_import()

    def check_memory(self):
        con = sqlite3.connect(self.ruta_DB_PATH_deporte)
        cursor = con.cursor()
        s = 'select ID,	[Fecha Operación], Concepto, Tiempo from deporte where ID='
        cursor.execute(s + self.data_id)
        for i in cursor:
            # self.ids.ti_id.text = i[0]
            self.ids.ti_fechao.text = i[1]
            self.ids.ti_Concepto.text = i[2]
            self.ids.ti_Tiempo.text = str(i[3])
        con.close()

    def update_data(self):
        con = sqlite3.connect(self.ruta_DB_PATH_deporte)
        cursor = con.cursor()
        d2 = self.ids.ti_fechao.text
        d3 = self.ids.ti_Concepto.text
        d5 = self.ids.ti_Tiempo.text
        a1 = (d2, d3, d5)
        s1 = 'UPDATE deporte SET'
        s2 = '[Fecha Operación]="%s",Concepto="%s",Tiempo=%s' % a1
        s3 = 'WHERE ID=%s' % self.data_id
        try:
            cursor.execute(s1 + ' ' + s2 + ' ' + s3)
            con.commit()
            con.close()

        except Exception as e:
            message = self.Popup.ids.message
            self.Popup.open()
            self.Popup.title = "Data base error"
            if '' in a1:
                message.text = 'Uno o más campos están vacíos'
            else:
                message.text = str(e)
            con.close()
        self.clear_widgets()
        self.add_widget(Actualizado())

    def delete_data(self):
        con = sqlite3.connect(self.ruta_DB_PATH_deporte)
        cursor = con.cursor()
        s = 'delete from deporte where ID=' + self.data_id
        cursor.execute(s)
        con.commit()
        con.close()
        self.back_to_dbw()

    def back_to_dbw(self):
        self.clear_widgets()
        self.add_widget(Eliminado())


class DataWid_import(BoxLayout):  # Usado en el check_memory para visualizar los registros en cada widget mini
    def __init__(self, **kwargs):
        super(DataWid_import, self).__init__()

    def update_data(self, data_id):
        self.clear_widgets()
        self.current = 'update_movimientos'
        self.add_widget(UpdateDataWid_import_movimientos_import(data_id))


class DataWid_import_deporte(BoxLayout):  # Usado en el check_memory para visualizar los registros en cada widget mini
    def __init__(self, **kwargs):
        super(DataWid_import_deporte, self).__init__()

    def update_data(self, data_id):
        self.clear_widgets()
        self.current = 'update_deporte'
        self.add_widget(UpdateDataWid_import_deporte_import(data_id))


Builder.load_string(
    """
#:import platform kivy.utils.platform
WindowManager_select:
    import_main:
    selectDBWid_md:
    export_data:
    import_data:

<Import_main>:
    name:"import_main"
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
        MDBoxLayout:
            orientation: "horizontal"
            size_hint_y: .1
            Button:
                text: 'Exportar'
                on_press: root.export_db()
            Button:
                text: 'Importar'
                on_press: root.import_db()
    
        Label:
            id: click_label
            text: 'Elige BBDD'
    
        Spinner:
            id: spinner_id
            text: 'Elige la base de datos'
            values: ["Movimientos bancarios", "Registro deporte", "Variables globales"]
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
                on_press: root.save_csv()
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

<Import_data>:
    name:"import_data"
    id:my_widget
    cols:2
    orientation: 'vertical'
    canvas:
        Color:
            rgb: .254,.556,.627
        Rectangle:
            pos: self.pos
            size: self.size
    BoxLayout:
        size_hint_y: 0.1
        orientation: 'vertical'
        BoxLayout:
            size_hint_y: 0.1
            orientation: 'horizontal'
            Button: # ---------Return
                font_size: self.height*0.25
                text:"Salir"
                pos: 1, 1
                size: 1, 5
                #size_hint_y: 0.1
                on_press: root.return_button()
            Button: # ---------Add
                font_size: self.height*0.25
                text:"Abrir"
                pos: 1, 1
                size: 1, 5
                #size_hint_y: 0.1
                on_press: root.open_file(filechooser.path, filechooser.selection)
        FileChooserListView:
            rootpath: '/storage/emulated/0/' if platform == 'android' else '/'
            id:filechooser
            on_selection: my_widget.selectfile(filechooser.selection)


<DataWid_import>:
    name:"DataWid_import"
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
        
<DataWid_import_deporte>:
    name:"DataWid_import"
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
        
<MessagePopup_import>:
    BoxLayout:
        orientation: 'vertical'
        Label:
            id: message
            size_hint: 1,0.8
            text: ''
        Button:
            size_hint: 1,0.2
            text: 'Regresar'
            on_press: root.dismiss()
      
"""
)
