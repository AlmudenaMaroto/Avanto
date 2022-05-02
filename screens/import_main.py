from kivy.lang.builder import Builder

from kivymd.uix.list import MDList, OneLineListItem

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
from kivy.properties import StringProperty

# Permisos de acceso a las carpetas del movil para poder importar y exportar
if platform == 'android':
    from android.permissions import request_permissions, Permission

    request_permissions([Permission.WRITE_EXTERNAL_STORAGE])


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
        self.tabla_seleccionada = 'empty'

    def on_enter(self):
        pass

    def on_leave(self):
        try:
            self.ids.list.clear_widgets()
        except:
            pass

    def goto_movimientos(self, *args):
        self.clear_widgets()
        self.current = 'impexpelm'
        self.add_widget(Impexpelm('Movimientos bancarios'))

    def goto_deporte(self, *args):
        self.clear_widgets()
        self.current = 'impexpelm'
        self.add_widget(Impexpelm('Registro Deporte'))

    def goto_tabladeporte(self, *args):
        self.clear_widgets()
        self.current = 'impexpelm'
        self.add_widget(Impexpelm('Tabla Deporte'))

    def goto_inventario(self, *args):
        self.clear_widgets()
        self.current = 'impexpelm'
        self.add_widget(Impexpelm('Inventario'))

    def goto_vblesglobales(self, *args):
        self.clear_widgets()
        self.current = 'impexpelm'
        self.add_widget(Impexpelm('Variables globales'))


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
                message.text = "Hay " + str(incorrectas - 1) + " con \n formato incorrecto o ID repetido"
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


class Impexpelm(MDScreen):
    tabla_seleccionada = StringProperty()

    def __init__(self, tabla_i, **kwargs):
        super(Impexpelm, self).__init__()
        self.tabla_seleccionada = tabla_i
        self.Popup = MessagePopup_import()
        self.full_path = os.getcwd()

    def importar_tabla(self):
        bbdd = self.tabla_seleccionada
        self.name_db = bbdd  # Variable usable a nivel general
        if bbdd == 'Movimientos bancarios':
            bbdd = 'movimientos'
            full_path = os.getcwd() + '/movimientos.db'
            self.clear_widgets()
            self.current = 'import_data'
            self.add_widget(Import_data(full_path, bbdd))
        elif bbdd == 'Registro Deporte':
            bbdd = 'deporte'
            full_path = os.getcwd() + '/deporte.db'
            self.clear_widgets()
            self.current = 'import_data'
            self.add_widget(Import_data(full_path, bbdd))
        elif bbdd == 'Variables globales':
            bbdd = 'globales'

    def exportar_tabla(self):
        bbdd = self.tabla_seleccionada

        if platform == 'android':
            os.chdir('/storage/emulated/0/')

        if bbdd == 'Movimientos bancarios':
            bbdd = 'movimientos'
            con = sqlite3.connect(self.full_path + '/movimientos.db')
            cur = con.cursor()
            data = cur.execute("SELECT * FROM movimientos")
            with open('movimientos.csv', 'w', newline='', encoding='latin') as f:
                writer = csv.writer(f, delimiter=';')
                writer.writerows(data)
            con.commit()
            con.close()
        elif bbdd == 'Registro Deporte':
            bbdd = 'deporte'
            con = sqlite3.connect(self.full_path + '/deporte.db')
            cur = con.cursor()
            data = cur.execute("SELECT * FROM deporte")
            with open('deporte.csv', 'w', newline='', encoding='latin') as f:
                writer = csv.writer(f, delimiter=';')
                writer.writerows(data)
            con.commit()
            con.close()
        elif bbdd == 'Variables globales':
            bbdd = 'globales'
            con = sqlite3.connect(self.full_path + '/globales.db')
            cur = con.cursor()
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

    def eliminar_tabla(self):
        bbdd = self.tabla_seleccionada
        if bbdd == 'Movimientos bancarios':
            con = sqlite3.connect(self.full_path + '/movimientos.db')
            cursor = con.cursor()
            s1 = 'DELETE FROM movimientos'
            cursor.execute(s1)
            con.commit()
            con.close()
        elif bbdd == 'Registro Deporte':
            con = sqlite3.connect(self.full_path + '/deporte.db')
            cursor = con.cursor()
            s1 = 'DELETE FROM deporte'
            cursor.execute(s1)
            con.commit()
            con.close()

        message = self.Popup.ids.message
        self.Popup.open()
        self.Popup.title = "Tabla eliminada"
        message.text = "Se ha eliminado la tabla " + bbdd

    def return_tabla(self):
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


Builder.load_string(
    """
#:import platform kivy.utils.platform
WindowManager_select:
    import_main:
    selectDBWid_md:
    export_data:
    import_data:
    
<DataloaderLabel@AKLabelLoader>
    size_hint_y: None
    height: dp(20)
    theme_text_color: "Primary"
    halign: "left"
    
        
<Import_main>:
    name:"import_main"
    canvas:
        Color:
            rgb: 1,1,1,1
        Rectangle:
            pos: self.pos
            size: self.size
    MDBoxLayout:
        orientation: "vertical"

        MyToolbar:
            id: _toolbar

        ScrollView:
            MDBoxLayout:
                orientation: "vertical"
                    
                MDList:
                    size_hint_y:.9
                    OneLineAvatarIconListItem:
                        text:'Movimientos bancarios'
                        on_release:root.goto_movimientos()
                        IconLeftWidget:
                            icon: "bank"
                    OneLineAvatarIconListItem:
                        text:'Registro Deporte'
                        on_release:root.goto_deporte()
                        IconLeftWidget:
                            icon: "weight-lifter"
                    OneLineAvatarIconListItem:
                        text:'Tablas Ejercicio'
                        on_release:root.goto_tabladeporte()
                        IconLeftWidget:
                            icon: "head-heart-outline"
                    OneLineAvatarIconListItem:
                        text:'Registro Alimentación'
                        on_release:pass
                        IconLeftWidget:
                            icon: "food-fork-drink"
                    OneLineAvatarIconListItem:
                        text:'Registro Compras'
                        on_release:pass
                        IconLeftWidget:
                            icon: "shopping-outline"
                    OneLineAvatarIconListItem:
                        text:'Tablas Alimentos'
                        on_release:pass
                        IconLeftWidget:
                            icon: "table-search"
                    OneLineAvatarIconListItem:
                        text:'Inventario'
                        on_release:root.goto_inventario()
                        IconLeftWidget:
                            icon: "list-status"
                    OneLineAvatarIconListItem:
                        text:'Variables Globales'
                        on_release:root.goto_vblesglobales()
                        IconLeftWidget:
                            icon: "globe-model"
                MDLabel:
                    size_hint_y:.1
                    text:''

<Import_data>:
    name:"import_data"
    id:my_widget
    cols:2
    orientation: 'vertical'
    canvas:
        Color:
            rgb: 1/255, 104/255, 113/255
        Rectangle:
            pos: self.pos
            size: self.size
    MDBoxLayout:
        orientation: "vertical"

        MyToolbar:
            id: _toolbar
            title: "Importar/Exportar"
        FileChooserListView:
            rootpath: '/storage/emulated/0/' if platform == 'android' else '/'
            id:filechooser
            on_selection: my_widget.selectfile(filechooser.selection)
        
        AKFloatingRoundedAppbar:

            AKFloatingRoundedAppbarButtonItem:
                icon: "keyboard-return"
                text: "Atrás"
                on_release: root.return_button()
    
            AKFloatingRoundedAppbarButtonItem:
                icon: "card-plus-outline"
                text: "Importar"
                on_release: root.open_file(filechooser.path, filechooser.selection)

<MessagePopup_import>:
    size_hint: .75,.75
    background: 'assets/texture_popup_blurred.png'
    separator_color: 0/255, 73/255, 80/255
    BoxLayout:
        orientation: 'vertical'
        Label:
            id: message
            size_hint: 1, 0.8
            text: ''
        Button:
            size_hint: 1,0.2
            background_color: 0/255, 128/255, 141/255, .5
            text: 'Regresar'
            on_press: root.dismiss()
            on_press: self.background_color = (14/255, 177/255, 192/255, .5)
      
<ImpExpElm>:
    name:"impexpelm"
    id:impexpelm_id
    orientation: 'vertical'
    canvas:
        Color:
            rgb: 1,1,1
        Rectangle:
            pos: self.pos
            size: self.size

    MDBoxLayout:
        orientation: "vertical"

        MyToolbar:
            id: _toolbar
            title: "Importar/Exportar"
            
        MDLabel:
            halign:'center'
            text: 'Seleccione acción a realizar con la tabla:'
            
        MDLabel:
            halign:'center'
            text: root.tabla_seleccionada
            
        AKFloatingRoundedAppbar:

            AKFloatingRoundedAppbarButtonItem:
                icon: "keyboard-return"
                text: "Atrás"
                on_release: root.return_tabla()
    
            AKFloatingRoundedAppbarButtonItem:
                icon: "database-import-outline"
                text: "Importar"
                on_release: root.importar_tabla()
                
            AKFloatingRoundedAppbarButtonItem:
                icon: "database-export-outline"
                text: "Exportar"
                on_release: root.exportar_tabla()
                
            AKFloatingRoundedAppbarButtonItem:
                icon: "delete"
                text: "Eliminar"
                on_release: root.eliminar_tabla()
"""
)
