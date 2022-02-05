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
from kivymd.uix.card import MDCard
from kivymd.uix.list import OneLineListItem

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
            r0 = ' ID: ' + str(i[0]) + '                       '
            r1 = i[1] + '  '
            r2 = i[2] + ', '
            r3 = str(i[3]) + ' '
            r23 = r2 + r3
            r4 = i[5] + ' '
            r5 = str(i[4]) + ' € '
            r6 = i[6][0:25] + '... '
            if r6 == '... ':
                r6 = ' '
            if i[6][0:25] == i[6]:
                r6 = i[6][0:25] + ' '
            if r23[0:23] != r23:
                r23 = r23[0:23] + '... '
            wid.data_id = str(i[0])
            wid.dataID = r0 + r1  # ID + fecha
            wid.dataCC = r23  # Concepto, categoria
            wid.dataIM = r5  # Importe
            wid.dataET = r4  # Etapa
            wid.dataUB = r6  # Ubicacion

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


class DataBaseWid_deporte(MDScreen):
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

        con = sqlite3.connect(self.ruta_DB_PATH_deporte)
        cursor = con.cursor()
        orden_execute = 'select * from deporte ORDER BY ID DESC LIMIT ' + str(
            self.num_rows)
        cursor.execute(orden_execute)
        for i in cursor:
            wid = DataWid_deporte()
            r0 = 'ID: ' + str(i[0]) + '                 '
            r1 = i[1] + ' '
            r2 = i[2] + ''
            r3 = str(i[3]) + ' h'
            wid.data_id = str(i[0])
            # wid.data = r0 + r1 + r2 + r3
            wid.dataID = r0 + r1
            wid.dataCO = r2
            wid.dataTM = r3
            self.ids.container.add_widget(wid)
        con.close()

    def add_10_more(self):
        self.num_rows = self.num_rows + 10
        self.check_memory()

    def create_new_product(self):
        self.num_rows = 10
        self.clear_widgets()
        self.current = 'insert_deporte'
        self.add_widget(InsertDataWid_deporte())


class Vbles_globalesWid(BoxLayout):
    def __init__(self, **kwargs):
        super(Vbles_globalesWid, self).__init__()
        self.check_memory()
        self.Popup = MessagePopup()

    def check_memory(self):
        path_principal = os.getcwd()
        path_globales = path_principal + '/globales.db'
        con = sqlite3.connect(path_globales)
        cursor = con.cursor()
        s = 'select * from globales where ID=1'
        cursor.execute(s)
        for i in cursor:
            self.ids.Obj_cuenta.text = str(i[1])
            self.ids.Obj_fecha.text = i[2]
            self.ids.Obj_peso.text = str(i[3])
            self.ids.Domiciliaciones.text = i[4]
            self.ids.Ingresos.text = i[5]
            self.ids.Obj_tasa.text = str(i[6])
        con.close()

    def update_data(self):
        path_principal = os.getcwd()
        full_path = path_principal + '/globales.db'
        con = sqlite3.connect(full_path)
        cursor = con.cursor()
        d2 = self.ids.Obj_cuenta.text
        d3 = self.ids.Obj_fecha.text
        d4 = self.ids.Obj_peso.text
        d5 = self.ids.Domiciliaciones.text
        d6 = self.ids.Ingresos.text
        d7 = self.ids.Obj_tasa.text
        a1 = (d2, d3, d4, d5, d6, d7)
        s1 = 'UPDATE globales SET'
        s2 = 'Obj_cuenta=%s,Obj_fecha="%s",Obj_peso=%s,Domiciliaciones="%s", Ingresos="%s",Obj_tasa=%s' % a1
        s3 = 'WHERE ID=1'
        try:
            cursor.execute(s1 + ' ' + s2 + ' ' + s3)
            con.commit()
            con.close()
            self.back_to_dbw()
        except Exception as e:
            message = self.mainwid.Popup.ids.message
            self.Popup.open()
            self.Popup.title = "Data base error"
            if '' in a1:
                message.text = 'Uno o más campos están vacíos'
            else:
                message.text = str(e)
            con.close()

    def back_to_dbw(self):
        self.clear_widgets()
        self.current = 'selectdb'
        self.add_widget(Selectdb())


class DataWid(MDCard):  # Usado en el check_memory para visualizar los registros en cada widget mini
    def __init__(self, **kwargs):
        super(DataWid, self).__init__()
        self.Selectdb = Selectdb

    def update_data(self, data_id):
        self.clear_widgets()
        self.current = 'update_movimientos'
        self.add_widget(UpdateDataWid_movimientos(data_id))


class DataWid_deporte(MDCard):  # Usado en el check_memory para visualizar los registros en cada widget mini
    def __init__(self, **kwargs):
        super(DataWid_deporte, self).__init__()
        self.Selectdb = Selectdb

    def update_data(self, data_id):
        self.clear_widgets()
        self.current = 'update_deporte'
        self.add_widget(UpdateDataWid_deporte(data_id))


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
        self.Popup = MessagePopup()

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
        if d2 == '':
            pass
        else:
            format = "%d/%m/%Y"
            try:
                datetime.strptime(d2, format)
            except:
                message = self.Popup.ids.message
                self.Popup.open()
                self.Popup.title = "Error formato"
                message.text = 'La fecha debe ser formato DD/MM/YYYY \n o estar en blanco'
                return
        d3 = self.ids.ti_Concepto.text
        d4 = self.ids.ti_Categoria.text
        d5 = self.ids.ti_Importe.text.replace(",", ".")
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
            message = self.Popup.ids.message
            self.Popup.open()
            self.Popup.title = "Data base error"
            if '' in a1:
                message.text = 'Uno o más campos están vacíos'
            else:
                message.text = str(e)
            con.close()

    def back_to_dbw(self):
        self.clear_widgets()
        self.current = 'db_movimientos'
        self.add_widget(DataBaseWid_movimientos())


class InsertDataWid_deporte(BoxLayout):
    def __init__(self, **kwargs):
        super(InsertDataWid_deporte, self).__init__()
        today = date.today()
        d1 = today.strftime("%d/%m/%Y")
        self.ids.ti_fechao.text = d1
        self.ruta_APP_PATH = os.getcwd()
        self.ruta_DB_PATH_movimientos = self.ruta_APP_PATH + '/movimientos.db'
        self.ruta_DB_PATH_deporte = self.ruta_APP_PATH + '/deporte.db'
        self.ruta_DB_PATH_vblesglobales = self.ruta_APP_PATH + '/globales.db'
        self.Popup = MessagePopup()

    def insert_data(self):
        con = sqlite3.connect(self.ruta_DB_PATH_deporte)
        cursor = con.cursor()
        cursor.execute('select ID from deporte ORDER BY ID DESC LIMIT 1')
        con.commit()
        #
        d1 = 1
        for i in cursor:
            d1 = i[0] + 1
        con.close()
        con = sqlite3.connect(self.ruta_DB_PATH_deporte)
        cursor = con.cursor()
        d2 = self.ids.ti_fechao.text
        if d2 == '':
            pass
        else:
            format = "%d/%m/%Y"
            try:
                datetime.strptime(d2, format)
            except:
                message = self.Popup.ids.message
                self.Popup.open()
                self.Popup.title = "Error formato"
                message.text = 'La fecha debe ser formato DD/MM/YYYY \n o estar en blanco'
                return

        d3 = self.ids.ti_Concepto.text
        d5 = self.ids.ti_Tiempo.text
        a1 = (d1, d2, d3, d5)
        s1 = 'INSERT INTO deporte (ID,	[Fecha Operación],	Concepto, Tiempo)'
        s2 = 'VALUES(%s,"%s","%s",%s)' % a1
        try:
            cursor.execute(s1 + ' ' + s2)
            con.commit()
            con.close()
            self.back_to_dbw()
        except Exception as e:
            message = self.Popup.ids.message
            self.Popup.open()
            self.Popup.title = "Data base error"
            if '' in a1:
                message.text = 'Uno o más campos están vacíos'
            else:
                message.text = str(e)
            con.close()

    def back_to_dbw(self):
        self.clear_widgets()
        self.current = 'db_deporte'
        self.add_widget(DataBaseWid_deporte())


class UpdateDataWid_movimientos(BoxLayout):
    def __init__(self, data_id, **kwargs):
        super(UpdateDataWid_movimientos, self).__init__()
        self.data_id = data_id
        self.ruta_APP_PATH = os.getcwd()
        self.ruta_DB_PATH_movimientos = self.ruta_APP_PATH + '/movimientos.db'
        self.ruta_DB_PATH_deporte = self.ruta_APP_PATH + '/deporte.db'
        self.ruta_DB_PATH_vblesglobales = self.ruta_APP_PATH + '/globales.db'
        self.check_memory()
        self.WindowManager_select = WindowManager_select
        self.Popup = MessagePopup()

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


class UpdateDataWid_deporte(BoxLayout):
    def __init__(self, data_id, **kwargs):
        super(UpdateDataWid_deporte, self).__init__()
        self.data_id = data_id
        self.ruta_APP_PATH = os.getcwd()
        self.ruta_DB_PATH_movimientos = self.ruta_APP_PATH + '/movimientos.db'
        self.ruta_DB_PATH_deporte = self.ruta_APP_PATH + '/deporte.db'
        self.ruta_DB_PATH_vblesglobales = self.ruta_APP_PATH + '/globales.db'
        self.check_memory()
        self.WindowManager_select = WindowManager_select
        self.Popup = MessagePopup()

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
WindowManager_select:
    db_movimientos:
    db_deporte:
    selectdb:
    insert_movimientos:
    datawid:
    update_movimientos:
    eliminado:
    actualizado:
    
<DataloaderLabel@AKLabelLoader>
    size_hint_y: None
    height: dp(20)
    theme_text_color: "Primary"
    halign: "left"
       
<Selectdb>:
    name:"selectdb"
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
                        text:'Registro deporte'
                        on_release:root.goto_deporte()
                        IconLeftWidget:
                            icon: "weight-lifter"
                    OneLineAvatarIconListItem:
                        text:'Tablas Ejercicio'
                        on_release:pass
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
                        text:'Variables Globales'
                        on_release:root.goto_vblesglobales()
                        IconLeftWidget:
                            icon: "globe-model"
                MDLabel:
                    size_hint_y:.1
                    text:''
                
<DataBaseWid_movimientos>:
    name:"db_movimientos"
    canvas:
        Color:
            rgb: 4/255,150/255,163/255,1
        Rectangle:
            pos: self.pos
            size: self.size
    
    MDBoxLayout:
        orientation: "vertical"

        MyToolbar:
            id: _toolbar
            title: "Movimientos Bancarios"

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
                
        AKFloatingRoundedAppbar:

            AKFloatingRoundedAppbarButtonItem:
                icon: "keyboard-return"
                text: "Atrás"
                on_release: root.goto_main()
    
            AKFloatingRoundedAppbarButtonItem:
                icon: "card-plus-outline"
                text: "Añadir 10"
                on_release: root.add_10_more()
                
            AKFloatingRoundedAppbarButtonItem:
                icon: "plus-circle-outline"
                text: "Añadir"
                on_release: root.create_new_product()
                
<DataBaseWid_deporte>:
    name:"db_deporte"
    canvas:
        Color:
            rgb: 4/255,150/255,163/255,1
        Rectangle:
            pos: self.pos
            size: self.size
    MDBoxLayout:
        orientation: "vertical"

        MyToolbar:
            id: _toolbar
            title: "Registro Deporte"
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
                
        AKFloatingRoundedAppbar:

            AKFloatingRoundedAppbarButtonItem:
                icon: "keyboard-return"
                text: "Atrás"
                on_release: root.goto_main()
    
            AKFloatingRoundedAppbarButtonItem:
                icon: "card-plus-outline"
                text: "Añadir 10"
                on_release: root.add_10_more()
                
            AKFloatingRoundedAppbarButtonItem:
                icon: "plus-circle-outline"
                text: "Añadir"
                on_release: root.create_new_product()

<DataWid>:
    padding: "8dp"
    name:"datawid"
    size_hint: .9, .2
    #size: dp(320), dp(140)
    radius: [dp(10),]
    pos_hint: {"center_x": .5, "center_y": .5}
    dataID: ""
    dataCC: ""
    dataIM: ""
    dataET: ""
    dataUB: ""
    data_id: ''
    on_release: root.update_data(root.data_id)

    MDBoxLayout:
        MDBoxLayout:
            orientation: "vertical"
            size_hint_x: .7
            
            MDLabel:
                text: ""
            DataloaderLabel:
                text:  root.dataID
                font_size: root.width * .04
            MDSeparator:
            
            DataloaderLabel:
                text:  root.dataCC
                
            MDSeparator:
            
            DataloaderLabel:
                text:  root.dataET
            MDSeparator:
            
            DataloaderLabel:
                text:  root.dataUB
            MDLabel:
                text: ""
            
        MDBoxLayout:
            size_hint_x: .3
            orientation:"vertical"
            MDLabel:
                text: ""
            DataloaderLabel:
                text:  root.dataIM
                halign: "center"
                valign: "center"
            MDLabel:
                text: ""
                
<DataWid_deporte>:
    padding: "8dp"
    name:"datawid"
    size_hint: .9, .2
    #size: dp(320), dp(140)
    radius: [dp(10),]
    pos_hint: {"center_x": .5, "center_y": .5}
    dataID: ""
    dataCO: ""
    dataTM: ""
    data_id: ''
    on_release: root.update_data(root.data_id)

    MDBoxLayout:
        MDBoxLayout:
            orientation: "vertical"
            size_hint_x: .7
            MDLabel:
                text: ""
            DataloaderLabel:
                text:  root.dataID
                font_size: root.width * .04
            MDSeparator:
            
            DataloaderLabel:
                text:  root.dataCO
            MDLabel:
                text: ""
                
        MDBoxLayout:
            size_hint_x: .3
            orientation:"vertical"
            MDLabel:
                text: ""
            DataloaderLabel:
                text:  root.dataTM
                halign: "center"
                valign: "center"
            MDLabel:
                text: ""

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

<InsertDataWid_deporte>:
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
    Label: # ---------- Concepto
        text: ' Concepto:'
    TextInput:
        id: ti_Concepto
        multiline: False
        hint_text: 'Concepto:'
    Label: # ---------- Importe
        text: ' Tiempo:'
    TextInput:
        id: ti_Tiempo
        multiline: False
        hint_text: 'Tiempo'
    BoxLayout:
        size_hint_y: 5
    BoxLayout: # ---------- Crear Salir
        Button:
            text: 'Crear'
            on_press: root.insert_data()
        Button:
            text: 'Salir'
            on_press: root.back_to_dbw()
            
<MessagePopup>:
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
            
<UpdateDataWid_movimientos>:
    name: "update_movimientos"
    orientation: 'vertical'
    data_id: ''
    canvas:
        Color:
            rgb: .254,.556,.627
        Rectangle:
            pos: self.pos
            size: self.size
    BoxLayout:
        TextInput:
            id: ti_fechao
            multiline: False
            hint_text: 'Fecha Operación'
        TextInput:
            id: ti_Concepto
            multiline: False
            hint_text: 'Concepto:'
        TextInput:
            id: ti_Categoria
            multiline: False
            hint_text: 'Categoría'
    BoxLayout:
        TextInput:
            id: ti_Importe
            multiline: False
            hint_text: 'Importe'
        TextInput:
            id: ti_Etapa
            multiline: False
            hint_text: 'Etapa'
        TextInput:
            id: ti_Ubi
            multiline: False
            hint_text: 'Ubicación'
    BoxLayout:
        Button:
            text: 'Actualizar'
            on_press: root.update_data()
        Button:
            text: 'Eliminar'
            on_press: root.delete_data()
            
<UpdateDataWid_deporte>:
    name: "update_deporte"
    orientation: 'vertical'
    data_id: ''
    canvas:
        Color:
            rgb: .254,.556,.627
        Rectangle:
            pos: self.pos
            size: self.size
    BoxLayout:
        TextInput:
            id: ti_fechao
            multiline: False
            hint_text: 'Fecha Operación'
        TextInput:
            id: ti_Concepto
            multiline: False
            hint_text: 'Concepto:'
    BoxLayout:
        TextInput:
            id: ti_Tiempo
            multiline: False
            hint_text: 'Tiempo'
    BoxLayout:
        Button:
            text: 'Actualizar'
            on_press: root.update_data()
        Button:
            text: 'Eliminar'
            on_press: root.delete_data()
            
<Eliminado>:
    name: "eliminado"
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: 'Registro eliminado'
            
<Actualizado>:
    name: "actualizado"
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: 'Registro actualizado'
            
<Vbles_globalesWid>:
    name:"db_vblesglob"
    orientation: 'vertical'
    data_id: ''
    canvas:
        Color:
            rgb: 4/255,150/255,163/255,1
        Rectangle:
            pos: self.pos
            size: self.size
    MDBoxLayout:
        orientation: "vertical"

        MyToolbar:
            id: _toolbar
            title: "Variables Globales"
            
        Label:
            text: ' Objetivo cuenta (€):'
        TextInput:
            id: Obj_cuenta
            multiline: False
            hint_text: '€'
        Label:
            text: ' Fecha límite para conseguirlo:'
        TextInput:
            id: Obj_fecha
            multiline: False
            hint_text: '01/01/2022'
        Label: # ---------- Domiciliaciones
            text: ' Domiciliaciones (separados por coma):'
        TextInput:
            id: Domiciliaciones
            multiline: False
            hint_text: 'ABONO, SPOTIFY,...'
        Label: # ---------- Ingresos
            text: ' Ingresos (separados por coma):'
        TextInput:
            id: Ingresos
            multiline: False
            hint_text: 'SALARIO, BECA,...'
        Label: # ---------- Importe
            text: ' Objetivo tasa de ahorro (%):'
        TextInput:
            id: Obj_tasa
            multiline: False
            hint_text: '%'
        Label: # ---------- 
            text: ' En desarrollo para futuros módulos:'
        Label: # ---------- Concepto
            text: ' Objetivo peso (Kg):'
        TextInput:
            id: Obj_peso
            multiline: False
            hint_text: ' Kg'
        BoxLayout:
            size_hint_y: 4
        BoxLayout:
            Button:
                text: 'Salir'
                on_press: root.back_to_dbw()
            Button:
                text: 'Actualizar'
                on_press: root.update_data()

"""
)
