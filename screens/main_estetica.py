from kivy.config import Config

Config.set("graphics", "width", "340")
Config.set("graphics", "hight", "640")
import kivy
import os
import sqlite3
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.screenmanager import FadeTransition
from kivy.properties import StringProperty
from os.path import join
import csv
from kivy.utils import platform
from kivy_garden.graph import Graph, LinePlot, HBar

if platform == 'android':
    from android.permissions import request_permissions, Permission

    request_permissions([Permission.WRITE_EXTERNAL_STORAGE])

if platform != 'android':
    os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'

from datetime import date
from datetime import datetime

today = date.today()
d1 = today.strftime("%d/%m/%Y")


def connect_to_database(path, name):
    # Evitar que no escriba correctamente los nombres de las BBDD por ir con PATH actualizado con la BBDD anterior
    # sep = '/'
    # stripped = path.split(sep, 1)[0]
    # full_path = stripped + '/' + name + '.db'
    full_path = path
    try:
        con = sqlite3.connect(full_path)
        cursor = con.cursor()
        if name == 'movimientos':
            create_table_movimientos(cursor)
        elif name == 'deporte':
            create_table_deporte(cursor)
        con.commit()
        con.close()
    except Exception as e:
        print(e)
    return full_path


def connect_to_DB_vbles_globales(path):
    full_path = path + '/globales.db'
    try:
        con = sqlite3.connect(full_path)
        cursor = con.cursor()
        create_table_vbles_globales(cursor)
        con.commit()
        con.close()
    except Exception as e:
        print(e)
    return full_path


def create_table_movimientos(cursor):
    cursor.execute(
        '''
        CREATE TABLE movimientos(
        ID        INT   PRIMARY KEY NOT NULL,
        [Fecha Operación]    TEXT               ,
        Concepto     TEXT               NOT NULL,
        Categoría   TEXT                NOT NULL,
        Importe     FLOAT              NOT NULL,
        Etapa   TEXT                NOT NULL,
        Ubicación TEXT
        )'''
    )


def create_table_deporte(cursor):
    cursor.execute(
        '''
        CREATE TABLE deporte(
        ID        INT   PRIMARY KEY NOT NULL,
        [Fecha Operación]    TEXT               ,
        Concepto     TEXT               NOT NULL,
        Tiempo     FLOAT              NOT NULL
        )'''
    )


def create_table_vbles_globales(cursor):
    cursor.execute(
        '''
        CREATE TABLE globales(
        ID        INT   PRIMARY KEY NOT NULL,
        Obj_cuenta           FLOAT,
        Obj_fecha           TEXT,
        Obj_peso             FLOAT,
        Domiciliaciones      TEXT,
        Obj_tasa FLOAT
        )''')

    cursor.execute(
        '''INSERT INTO globales (ID, Obj_cuenta, Obj_fecha, Obj_peso, Domiciliaciones, Obj_tasa) VALUES (1,25000,'01/09/2022',60,'ABONO',80)'''
    )


class MessagePopup(Popup):
    pass


class MainWid(ScreenManager):
    def __init__(self, **kwargs):
        super(MainWid, self).__init__()
        self.APP_PATH = os.getcwd()  # aqui para cambiar donde se guarda la base de datos
        self.DB_PATH_movimientos = self.APP_PATH + '/movimientos.db'
        self.DB_PATH_deporte = self.APP_PATH + '/deporte.db'
        self.DB_PATH = ''
        self.name_db = ''
        self.num_rows = 10
        # tienes que definirlo aqui como a si mismo, no me preguntes por qué.
        self.StartWid = StartWid(self)
        self.DataBaseWid = DataBaseWid(self)
        self.DataBaseWid_deporte = DataBaseWid_deporte(self)
        self.SelectDBWid = SelectDBWid(self)
        self.SelectDBWid_fb = SelectDBWid_fb(self)
        self.SelectDBWid_md = SelectDBWid_md(self)
        self.InsertDataWid = BoxLayout()
        self.InsertDataWid_deporte = BoxLayout()
        self.UpdateDataWid = BoxLayout()
        self.UpdateDataWid_deporte = BoxLayout()
        self.Popup = MessagePopup()
        self.FileBrowser = BoxLayout()
        self.Moddata = Moddata(self)
        # self.Vbles_globalesWid = BoxLayout()
        self.Vbles_globalesWid = Vbles_globalesWid(self)
        self.DataAnalysisWid = DataAnalysisWid(self)
        self.KPIWid = BoxLayout()

        wid = Screen(name='start')
        wid.add_widget(self.StartWid)
        self.add_widget(wid)
        wid = Screen(name='selectdb')
        wid.add_widget(self.SelectDBWid)
        self.add_widget(wid)
        wid = Screen(name='database')
        wid.add_widget(self.DataBaseWid)
        self.add_widget(wid)
        wid = Screen(name='database_deporte')
        wid.add_widget(self.DataBaseWid_deporte)
        self.add_widget(wid)
        wid = Screen(name='insertdata')
        wid.add_widget(self.InsertDataWid)
        self.add_widget(wid)
        wid = Screen(name='insertdata_deporte')
        wid.add_widget(self.InsertDataWid_deporte)
        self.add_widget(wid)
        wid = Screen(name='updatedata')
        wid.add_widget(self.UpdateDataWid)
        self.add_widget(wid)
        wid = Screen(name='updatedata_deporte')
        wid.add_widget(self.UpdateDataWid_deporte)
        self.add_widget(wid)
        wid = Screen(name='selectdb_fb')
        wid.add_widget(self.SelectDBWid_fb)
        self.add_widget(wid)
        wid = Screen(name='selectdb_md')
        wid.add_widget(self.SelectDBWid_md)
        self.add_widget(wid)
        wid = Screen(name='filebrowser')
        wid.add_widget(self.FileBrowser)
        self.add_widget(wid)
        wid = Screen(name='moddata')
        wid.add_widget(self.Moddata)
        self.add_widget(wid)
        wid = Screen(name='vbles_globales')
        wid.add_widget(self.Vbles_globalesWid)
        self.add_widget(wid)
        wid = Screen(name='dataanalysis')
        wid.add_widget(self.DataAnalysisWid)
        self.add_widget(wid)
        wid = Screen(name='KPI')
        wid.add_widget(self.KPIWid)
        self.add_widget(wid)

        self.goto_start()
        #

    # FUNCIONES PARA SALTAR A LAS PANTALLAS:

    def goto_start(self):
        self.current = 'start'

    def goto_selectdb(self):
        self.current = 'selectdb'

    def goto_selectdb_fb(self):
        self.current = 'selectdb_fb'

    def goto_selectdb_md(self):
        self.current = 'selectdb_md'

    def goto_database(self):
        if self.name_db == 'movimientos':
            self.DataBaseWid.check_memory()
            self.current = 'database'
        if self.name_db == 'deporte':
            self.DataBaseWid_deporte.check_memory()
            self.current = 'database_deporte'

    def goto_insertdata(self):
        if self.name_db == 'movimientos':
            self.InsertDataWid.clear_widgets()
            wid = InsertDataWid(self)
            self.InsertDataWid.add_widget(wid)
            self.current = 'insertdata'
        elif self.name_db == 'deporte':
            self.InsertDataWid_deporte.clear_widgets()
            wid = InsertDataWid_deporte(self)
            self.InsertDataWid_deporte.add_widget(wid)
            self.current = 'insertdata_deporte'

    def goto_updatedata(self, data_id):
        if self.name_db == 'movimientos':
            self.UpdateDataWid.clear_widgets()
            wid = UpdateDataWid(self, data_id)
            self.UpdateDataWid.add_widget(wid)
            self.current = 'updatedata'
        elif self.name_db == 'deporte':
            self.UpdateDataWid_deporte.clear_widgets()
            wid = UpdateDataWid_deporte(self, data_id)
            self.UpdateDataWid_deporte.add_widget(wid)
            self.current = 'updatedata_deporte'

    def goto_filebrowser(self):
        self.FileBrowser.clear_widgets()
        wid = FileBrowser(self)
        self.FileBrowser.add_widget(wid)
        self.current = 'filebrowser'

    def goto_moddata(self):
        self.Moddata.check_memory()
        self.current = 'moddata'

    def goto_vbles_globales(self):
        self.current = 'vbles_globales'

    def goto_data_analysis(self):
        self.current = 'dataanalysis'

    def goto_KPI(self):
        self.KPIWid.clear_widgets()
        wid = KPIWid(self)
        self.KPIWid.add_widget(wid)
        self.current = 'KPI'


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


class SelectDBWid(BoxLayout):
    def __init__(self, mainwid, **kwargs):
        super(SelectDBWid, self).__init__()
        self.mainwid = mainwid

    def select_db(self):
        bbdd = self.ids.click_label.text
        self.mainwid.name_db = bbdd  # Variable usable a nivel general
        if bbdd == 'movimientos':
            self.mainwid.DB_PATH = self.mainwid.DB_PATH_movimientos
            self.mainwid.DB_PATH_movimientos = connect_to_database(self.mainwid.DB_PATH_movimientos, bbdd)
        elif bbdd == 'deporte':
            self.mainwid.DB_PATH = self.mainwid.DB_PATH_deporte
            self.mainwid.DB_PATH_deporte = connect_to_database(self.mainwid.DB_PATH_deporte, bbdd)
        self.mainwid.goto_database()

    def spinner_clicked(self, value):
        self.ids.click_label.text = value


class SelectDBWid_fb(BoxLayout):
    def __init__(self, mainwid, **kwargs):
        super(SelectDBWid_fb, self).__init__()
        self.mainwid = mainwid

    def select_db(self):
        bbdd = self.ids.click_label.text
        self.mainwid.name_db = bbdd  # Variable usable a nivel general
        if bbdd == 'movimientos':
            self.mainwid.DB_PATH = self.mainwid.DB_PATH_movimientos
            self.mainwid.DB_PATH_movimientos = connect_to_database(self.mainwid.DB_PATH_movimientos, bbdd)
        elif bbdd == 'deporte':
            self.mainwid.DB_PATH = self.mainwid.DB_PATH_deporte
            self.mainwid.DB_PATH_deporte = connect_to_database(self.mainwid.DB_PATH_deporte, bbdd)
        self.mainwid.goto_filebrowser()

    def spinner_clicked(self, value):
        self.ids.click_label.text = value


class SelectDBWid_md(BoxLayout):
    def __init__(self, mainwid, **kwargs):
        super(SelectDBWid_md, self).__init__()
        self.mainwid = mainwid

    def select_db(self):
        bbdd = self.ids.click_label.text
        self.mainwid.name_db = bbdd  # Variable usable a nivel general
        if bbdd == 'movimientos':
            self.mainwid.DB_PATH = self.mainwid.DB_PATH_movimientos
            self.mainwid.DB_PATH_movimientos = connect_to_database(self.mainwid.DB_PATH_movimientos, bbdd)
        elif bbdd == 'deporte':
            self.mainwid.DB_PATH = self.mainwid.DB_PATH_deporte
            self.mainwid.DB_PATH_deporte = connect_to_database(self.mainwid.DB_PATH_deporte, bbdd)
        self.mainwid.goto_moddata()

    def spinner_clicked(self, value):
        self.ids.click_label.text = value


class DataBaseWid(BoxLayout):
    def __init__(self, mainwid, **kwargs):
        super(DataBaseWid, self).__init__()
        self.mainwid = mainwid

    def check_memory(self):
        self.ids.container.clear_widgets()

        con = sqlite3.connect(self.mainwid.DB_PATH)
        cursor = con.cursor()
        orden_execute = 'select * from ' + self.mainwid.name_db + ' ORDER BY ID DESC LIMIT ' + str(
            self.mainwid.num_rows)
        cursor.execute(orden_execute)
        if self.mainwid.name_db == 'movimientos':
            for i in cursor:
                wid = DataWid(self.mainwid)
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
        elif self.mainwid.name_db == 'deporte':
            for i in cursor:
                wid = DataWid(self.mainwid)
                r0 = 'ID: ' + str(i[0]) + ' '
                r1 = i[1] + ' \n'
                r2 = i[2] + '\n'
                r3 = str(i[3]) + ' '
                wid.data_id = str(i[0])
                wid.data = r0 + r1 + r2 + r3
                self.ids.container.add_widget(wid)
        con.close()

    def create_new_product(self):
        self.mainwid.num_rows = 10
        self.mainwid.goto_insertdata()

    def back_to_dbw(self):
        self.mainwid.num_rows = 10
        self.mainwid.goto_database()

    def return_button(self):
        self.mainwid.num_rows = 10
        self.mainwid.goto_start()

    def add_10_more(self):
        self.mainwid.num_rows = self.mainwid.num_rows + 10
        self.mainwid.goto_database()


class DataBaseWid_deporte(BoxLayout):
    def __init__(self, mainwid, **kwargs):
        super(DataBaseWid_deporte, self).__init__()
        self.mainwid = mainwid

    def check_memory(self):
        self.ids.container.clear_widgets()

        con = sqlite3.connect(self.mainwid.DB_PATH)
        cursor = con.cursor()
        orden_execute = 'select * from ' + self.mainwid.name_db + ' ORDER BY ID DESC LIMIT ' + str(
            self.mainwid.num_rows)
        cursor.execute(orden_execute)
        if self.mainwid.name_db == 'movimientos':
            for i in cursor:
                wid = DataWid(self.mainwid)
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
        elif self.mainwid.name_db == 'deporte':
            for i in cursor:
                wid = DataWid(self.mainwid)
                r0 = 'ID: ' + str(i[0]) + ' '
                r1 = i[1] + ' \n'
                r2 = i[2] + '\n'
                r3 = str(i[3]) + ' '
                wid.data_id = str(i[0])
                wid.data = r0 + r1 + r2 + r3
                self.ids.container.add_widget(wid)
        con.close()

    def create_new_product(self):
        self.mainwid.num_rows = 10
        self.mainwid.goto_insertdata()

    def back_to_dbw(self):
        self.mainwid.num_rows = 10
        self.mainwid.goto_database()

    def return_button(self):
        self.mainwid.num_rows = 10
        self.mainwid.goto_start()

    def add_10_more(self):
        self.mainwid.num_rows = self.mainwid.num_rows + 10
        self.mainwid.goto_database()


class UpdateDataWid(BoxLayout):
    def __init__(self, mainwid, data_id, **kwargs):
        super(UpdateDataWid, self).__init__()
        self.mainwid = mainwid
        self.data_id = data_id
        # self.data_vis = data_vis
        self.check_memory()

    def check_memory(self):
        con = sqlite3.connect(self.mainwid.DB_PATH)
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


class UpdateDataWid_deporte(BoxLayout):
    def __init__(self, mainwid, data_id, **kwargs):
        super(UpdateDataWid_deporte, self).__init__()
        self.mainwid = mainwid
        self.data_id = data_id
        # self.data_vis = data_vis
        self.check_memory()

    def check_memory(self):
        con = sqlite3.connect(self.mainwid.DB_PATH)
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
        con = sqlite3.connect(self.mainwid.DB_PATH)
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
        s = 'delete from deporte where ID=' + self.data_id
        cursor.execute(s)
        con.commit()
        con.close()
        self.mainwid.goto_database()

    def back_to_dbw(self):
        self.mainwid.goto_database()


class InsertDataWid(BoxLayout):
    def __init__(self, mainwid, **kwargs):
        super(InsertDataWid, self).__init__()
        self.mainwid = mainwid
        self.ids.ti_fechao.text = d1

    def insert_data(self):
        con = sqlite3.connect(self.mainwid.DB_PATH)
        cursor = con.cursor()
        cursor.execute('select ID from movimientos ORDER BY ID DESC LIMIT 1')
        con.commit()
        #
        d1 = 1
        for i in cursor:
            d1 = i[0] + 1
        con.close()
        con = sqlite3.connect(self.mainwid.DB_PATH)
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

    def back_to_dbw(self):
        self.mainwid.goto_database()


class InsertDataWid_deporte(BoxLayout):
    def __init__(self, mainwid, **kwargs):
        super(InsertDataWid_deporte, self).__init__()
        self.mainwid = mainwid
        self.ids.ti_fechao.text = d1

    def insert_data(self):
        con = sqlite3.connect(self.mainwid.DB_PATH)
        cursor = con.cursor()
        cursor.execute('select ID from deporte ORDER BY ID DESC LIMIT 1')
        con.commit()
        #
        d1 = 1
        for i in cursor:
            d1 = i[0] + 1
        con.close()
        con = sqlite3.connect(self.mainwid.DB_PATH)
        cursor = con.cursor()
        d2 = self.ids.ti_fechao.text
        d3 = self.ids.ti_Concepto.text
        d5 = self.ids.ti_Tiempo.text
        a1 = (d1, d2, d3, d5)
        s1 = 'INSERT INTO deporte (ID,	[Fecha Operación],	Concepto, Tiempo)'
        s2 = 'VALUES(%s,"%s","%s",%s)' % a1
        try:
            cursor.execute(s1 + ' ' + s2)
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

    def back_to_dbw(self):
        self.mainwid.goto_database()


class DataWid(BoxLayout):  # Usado en el check_memory para visualizar los registros en cada widget mini
    def __init__(self, mainwid, **kwargs):
        super(DataWid, self).__init__()
        self.mainwid = mainwid

    def update_data(self, data_id):
        self.mainwid.goto_updatedata(data_id)


class FileBrowser(BoxLayout):
    def __init__(self, mainwid, **kwargs):
        super(FileBrowser, self).__init__()
        self.mainwid = mainwid
        self.file_name = ''

    def open_file(self, path, filename):
        if ".csv" in filename[0]:
            with open(os.path.join(path, filename[0])) as f:
                # print (f.read())
                row = f.read()
                row2 = row.split('\n')
                i = 0
                incorrectas = 0
                for each_row in row2:
                    # message = self.mainwid.Popup.ids.message
                    # self.mainwid.Popup.open()
                    # self.mainwid.Popup.title = "INICIO"
                    # message.text = "INICIO " + str(i)
                    try:
                        string_list = each_row.split(";")
                        string_list[4] = string_list[4].replace(",", ".")
                        string_list = tuple(string_list)
                        # Comas a puntos
                        # self.df.loc[i] = string_list
                        if self.mainwid.name_db == 'movimientos':
                            con = sqlite3.connect(self.mainwid.DB_PATH_movimientos)
                            cursor = con.cursor()
                            s1 = 'INSERT INTO movimientos(ID, [Fecha Operación], Concepto, Categoría, Importe, Etapa, Ubicación)'
                            s2 = 'VALUES(%s,"%s","%s","%s",%s,"%s","%s")' % string_list
                            # comando = s1 + ' ' + s2
                            cursor.execute(s1 + ' ' + s2)
                        elif self.mainwid.name_db == 'deporte':
                            con = sqlite3.connect(self.mainwid.DB_PATH_deporte)
                            cursor = con.cursor()
                            s1 = 'INSERT INTO deporte(ID,	[Fecha Operación],	Concepto, Tiempo)'
                            s2 = 'VALUES(%s,"%s","%s",%s)' % string_list
                            # comando = s1 + ' ' + s2
                            cursor.execute(s1 + ' ' + s2)
                        con.commit()
                        con.close()
                        # message = self.mainwid.Popup.ids.message
                        # self.mainwid.Popup.open()
                        # self.mainwid.Popup.title = "FIN"
                        # message.text = "FIN " + str(i)
                    except:
                        incorrectas = incorrectas + 1
                    i = i + 1
                # print("Hay", incorrectas, "líneas incorrectas")
                message = self.mainwid.Popup.ids.message
                self.mainwid.Popup.open()
                self.mainwid.Popup.title = "Líneas generadas"
                message.text = "Hay " + str(incorrectas) + " con formato incorrecto o ID repetido"
        else:
            message = self.mainwid.Popup.ids.message
            self.mainwid.Popup.open()
            self.mainwid.Popup.title = "Error de formato"
            message.text = 'El fichero no es un csv'

    def selectfile(self, filename):
        self.file_name = filename

    def return_button(self):
        self.mainwid.goto_start()


class Moddata(BoxLayout):
    def __init__(self, mainwid, **kwargs):
        super(Moddata, self).__init__()
        self.mainwid = mainwid

    def check_memory(self):
        self.ids.container.clear_widgets()

        con = sqlite3.connect(self.mainwid.DB_PATH)
        cursor = con.cursor()
        orden_execute = 'select * from ' + self.mainwid.name_db + ' ORDER BY ID DESC LIMIT ' + str(
            self.mainwid.num_rows)
        cursor.execute(orden_execute)
        if self.mainwid.name_db == 'movimientos':
            for i in cursor:
                wid = DataWid(self.mainwid)
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
        elif self.mainwid.name_db == 'deporte':
            for i in cursor:
                wid = DataWid(self.mainwid)
                r0 = 'ID: ' + str(i[0]) + ' '
                r1 = i[1] + ' \n'
                r2 = i[2] + '\n'
                r3 = str(i[3]) + ' '
                wid.data_id = str(i[0])
                wid.data = r0 + r1 + r2 + r3
                self.ids.container.add_widget(wid)
        con.close()

    def return_button(self):
        self.mainwid.goto_start()

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


class Vbles_globalesWid(BoxLayout):
    def __init__(self, mainwid, **kwargs):
        super(Vbles_globalesWid, self).__init__()
        self.mainwid = mainwid
        self.check_memory()

    def check_memory(self):
        path_globales = connect_to_DB_vbles_globales(self.mainwid.APP_PATH)
        con = sqlite3.connect(path_globales)
        cursor = con.cursor()
        s = 'select * from globales where ID=1'
        cursor.execute(s)
        for i in cursor:
            self.ids.Obj_cuenta.text = str(i[1])
            self.ids.Obj_fecha.text = i[2]
            self.ids.Obj_peso.text = str(i[3])
            self.ids.Domiciliaciones.text = i[4]
            self.ids.Obj_tasa.text = str(i[5])
        con.close()

    def update_data(self):
        full_path = self.mainwid.APP_PATH + '/globales.db'
        con = sqlite3.connect(full_path)
        cursor = con.cursor()
        d2 = self.ids.Obj_cuenta.text
        d3 = self.ids.Obj_fecha.text
        d4 = self.ids.Obj_peso.text
        d5 = self.ids.Domiciliaciones.text
        d6 = self.ids.Obj_tasa.text
        a1 = (d2, d3, d4, d5, d6)
        s1 = 'UPDATE globales SET'
        s2 = 'Obj_cuenta=%s,Obj_fecha="%s",Obj_peso=%s,Domiciliaciones="%s",Obj_tasa=%s' % a1
        s3 = 'WHERE ID=1'
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

    def back_to_dbw(self):
        self.mainwid.goto_start()


class DataAnalysisWid(BoxLayout):

    def __init__(self, mainwid, **kwargs):
        super(DataAnalysisWid, self).__init__()
        self.mainwid = mainwid

    def go_back(self):
        self.mainwid.goto_start()

    def empty_button(self):
        pass

    def KPIs(self):
        # Ir a pantalla a mostrar resultados
        self.mainwid.goto_KPI()

    def linea_temporal(self):
        pass

    def donut_etapa(self):
        pass

    def tabla_ingresos_gastos(self):
        pass

    def tabla_salario_mensual(self):
        pass

    def tabla_semanal(self):
        pass

    def evolucion_tasa(self):
        pass


class KPIWid(BoxLayout):

    def __init__(self, mainwid, **kwargs):
        super(KPIWid, self).__init__()
        self.mainwid = mainwid

        # Calculamos el valor de la cuenta, el ahorro por mes, las domiciliaciones, y la barra de ahorro.
        con = sqlite3.connect(self.mainwid.DB_PATH_movimientos)
        cursor = con.cursor()
        orden_execute = 'select * from movimientos'
        cursor.execute(orden_execute)
        saldo = 0
        ingresos = 0
        gastos = 0
        fecha_min = '01/01/2099'
        fecha_max = '01/01/1999'
        for i in cursor:
            saldo = saldo + i[4]
            if i[4] > 0:
                ingresos = ingresos + i[4]
            else:
                gastos = gastos + i[4]
            # Conseguir las fechas min y max del periodo
            try:
                if datetime.strptime(i[1], '%d/%m/%Y') > datetime.strptime(fecha_max, '%d/%m/%Y'):
                    fecha_max = i[1]

                if datetime.strptime(i[1], '%d/%m/%Y') < datetime.strptime(fecha_min, '%d/%m/%Y'):
                    fecha_min = i[1]
            except:
                pass
        con.commit()
        con.close()

        # Obtenemos variables globales que vamos a usar:
        path_globales = self.mainwid.APP_PATH + '/globales.db'
        con = sqlite3.connect(path_globales)
        cursor = con.cursor()
        orden_execute = 'select Obj_cuenta, Obj_fecha, Domiciliaciones, Obj_tasa from globales where ID = 1'
        cursor.execute(orden_execute)
        for i in cursor:
            obj_cuenta = i[0]
            obj_fecha = i[1]
            domiciliaciones = i[2]
            domiciliaciones_list = domiciliaciones.replace(' ', '').split(',')
            obj_tasa = i[3]
        con.commit()
        con.close()

        # Cálculos:
        # Ahorro objetivo
        try:
            ahorro_obj_mensual = (obj_cuenta - saldo) * 30 / (
                    datetime.strptime(obj_fecha, '%d/%m/%Y') - datetime.now()).days
        except ZeroDivisionError:
            ahorro_obj_mensual = 0
        # Tasa de ahorro
        try:
            tasa_ahorro = (ingresos + gastos) / ingresos
        except ZeroDivisionError:
            tasa_ahorro = -1
        # Ahorro real
        try:
            ahorro_real_mes = saldo * 30 / (
                    datetime.strptime(fecha_max, '%d/%m/%Y') - datetime.strptime(fecha_min, '%d/%m/%Y')).days
        except ZeroDivisionError:
            ahorro_real_mes = 0

        # Asignaciones
        self.ids.saldo.text = str(round(saldo, 2)) + ' €'
        self.ids.ahorro_obj_mensual.text = str(round(ahorro_obj_mensual, 2)) + ' €'
        self.ids.tasa_ahorro.text = str(round(tasa_ahorro * 100, 2)) + ' %'
        self.ids.ahorro_real_mes.text = str(round(ahorro_real_mes, 2)) + ' €'

    def return_button(self):
        self.mainwid.goto_start()


class MainApp(App):
    def build(self):
        return MainWid()


if __name__ == '__main__':
    MainApp().run()
