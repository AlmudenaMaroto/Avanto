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
from tools.swipe_widget import SwipeBehavior
# Para la tabla de ejercicios:
from tools.MDDataTable_avanto import MDDataTable
from kivy.metrics import dp


class AnimatedBox(MDList, AKAddWidgetAnimationBehavior):
    pass


class MessagePopup(Popup):
    pass


class Eliminado(MDScreen):
    pass


class Eliminado_inventario(MDScreen):
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

    def goto_tabladeporte(self, *args):
        self.clear_widgets()
        self.current = 'db_tabladeporte'
        self.add_widget(DB_tabladeporte())

    def goto_inventario(self, *args):
        self.clear_widgets()
        self.current = 'db_inventario'
        self.add_widget(DataBaseWid_inventario())

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


class DB_tabladeporte(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.Selectdb = Selectdb
        self.num_rows = 10
        self.ruta_APP_PATH = os.getcwd()
        self.ruta_DB_PATH_tabladeporte = self.ruta_APP_PATH + '/tabladeporte.db'
        self.tabla_ejercicio = ''
        self.objeto_seleccionado = []
        self.Popup = MessagePopup()
        self.check_memory()

    def goto_main(self):
        self.clear_widgets()
        self.current = 'selectdb'
        self.add_widget(Selectdb())

    def check_memory(self):
        datos_filas = []
        fila_i = []
        # Cargamos datos
        con = sqlite3.connect(self.ruta_DB_PATH_tabladeporte)
        cursor = con.cursor()
        orden_execute = 'select * from tabladeporte ORDER BY ID ASC'
        cursor.execute(orden_execute)
        for i in cursor:
            fila_i = [i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7]]
            datos_filas.append(tuple(fila_i))
        con.close()
        # datos_filas = [('Tenis', 10), ('Tenis', 10)]
        self.ids.container.clear_widgets()

        self.tabla_ejercicio = MDDataTable(pos_hint={'center_x': 0.5, 'center_y': 0.5},
                                           size_hint=(0.9, 0.6),
                                           check=True,
                                           rows_num=7,
                                           use_pagination=False,
                                           column_data=[
                                               ("ID", dp(20)),
                                               ("Ejercicio", dp(30)),
                                               ("kcal/h", dp(12)),
                                               ("Cardio", dp(12)),
                                               ("Brazo", dp(12)),
                                               ("Pecho", dp(12)),
                                               ("Espalda", dp(13)),
                                               ("Pierna", dp(12)),
                                           ],
                                           row_data=datos_filas,
                                           )
        # self.tabla_ejercicio.bind(on_row_press=self.on_row_press)
        self.tabla_ejercicio.bind(on_check_press=self.on_check_press)

        self.ids.container.add_widget(self.tabla_ejercicio)

    def add_10_more(self):
        # self.num_rows = self.num_rows + 10
        # self.check_memory()
        pass

    def create_new_product(self):
        self.clear_widgets()
        self.current = 'insert_tabladeporte'
        self.add_widget(InsertDataWid_tabladeporte())

    def on_row_press(self, instance_table, instance_row):
        '''Called when a table row is clicked.'''
        pass
        # print(instance_table, instance_row)

    def on_check_press(self, instance_table, current_row):
        '''Called when the check box in the table row is checked.'''
        if current_row[0] not in self.objeto_seleccionado:
            self.objeto_seleccionado.append(current_row[0])
        else:
            self.objeto_seleccionado.remove(current_row[0])
        # print(instance_table, current_row)
        a = 0

    def delete_ejercicio(self):

        con = sqlite3.connect(self.ruta_DB_PATH_tabladeporte)
        cursor = con.cursor()
        for elemento_i in self.objeto_seleccionado:
            s = 'delete from tabladeporte where ID=' + elemento_i
            cursor.execute(s)
            con.commit()
        con.close()
        self.check_memory()

    def edit_ejercicio(self):
        if len(self.objeto_seleccionado) != 1:
            message = self.Popup.ids.message
            self.Popup.open()
            self.Popup.title = "Selección Múltiple"
            message.text = 'Solo es posible editar un registro'
        else:
            pass
            # self.clear_widgets()
            # self.current = 'edit_tabladeporte'
            # self.add_widget(EditDataWid_tabladeporte())



class DataBaseWid_inventario(MDScreen):
    # row_default_height define la altura de los widget integrados. Cambiar en la parte kv
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.Selectdb = Selectdb
        self.num_rows = 10
        self.ruta_APP_PATH = os.getcwd()
        self.ruta_DB_PATH_inventario = self.ruta_APP_PATH + '/inventario.db'
        self.check_memory()

        # Lista en la base de datos:
        self.lista_ID = []
        self.lista_alimentos = []
        self.lista_cantidad = []
        self.lista_lista = []
        con = sqlite3.connect(self.ruta_DB_PATH_inventario)
        cursor = con.cursor()
        orden_execute = 'select * from inventario'
        cursor.execute(orden_execute)
        for i in cursor:
            ID = i[0]
            r0 = i[1]  # Alimento
            r1 = str(i[2])  # Cantidad
            r2 = str(i[3])  # Lista
            self.lista_ID.append(ID)
            self.lista_alimentos.append(r0)
            self.lista_cantidad.append(r1)
            self.lista_lista.append(r2)
        con.close()
        self.dict_inventario = dict(zip(self.lista_alimentos, self.lista_ID))

    def goto_main(self):
        self.clear_widgets()
        self.current = 'selectdb'
        self.add_widget(Selectdb())

    def check_memory(self):
        self.ids.lista_alimentos.clear_widgets()
        con = sqlite3.connect(self.ruta_DB_PATH_inventario)
        cursor = con.cursor()
        orden_execute = 'select * from inventario ORDER BY Concepto ASC LIMIT ' + str(
            self.num_rows)
        cursor.execute(orden_execute)
        for i in cursor:
            wid = DataWid_inventario(size_hint=(.5, .2))
            ID = str(i[0])
            r0 = i[1]  # Alimento
            r1 = str(i[2])  # Cantidad
            r2 = str(i[3])  # Lista
            texto_i = r0 + " " + r1
            wid.dataID = ID
            wid.dataCO = r0
            wid.dataCA = r1
            wid.dataLI = r2
            # self.ids.lista_alimentos.add_widget(
            #     OneLineListItem(
            #         text=texto_i,
            #     )
            # )
            self.ids.lista_alimentos.add_widget(wid)
        con.close()

    def add_10_more(self):
        self.num_rows = self.num_rows + 10
        self.check_memory()

    def create_new_product(self):
        self.num_rows = 10
        self.clear_widgets()
        self.current = 'insert_inventario'
        self.add_widget(InsertDataWid_inventario())

    def set_list_md_icons(self, text="", search=False):
        '''Builds a list of icons for the screen MDIcons.'''

        # Nos traemos la lista de la db
        if len(text) > 1:  # Para evitar listas largas que carguen el sistema
            self.ids.lista_alimentos.clear_widgets()
            for name_icon in self.lista_alimentos:
                if search:
                    if text.lower() in name_icon.lower():
                        wid = DataWid_inventario()
                        wid.dataCO = name_icon

                        ID = self.dict_inventario.get(name_icon)
                        con = sqlite3.connect(self.ruta_DB_PATH_inventario)
                        cursor = con.cursor()
                        orden_execute = 'SELECT * FROM inventario WHERE ID = %s' % ID
                        cursor.execute(orden_execute)
                        for i in cursor:
                            wid.dataCA = str(i[2])
                            wid.dataID = str(ID)
                            wid.dataLI = str(i[3])
                        con.close()

                        self.ids.lista_alimentos.add_widget(wid)
                else:
                    pass
                    # TODO: Sugerir añadir a la lista del inventario.

    def selected_categoria(self, texto):
        self.ids.search_field.text = texto

    def lista_compra(self):
        self.ids.lista_alimentos.clear_widgets()

        con = sqlite3.connect(self.ruta_DB_PATH_inventario)
        cursor = con.cursor()
        orden_execute = 'select * from inventario WHERE Cantidad <= Lista ORDER BY Concepto ASC LIMIT ' + str(
            self.num_rows)
        cursor.execute(orden_execute)
        for i in cursor:
            wid = DataWid_inventario(size_hint=(.5, .2))
            ID = str(i[0])
            r0 = i[1]  # Alimento
            r1 = str(i[2])  # Cantidad
            r2 = str(i[3])  # Lista
            texto_i = r0 + " " + r1
            wid.dataID = ID
            wid.dataCO = r0
            wid.dataCA = r1
            wid.dataLI = r2
            # self.ids.lista_alimentos.add_widget(
            #     OneLineListItem(
            #         text=texto_i,
            #     )
            # )
            self.ids.lista_alimentos.add_widget(wid)
        con.close()


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


class DataWid_inventario(MDCard):  # Usado en el check_memory para visualizar los registros en cada widget mini
    def __init__(self, **kwargs):
        super(DataWid_inventario, self).__init__()
        self.Selectdb = Selectdb
        self.ruta_APP_PATH = os.getcwd()
        self.ruta_DB_PATH_inventario = self.ruta_APP_PATH + '/inventario.db'

    def add_one(self):
        self.dataCA = str(int(self.dataCA) + 1)
        con = sqlite3.connect(self.ruta_DB_PATH_inventario)
        cursor = con.cursor()
        a1 = (self.dataCO, self.dataCA, self.dataLI)
        s1 = 'UPDATE inventario SET '
        s2 = 'Concepto="%s",Cantidad="%s",Lista=%s ' % a1
        s3 = 'WHERE ID=%s' % self.dataID
        orden_execute = s1 + s2 + s3
        cursor.execute(orden_execute)
        con.commit()
        con.close()

    def rest_one(self):
        self.dataCA = str(int(self.dataCA) - 1)
        con = sqlite3.connect(self.ruta_DB_PATH_inventario)
        cursor = con.cursor()
        a1 = (self.dataCO, self.dataCA, self.dataLI)
        s1 = 'UPDATE inventario SET '
        s2 = 'Concepto="%s",Cantidad="%s",Lista=%s ' % a1
        s3 = 'WHERE ID=%s' % self.dataID
        orden_execute = s1 + s2 + s3
        cursor.execute(orden_execute)
        con.commit()
        con.close()

    def delete_data(self):
        con = sqlite3.connect(self.ruta_DB_PATH_inventario)
        cursor = con.cursor()
        s = 'delete from inventario where ID=' + self.dataID
        cursor.execute(s)
        con.commit()
        con.close()
        self.back_to_dbw()

    def back_to_dbw(self):
        self.clear_widgets()
        self.add_widget(Eliminado_inventario())


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


class InsertDataWid_tabladeporte(BoxLayout):
    def __init__(self, **kwargs):
        super(InsertDataWid_tabladeporte, self).__init__()
        today = date.today()
        # d1 = today.strftime("%d/%m/%Y")
        # self.ids.ti_fechao.text = d1
        self.ruta_APP_PATH = os.getcwd()
        self.ruta_DB_PATH_tabladeporte = self.ruta_APP_PATH + '/tabladeporte.db'
        self.Popup = MessagePopup()

    def insert_data(self):
        con = sqlite3.connect(self.ruta_DB_PATH_tabladeporte)
        cursor = con.cursor()
        cursor.execute('select ID from tabladeporte ORDER BY ID DESC LIMIT 1')
        con.commit()
        d1 = 1
        for i in cursor:
            d1 = i[0] + 1
        con.close()
        con = sqlite3.connect(self.ruta_DB_PATH_tabladeporte)
        cursor = con.cursor()
        d2 = self.ids.tb_Concepto.text
        d3 = self.ids.tb_kcal.text
        d4 = self.ids.tb_Cardio.text
        d5 = self.ids.tb_Brazo.text
        d6 = self.ids.tb_Pecho.text
        d7 = self.ids.tb_Espalda.text
        d8 = self.ids.tb_Pierna.text
        # La suma de los componentes debe ser 100:
        if float(d4) + float(d5) + float(d6) + float(d7) + float(d8) == 100:
            a1 = (d1, d2, d3, d4, d5, d6, d7, d8)
            s1 = 'INSERT INTO tabladeporte(ID, Concepto, kcal, Cardio, Brazo, Pecho, Espalda, Pierna)'
            s2 = 'VALUES(%s,"%s",%s,%s,%s,%s,%s,%s)' % a1
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
        else:
            message = self.Popup.ids.message
            self.Popup.open()
            self.Popup.title = "Error de formato"
            message.text = 'La suma de los porcentajes debe ser 100'

    def back_to_dbw(self):
        self.clear_widgets()
        self.current = 'db_tabladeporte'
        self.add_widget(DB_tabladeporte())


class InsertDataWid_inventario(BoxLayout):
    def __init__(self, **kwargs):
        super(InsertDataWid_inventario, self).__init__()
        self.ruta_APP_PATH = os.getcwd()
        self.ruta_DB_PATH_inventario = self.ruta_APP_PATH + '/inventario.db'
        self.Popup = MessagePopup()

    def insert_data(self):
        con = sqlite3.connect(self.ruta_DB_PATH_inventario)
        cursor = con.cursor()
        cursor.execute('select ID from inventario ORDER BY ID DESC LIMIT 1')
        con.commit()
        #
        d1 = 1
        for i in cursor:
            d1 = i[0] + 1
        con.close()
        con = sqlite3.connect(self.ruta_DB_PATH_inventario)
        cursor = con.cursor()

        d2 = self.ids.ti_Concepto.text
        d3 = self.ids.ti_Cantidad.text
        d4 = self.ids.ti_Lista.text
        a1 = (d1, d2, d3, d4)
        s1 = 'INSERT INTO inventario(ID, Concepto,	Cantidad, Lista)'
        s2 = 'VALUES(%s,"%s","%s","%s")' % a1
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
        self.current = 'db_inventario'
        self.add_widget(DataBaseWid_inventario())


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
    db_tabladeporte:
    selectdb:
    insert_movimientos:
    insert_inventario:
    datawid:
    update_movimientos:
    eliminado:
    eliminado_inventario:
    actualizado:
    db_inventario:
    
<DataloaderLabel_select@AKLabelLoader>
    size_hint_y: None
    height: dp(20)
    theme_text_color: "Primary"
    halign: "left"
    
<InventarioOneLineIconListItem>
    on_release:root.parent.parent.parent.parent.selected_categoria(self.text)
    IconLeftWidget:
        icon: root.icon

<RoundedButtonInventario@Button>:
    background_color: 0,0,0,0  # the last zero is the critical on, make invisible
    canvas.before:
        Color:
            rgba: (.4,.4,.4,1) if self.state=='normal' else (0,.7,.7,1)  # visual feedback of press
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [50,]


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
                
                
<DB_tabladeporte>:
    name:"db_tabladeporte"
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
            title: "Tablas Ejercicio"
        GridLayout:
            id: container
            padding: [10,10,10,10]
            spacing: 5
            size_hint_y: None
            cols: 1
            row_default_height: root.height*0.8
            height: self.minimum_height
            
                
        AKFloatingRoundedAppbar:

            AKFloatingRoundedAppbarButtonItem:
                icon: "keyboard-return"
                text: "Atrás"
                on_release: root.goto_main()
    
            AKFloatingRoundedAppbarButtonItem:
                icon: "delete-outline"
                text: "Eliminar"
                on_release: root.delete_ejercicio()
                
            AKFloatingRoundedAppbarButtonItem:
                icon: "square-edit-outline"
                text: "Editar"
                on_release: root.edit_ejercicio()
                
            AKFloatingRoundedAppbarButtonItem:
                icon: "plus-circle-outline"
                text: "Añadir"
                on_release: root.create_new_product()

<DataBaseWid_inventario>:
    name:"db_inventario"
    canvas:
        Color:
            rgb: 4/255,150/255,163/255,1
        Rectangle:
            pos: self.pos
            size: self.size
    padding: '1dp', '1dp'
    spacing: '1dp', '1dp'
    MDBoxLayout:
        orientation: "vertical"
        MyToolbar:
            id: _toolbar
            title: "Inventario"
        MDBoxLayout:
            adaptive_height: True
            canvas:
                Color:
                    rgb: 4/255,150/255,163/255,1
                Rectangle:
                    pos: self.pos
                    size: self.size
            MDIconButton:
                icon: 'magnify'
                icon_color: 1,1,1,1
            MDTextField:
                text_color: 1,1,1,1
                line_color_normal: 1,1,1,1
                id: search_field
                hint_text: 'Buscar'
                hint_text_color: 1,1,1,1
                on_text: root.set_list_md_icons(self.text, True)
        ScrollView:
            size: self.size
            GridLayout:
                id: lista_alimentos
                padding: [10,10,10,10]
                spacing: 1
                size_hint_y: None
                cols: 1
                row_default_height: root.height*0.09
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
            AKFloatingRoundedAppbarButtonItem:
                icon: "clipboard-list-outline"
                text:"Lista"
                on_release: root.lista_compra()
            AKFloatingRoundedAppbarButtonItem:
                icon: "refresh"
                text:"Refrescar"
                on_release: root.check_memory()
            

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
            DataloaderLabel_select:
                text:  root.dataID
                font_size: root.width * .04
            MDSeparator:
            
            DataloaderLabel_select:
                text:  root.dataCC
                
            MDSeparator:
            
            DataloaderLabel_select:
                text:  root.dataET
            MDSeparator:
            
            DataloaderLabel_select:
                text:  root.dataUB
            MDLabel:
                text: ""
            
        MDBoxLayout:
            size_hint_x: .3
            orientation:"vertical"
            MDLabel:
                text: ""
            DataloaderLabel_select:
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
            DataloaderLabel_select:
                text:  root.dataID
                font_size: root.width * .04
            MDSeparator:
            
            DataloaderLabel_select:
                text:  root.dataCO
            MDLabel:
                text: ""
                
        MDBoxLayout:
            size_hint_x: .3
            orientation:"vertical"
            MDLabel:
                text: ""
            DataloaderLabel_select:
                text:  root.dataTM
                halign: "center"
                valign: "center"
            MDLabel:
                text: ""

<DataWid_inventario>:
    padding: "8dp"
    name:"datawid_inventario"
    size_hint: .9, .2
    spacing: dp(5), dp(5)
    radius: [dp(10),]
    pos_hint: {"center_x": .5, "center_y": .5}
    dataID: ""
    dataCO: ""
    dataCA: ""
    dataLI: ""
    on_release: pass
    
    MDBoxLayout:
        orientation: "vertical"
        MDBoxLayout:
            orientation: "horizontal"
            size_hint_y: .01
            MDLabel:
                size_hint_x:.01
                text:""
            Button:
                size_hint: None, None
                background_color: 1,1,1,0
                text:"x"
                color: 251/255,58/255,58/255,1
                size: dp(15), dp(10)
                on_release: root.delete_data()
            MDLabel:
                size_hint_x:.8
                text:""
        MDBoxLayout:
            orientation: "horizontal"
            size_hint_y: .99
            MDBoxLayout:
                orientation: "vertical"
                size_hint_x: .5
                MDLabel:
                    text: ""
                DataloaderLabel_select:
                    text:  root.dataCO
                    font_size: root.width * .04
                MDLabel:
                    text: ""
            MDBoxLayout:
                size_hint_x: .2
                orientation: "vertical"
                MDLabel:
                    text: " "
                DataloaderLabel_select:
                    text:  root.dataCA
                    font_size: root.width * .04
                MDLabel:
                    text: " "
            MDBoxLayout:
                size_hint_x: .3
                MDBoxLayout:
                    orientation: "horizontal"
                    Button:
                        text: '-'
                        border: 5, 5, 5, 5
                        background_color: 14/255, 180/255, 195/255 , .7
                        on_release:root.rest_one()
                    Button:
                        text: '+'
                        background_color: 14/255, 180/255, 195/255 , .7
                        on_release:root.add_one()
        


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
            
<InsertDataWid_tabladeporte>:
    name:"insert_tabladeporte"
    orientation: 'vertical'
    canvas:
        Color:
            rgb: .254,.556,.627
        Rectangle:
            pos: self.pos
            size: self.size

    Label: # ---------- Concepto
        text: ' Concepto:'
    TextInput:
        id: tb_Concepto
        multiline: False
    Label: # ---------- kcal
        text: ' kcal:'
    TextInput:
        id: tb_kcal
        multiline: False
        hint_text: 'kcal:'
    Label: # ---------- Cardio
        text: ' Cardio:'
    TextInput:
        id: tb_Cardio
        multiline: False
        hint_text: '%'
    Label: # ---------- Brazo
        text: ' Brazo:'
    TextInput:
        id: tb_Brazo
        multiline: False
        hint_text: '%'
    Label: # ---------- Pecho
        text: ' Pecho:'
    TextInput:
        id: tb_Pecho
        multiline: False
        hint_text: '%'
    Label: # ---------- Espalda
        text: ' Espalda:'
    TextInput:
        id: tb_Espalda
        multiline: False
        hint_text: '%'
    Label: # ---------- Pierna
        text: ' Pierna:'
    TextInput:
        id: tb_Pierna
        multiline: False
        hint_text: '%'
    BoxLayout:
        size_hint_y: 5
    BoxLayout: # ---------- Crear Salir
        Button:
            text: 'Crear'
            on_press: root.insert_data()
        Button:
            text: 'Salir'
            on_press: root.back_to_dbw()

<InsertDataWid_inventario>:
    name:"insert_movimientos"
    orientation: 'vertical'
    canvas:
        Color:
            rgb: .254,.556,.627
        Rectangle:
            pos: self.pos
            size: self.size

    Label: # ---------- Concepto
        text: ' Concepto:'
    TextInput:
        id: ti_Concepto
        multiline: False
        hint_text: 'Concepto:'
    Label: # ---------- Cantidad
        text: ' Cantidad:'
    TextInput:
        id: ti_Cantidad
        multiline: False
        hint_text: 'Cantidad'
    Label: # ---------- Lista
        text: ' Comprar cuando llegue a:'
    TextInput:
        id: ti_Lista
        multiline: False
        hint_text: 'Lista'
    
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
            
<Eliminado_inventario>:
    name: "eliminado_inventario"
    BoxLayout:
        orientation: 'vertical'
        Label:
            color: 0,0,0,1
            text: 'Registro eliminado'
            
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
