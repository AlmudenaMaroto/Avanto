from kivy.lang.builder import Builder
from kivymd.uix.screen import MDScreen
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
import sqlite3
import os
from datetime import datetime
import time
from calendar import timegm
import charts_almu
import chart_progress
from tasa_ahorro import Tabla_tasa_ahorro
from date_pick_esp import AKDatePicker_ini, AKDatePicker_fin
import datetime
from itertools import groupby
from kivy.uix.popup import Popup
from kivymd.uix.dialog import BaseDialog
from kivymd.theming import ThemableBehavior
# from kivymd_extensions.akivymd.uix.selectionlist import AKSelectListAvatarItem
from listas_config import AKSelectListAvatarItem_etapa
from charts_almu import AKPieChart_etapas
from datetime import date
from kivy.utils import platform
import csv
import collections

today = date.today()
lista_seleccionada_etapa = []
lista_seleccionada_categoria = []
global lista_etapas_posibles
lista_etapas_posibles = []
global inicial_etapas_tick
inicial_etapas_tick = 1

lista_seleccionada_categoria = []
global lista_categorias_posibles
lista_categorias_posibles = []
global inicial_categorias_tick
inicial_categorias_tick = 1


# conversion de epoch a fechas:
def epoch2human(epoch):
    return time.strftime('%m/%y',
                         time.localtime(int(epoch)))


def epoch2human_year(epoch):
    return time.strftime('%Y',
                         time.localtime(int(epoch)))


# Funciones para filtrar dict_sorted_eco.
def filtrar_dict_fechas(dic, epoch_ini, epoch_fin):
    return epoch_ini < dic['epoch'] < epoch_fin


def filtrar_ingresos(dic):
    return dic['importe'] > 0


def filtrar_gastos(dic):
    return dic['importe'] < 0


def filtrar_fecha_ini(dic, fecha_ini):
    return datetime.datetime.strptime(dic['fecha'], '%d/%m/%Y') > datetime.datetime.strptime(fecha_ini, '%d/%m/%Y')


def filtrar_fecha_fin(dic, fecha_fin):
    return datetime.datetime.strptime(dic['fecha'], '%d/%m/%Y') < datetime.datetime.strptime(fecha_fin, '%d/%m/%Y')


def filtrar_etapa(dic, lista_etapas):
    try:
        if platform == 'android':
            os.chdir('/storage/emulated/0/')
        with open('etapas_seleccionadas.csv', 'r', newline='', encoding='latin') as f:
            reader = csv.reader(f, delimiter=';')
            lista_etapas_seleccionadas = list(reader)
        for etapa_i in lista_etapas_seleccionadas[0]:
            if dic['etapa'] == etapa_i:
                return True
    except FileNotFoundError:
        return True


def filtrar_categoria(dic, lista_categoria):
    try:
        if platform == 'android':
            os.chdir('/storage/emulated/0/')
        with open('categorias_seleccionadas.csv', 'r', newline='', encoding='latin') as f:
            reader = csv.reader(f, delimiter=';')
            lista_categorias_seleccionadas = list(reader)
        for categoria_i in lista_categorias_seleccionadas[0]:
            if dic['categoria'] == categoria_i:
                return True
    except FileNotFoundError:
        return True


class MessagePopup_eco(Popup):
    pass


class Economia(MDScreen):
    def __init__(self, **kwargs):
        super(Economia, self).__init__()
        self.Popup = MessagePopup_eco()
        self.path_app = os.getcwd()
        self.dict_eco_sorted = {}
        self.dict_barmes = []
        self.dict_barano = []
        self.max_epoch_evtemp = 0
        self.min_epoch_evtemp = 0
        self.eje_y_max_evtemp = 0
        self.eje_y_min_evtemp = 0
        self.saldo_total = 0
        self.fecha_ini = ''
        self.fecha_fin = ''
        self.obj_cuenta = 0
        self.obj_fecha = 0
        self.obj_peso = 0
        self.domiciliaciones = ''
        self.ingresos = ''
        self.obj_tasa = 0
        self.lista_etapas = ''
        self.lista_categorias = ''
        self.filtrado_etapa = 1
        self.filtrado_categoria = 1
        self.etapas_posibles = ''
        self.categorias_posibles = ''
        self.date = ''
        self.error = 0
        self.piechart = ''
        self.ini_etapas = 1
        self.ini_etapa_filtro = True
        self.ini_categorias = 1
        self.ini_categoria_filtro = True
        self.update()

    def update(self):
        con = sqlite3.connect(self.path_app + '/globales.db')
        cursor = con.cursor()
        orden_execute = 'select * from globales'
        cursor.execute(orden_execute)
        for i in cursor:
            self.obj_cuenta = i[1]
            self.obj_fecha = i[2]
            self.obj_peso = i[3]
            self.domiciliaciones = i[4]
            self.ingresos = i[5]
            self.obj_tasa = i[6]
        con.close()
        self.calculos()
        if self.error == 1:
            self.error = 0
            return
        if self.error == 2:
            self.error = 0
            return
        self.barchart_datos()
        self.barchart_ano()
        self.calc_ahorros()
        # self.tabla_tasa_ahorro()
        self.pie_etapa_importe()
        self.pie_etapa_tiempo()
        self.ranking_gastos()
        self.ranking_ingresos()

        id_evtemp = self.ids.id_evtemp
        id_barmes = self.ids.id_barmes
        id_barano = self.ids.id_barano
        id_ranking_gastos = self.ids.id_ranking_gastos
        id_ranking_ingresos = self.ids.id_ranking_ingresos
        id_evtemp.update()
        id_barmes.update()
        id_barano.update()
        id_ranking_gastos.update()
        id_ranking_ingresos.update()

    def calculos(self):
        # Reseteo de nuevo
        self.dict_eco_sorted = {}
        self.dict_barmes = []
        self.dict_barano = []
        self.max_epoch_evtemp = 0
        self.min_epoch_evtemp = 0
        self.eje_y_max_evtemp = 0
        self.eje_y_min_evtemp = 0
        ########################
        # Linea temporal:      #
        ########################
        # Conseguir longitud del fichero
        con = sqlite3.connect(self.path_app + '/movimientos.db')
        cursor = con.cursor()
        orden_execute = 'select * from movimientos'
        cursor.execute(orden_execute)
        longitud = len(cursor.fetchall())
        if longitud == 0:
            message = self.Popup.ids.message
            self.Popup.open()
            self.Popup.title = "Vacío"
            message.text = 'Para poder analizar, deben existir registros.'
            self.error = 2
            return
        con.close()

        # Linea temporal: creamos una list of dict
        row_i = {}
        dict_eco = []
        saldo = 0
        con = sqlite3.connect(self.path_app + '/movimientos.db')
        cursor = con.cursor()
        orden_execute = 'select * from movimientos'
        cursor.execute(orden_execute)
        ticks_sobrecarga = round(longitud / 300)
        if ticks_sobrecarga == 0:
            ticks_sobrecarga = 1
        for i in cursor:
            # saldo = round(saldo + i[4], 2)
            try:
                utc_time = time.strptime(i[1], "%d/%m/%Y")
                epoch_time = timegm(utc_time)
                ano_mes = datetime.datetime.strptime(str(i[1]), '%d/%m/%Y').strftime('%m/%y')
                # Agrupamos en un diccionario para cada linea, para poder ordenarlo
                row_i['fecha'] = str(i[1])
                row_i['anomes'] = ano_mes
                row_i['epoch'] = epoch_time
                row_i['importe'] = i[4]
                # row_i['saldo'] = saldo
                row_i['concepto'] = i[2]
                row_i['categoria'] = i[3]
                row_i['etapa'] = i[5]
                row_i['ubicacion'] = i[6]
                dict_eco.append(row_i)
                row_i = {}

            except ValueError:
                pass
        con.close()

        ###########################
        # Ordenamos y añadimos saldo
        self.dict_eco_sorted = sorted(dict_eco, key=lambda d: d['epoch'], reverse=False)
        i = 0
        for row_i in self.dict_eco_sorted:
            saldo = saldo + row_i['importe']
            self.dict_eco_sorted[i]['saldo'] = round(saldo, 2)
            i = i + 1
        ################ FILTROS ####################
        if self.fecha_ini != '':
            self.dict_eco_sorted = [d for d in self.dict_eco_sorted if filtrar_fecha_ini(d, self.fecha_ini)]
        if self.fecha_fin != '':
            self.dict_eco_sorted = [d for d in self.dict_eco_sorted if filtrar_fecha_fin(d, self.fecha_fin)]
        if not self.ini_etapa_filtro:
            self.dict_eco_sorted = [d for d in self.dict_eco_sorted if filtrar_etapa(d, lista_seleccionada_etapa)]
        self.ini_etapa_filtro = False
        if not self.ini_categoria_filtro:
            self.dict_eco_sorted = [d for d in self.dict_eco_sorted if
                                    filtrar_categoria(d, lista_seleccionada_categoria)]
        self.ini_categoria_filtro = False

        # Si está vacío mensaje de error y reseteamos los filtros:
        if self.dict_eco_sorted == []:
            message = self.Popup.ids.message
            self.Popup.open()
            self.Popup.title = "Vacío"
            message.text = 'No hay datos que cumplan el criterio'
            self.error = 1
            return

        #############################################
        # Para no petar el grafico, cogemos menos valores
        maximo_saldo = max(self.dict_eco_sorted, key=lambda x: x['saldo']).get('saldo')
        minimo_saldo = min(self.dict_eco_sorted, key=lambda x: x['saldo']).get('saldo')
        max_epoch = max(self.dict_eco_sorted, key=lambda x: x['epoch']).get('epoch')
        min_epoch = min(self.dict_eco_sorted, key=lambda x: x['epoch']).get('epoch')

        eje_y_max = round(maximo_saldo, -3) + 1000
        eje_y_min = round(minimo_saldo, -3)

        num_saltos = 4
        label_x_paso = []
        label_y_paso = []
        for i in range(num_saltos + 1):
            paso_y = (eje_y_max - eje_y_min) / num_saltos
            paso_x = (max_epoch - min_epoch) / num_saltos
            label_x_paso.append(min_epoch + i * paso_x)
            label_y_paso.append(eje_y_min + i * paso_y)
        label_x_paso = [epoch2human(t) for t in label_x_paso]

        valores_x_reducidos = [d['epoch'] for d in self.dict_eco_sorted if 'epoch' in d][0::ticks_sobrecarga]
        valores_y_reducidos = [d['saldo'] for d in self.dict_eco_sorted if 'saldo' in d][0::ticks_sobrecarga]
        self.ids.id_evtemp.x_values = valores_x_reducidos
        self.ids.id_evtemp.x_labels = label_x_paso
        self.ids.id_evtemp.y_values = valores_y_reducidos
        self.ids.id_evtemp.y_labels = label_y_paso

        # Cuenta actual
        self.saldo_total = 0
        self.saldo_total = sum(item['importe'] for item in self.dict_eco_sorted)
        self.ids.saldo_total.text = str(round(self.saldo_total, 2)) + ' €'

    def barchart_datos(self):
        for row_i in self.dict_eco_sorted:
            barmes_i = {}
            barmes_i['importe'] = row_i['importe']
            barmes_i['anomes'] = row_i['anomes']
            self.dict_barmes.append(barmes_i)
        dict_anomes_red = []
        for k, v in groupby(self.dict_barmes, key=lambda x: x['anomes']):
            linea = {'anomes': k, 'importe': sum(int(d['importe']) for d in v)}
            utc_time = time.strptime(k, "%m/%y")
            epoch_time = timegm(utc_time)
            linea['epoch'] = epoch_time
            dict_anomes_red.append(linea)

        self.ids.id_barmes.x_values = [d['epoch'] for d in dict_anomes_red if 'epoch' in d]
        self.ids.id_barmes.y_values = [d['importe'] for d in dict_anomes_red if 'importe' in d]

        self.max_epoch_evtemp = max(self.ids.id_barmes.x_values)
        self.min_epoch_evtemp = min(self.ids.id_barmes.x_values)
        self.eje_y_max_evtemp = round(max(self.ids.id_barmes.y_values), -3) + 1000
        self.eje_y_min_evtemp = round(min(self.ids.id_barmes.y_values), -3)
        num_saltos = 4
        label_x_paso = []
        label_y_paso = []
        for i in range(num_saltos + 1):
            paso_y = (self.eje_y_max_evtemp - self.eje_y_min_evtemp) / num_saltos
            paso_x = (self.max_epoch_evtemp - self.min_epoch_evtemp) / num_saltos
            label_x_paso.append(self.min_epoch_evtemp + i * paso_x)
            label_y_paso.append(self.eje_y_min_evtemp + i * paso_y)
        label_x_paso = [epoch2human(t) for t in label_x_paso]

        self.ids.id_barmes.x_labels = label_x_paso
        self.ids.id_barmes.y_labels = label_y_paso

    def barchart_ano(self):

        for row_i in self.dict_eco_sorted:
            barmes_i = {}
            barmes_i['importe'] = row_i['importe']
            barmes_i['anomes'] = row_i['anomes'][-2:]
            self.dict_barano.append(barmes_i)
        dict_anomes_red = []
        for k, v in groupby(self.dict_barano, key=lambda x: x['anomes']):
            linea = {'anomes': k, 'importe': sum(int(d['importe']) for d in v)}
            utc_time = time.strptime(k, "%y")
            epoch_time = timegm(utc_time)
            linea['epoch'] = epoch_time
            dict_anomes_red.append(linea)

        self.ids.id_barano.x_values = [d['epoch'] for d in dict_anomes_red if 'epoch' in d]
        self.ids.id_barano.y_values = [d['importe'] for d in dict_anomes_red if 'importe' in d]

        self.max_epoch_evtemp = max([int('20' + d['anomes']) for d in dict_anomes_red if 'anomes' in d]) + 1
        self.min_epoch_evtemp = min([int('20' + d['anomes']) for d in dict_anomes_red if 'anomes' in d])
        self.eje_y_max_evtemp = round(max(self.ids.id_barano.y_values), -3) + 1000
        self.eje_y_min_evtemp = round(min(self.ids.id_barano.y_values), -3)
        num_saltos = len(dict_anomes_red)
        label_x_paso = []
        label_y_paso = []
        for i in range(num_saltos):
            paso_y = (self.eje_y_max_evtemp - self.eje_y_min_evtemp) / num_saltos
            paso_x = (self.max_epoch_evtemp - self.min_epoch_evtemp) / num_saltos
            label_x_paso.append(str(round(self.min_epoch_evtemp + i * paso_x)))
            label_y_paso.append(self.eje_y_min_evtemp + i * paso_y)
        # label_x_paso = [epoch2human_year(t) for t in label_x_paso]

        self.ids.id_barano.x_labels = label_x_paso
        self.ids.id_barano.y_labels = label_y_paso

    def set_text_evtemp(self, args):
        # Como hemos guardado los valores de los ejes max y min en self podemos usarlos para calcular
        # la conversion y hacer print del valor.
        # size = [50, 180]
        # dist_x = self.max_epoch_evtemp - self.min_epoch_evtemp
        # dist_y = self.eje_y_max_evtemp - self.eje_y_min_evtemp
        # eje_x = epoch2human((args[2] / size[0]) * dist_x + self.min_epoch_evtemp)
        # eje_y = int((args[3] / size[1]) * dist_y + self.eje_y_min_evtemp)
        # self.ids._label_evtemp.text = f"[{eje_x},{eje_y}]"
        pass

    def calc_ahorros(self):

        # Porcentaje de ahorro:
        porcentaje_ahorro = self.saldo_total * 100 / self.obj_cuenta
        self.ids.progress_percent.cambiar_porc(porcentaje_ahorro)
        # Ahorro mensual a realizar:
        fecha_obj = datetime.datetime.strptime(self.obj_fecha, '%d/%m/%Y')
        diff_fechas = (fecha_obj - datetime.datetime.strptime(today.strftime("%d/%m/%Y"), '%d/%m/%Y')).days
        self.ids.ahorro_mensual_obj.text = str(round((self.obj_cuenta - self.saldo_total) * 30 / diff_fechas)) + ' €'
        # Gasto en domiciliaciones al mes (ultimos 30 dias)
        domiciliaciones_list = self.domiciliaciones.replace(' ', '').split(',')
        epoch_fin = datetime.datetime.strptime(today.strftime("%d/%m/%Y"), '%d/%m/%Y').timestamp()
        epoch_ini = (datetime.datetime.strptime(today.strftime("%d/%m/%Y"), '%d/%m/%Y') - datetime.timedelta(
            days=30)).timestamp()
        dict_domic = list(filter(lambda d: d['categoria'] in domiciliaciones_list, self.dict_eco_sorted))
        dict_domic_fech = [d for d in dict_domic if filtrar_dict_fechas(d, epoch_ini, epoch_fin)]
        self.ids.domiciliaciones_mes.text = str(-round(sum(item['importe'] for item in dict_domic_fech), 2)) + ' €'


    def choose_etapa(self):
        # Si ya hemos calculado las etapas, no hay que calcularlas de nuevo, o perdemos elementos de la lista.
        global lista_etapas_posibles
        if self.filtrado_etapa:
            self.etapas_posibles = list(dict.fromkeys([d['etapa'] for d in self.dict_eco_sorted if 'etapa' in d]))
        self.filtrado_etapa = 0
        lista_etapas_posibles = self.etapas_posibles.copy()
        if platform == 'android':
            os.chdir('/storage/emulated/0/')
        with open('etapas_lista.csv', 'w', newline='', encoding='latin') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow(lista_etapas_posibles)
        if self.ini_etapas:
            with open('etapas_seleccionadas.csv', 'w', newline='', encoding='latin') as f:
                writer = csv.writer(f, delimiter=';')
                writer.writerow(lista_etapas_posibles)
            self.ini_etapas = 0

        a = Selectionlist_etapa()
        a.on_enter(self.etapas_posibles)
        a.open()

    def choose_categoria(self):
        # Si ya hemos calculado las etapas, no hay que calcularlas de nuevo, o perdemos elementos de la lista.
        global lista_categorias_posibles
        if self.filtrado_categoria:
            self.categorias_posibles = list(
                dict.fromkeys([d['categoria'] for d in self.dict_eco_sorted if 'categoria' in d]))
        self.filtrado_categoria = 0
        lista_categorias_posibles = self.categorias_posibles.copy()
        if platform == 'android':
            os.chdir('/storage/emulated/0/')
        with open('categorias_lista.csv', 'w', newline='', encoding='latin') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow(lista_categorias_posibles)
        if self.ini_categorias:
            with open('categorias_seleccionadas.csv', 'w', newline='', encoding='latin') as f:
                writer = csv.writer(f, delimiter=';')
                writer.writerow(lista_categorias_posibles)
            self.ini_categorias = 0

        a = Selectionlist_categoria()
        a.on_enter(self.categorias_posibles)
        a.open()

    def choose_fecha(self):
        self.date = AKDatePicker_ini(callback=self.callback_ini)
        self.date.open()
        self.date = AKDatePicker_fin(callback=self.callback_fin)
        self.date.open()

    def callback_ini(self, date_i):
        if not date_i:
            return
        self.fecha_ini = "%d/%d/%d" % (date_i.day, date_i.month, date_i.year)

    def callback_fin(self, date_i):
        if not date_i:
            return
        self.fecha_fin = "%d/%d/%d" % (date_i.day, date_i.month, date_i.year)

    def pie_etapa_importe(self):
        # Para que no se duplique el grafico hay que borrarlo.
        self.ids.chart_box_etapaimporte.clear_widgets()
        dict_etapa_importe = []
        list_dict_etapa_importe = {}
        for k, v in groupby(self.dict_eco_sorted, key=lambda x: x['etapa']):
            linea = {k: sum(int(d['importe']) * 100 / self.saldo_total for d in v)}
            if linea[k] < 0:
                linea[k] = 0
            list_dict_etapa_importe[k] = linea.get(k)
            # dict_etapa_importe.append(linea)
        total_perc = sum(list_dict_etapa_importe.values())
        list_dict_etapa_importe.update((x, round(y * 100 / total_perc, 0)) for x, y in list_dict_etapa_importe.items())
        porc_real = sum(list_dict_etapa_importe.values())
        lista_etapas_total = set(d['etapa'] for d in self.dict_eco_sorted)
        for etapa_i in lista_etapas_total:
            pass
        if porc_real != 100:
            list_dict_etapa_importe[etapa_i] = list_dict_etapa_importe[etapa_i] + 100 - porc_real
        # Eliminamos los registros 0% para mejorar el grafico
        list_dict_etapa_importe = {key: val for key, val in list_dict_etapa_importe.items() if val != 0}
        self.piechart = AKPieChart_etapas(
            items=[list_dict_etapa_importe],
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            size_hint=[None, None],
            size=(dp(250), dp(250)),
        )
        self.ids.chart_box_etapaimporte.add_widget(self.piechart)

    def pie_etapa_tiempo(self):
        # Para que no se duplique el grafico hay que borrarlo.
        self.ids.chart_box_etapatiempo.clear_widgets()
        # Conseguir lista de etapas que hay
        tiempos = []
        list_dict_etapa_tiempo = {}
        lista_etapas_total = set(d['etapa'] for d in self.dict_eco_sorted)
        for etapa_i in lista_etapas_total:
            dict_etapa_i = [d for d in self.dict_eco_sorted if d['etapa'] in etapa_i]
            max_epoch = max(dict_etapa_i, key=lambda x: x['epoch']).get('epoch')
            min_epoch = min(dict_etapa_i, key=lambda x: x['epoch']).get('epoch')
            tiempo_en_etapa = max_epoch - min_epoch
            tiempos.append(tiempo_en_etapa)
            list_dict_etapa_tiempo[etapa_i] = tiempo_en_etapa

        total_perc = sum(tiempos)
        list_dict_etapa_tiempo.update((x, round(y * 100 / total_perc, 0)) for x, y in list_dict_etapa_tiempo.items())
        porc_real = sum(list_dict_etapa_tiempo.values())
        if porc_real != 100:
            list_dict_etapa_tiempo[etapa_i] = list_dict_etapa_tiempo[etapa_i] + 100 - porc_real

        list_dict_etapa_tiempo = {key: val for key, val in list_dict_etapa_tiempo.items() if val != 0}
        self.piechart = AKPieChart_etapas(
            items=[list_dict_etapa_tiempo],
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            size_hint=[None, None],
            size=(dp(250), dp(250)),
        )
        self.ids.chart_box_etapatiempo.add_widget(self.piechart)

    def ranking_gastos(self):
        # Filtramos por gastos (<0)
        # Con counter agrupamos los importes del mismo concepto.
        # ordenamos por max valor sorted_x.reverse() para inverso y redondeamos. Cogemos 10 primeros
        list_of_dict_gastos = [d for d in self.dict_eco_sorted if d['importe'] < 0]
        dict_ranking_gastos = collections.Counter()
        for d in list_of_dict_gastos:
            dict_ranking_gastos[d['concepto']] += (d['importe'])
        dict_ranking_gastos = dict(dict_ranking_gastos)
        dict_ranking_gastos = dict(sorted(dict_ranking_gastos.items(), key=lambda item: item[1]))
        dict_ranking_gastos = {key: round(-dict_ranking_gastos[key], 2) for key in dict_ranking_gastos}
        dict_ranking_gastos = {k: dict_ranking_gastos[k] for k in list(dict_ranking_gastos)[:10]}
        dict_ranking_gastos = dict(sorted(dict_ranking_gastos.items(), key=lambda item: item[1]))

        # Labels y values para el grafico

        self.ids.id_ranking_gastos.y_values = list(dict_ranking_gastos.values())
        # x_value es la longitud del ranking
        label_y_paso = []
        i = 0
        for i in range(len(dict_ranking_gastos)):
            paso_y = (max(self.ids.id_ranking_gastos.y_values) - min(self.ids.id_ranking_gastos.y_values)) / len(
                dict_ranking_gastos)
            label_y_paso.append(min(self.ids.id_ranking_gastos.y_values) + i * paso_y)

        self.ids.id_ranking_gastos.x_values = [*range(len(dict_ranking_gastos))]
        self.ids.id_ranking_gastos.x_labels = list(dict_ranking_gastos.keys())
        self.ids.id_ranking_gastos.y_labels = label_y_paso

    def ranking_ingresos(self):
        list_of_dict_gastos = [d for d in self.dict_eco_sorted if d['importe'] > 0]
        dict_ranking_gastos = collections.Counter()
        for d in list_of_dict_gastos:
            dict_ranking_gastos[d['concepto']] += (d['importe'])
        dict_ranking_gastos = dict(dict_ranking_gastos)
        dict_ranking_gastos = dict(sorted(dict_ranking_gastos.items(), key=lambda item: item[1], reverse=True))
        dict_ranking_gastos = {key: round(dict_ranking_gastos[key], 2) for key in dict_ranking_gastos}
        dict_ranking_gastos = {k: dict_ranking_gastos[k] for k in list(dict_ranking_gastos)[:10]}
        dict_ranking_gastos = dict(sorted(dict_ranking_gastos.items(), key=lambda item: item[1]))

        # Labels y values para el grafico

        self.ids.id_ranking_ingresos.y_values = list(dict_ranking_gastos.values())
        # x_value es la longitud del ranking
        label_y_paso = []
        i = 0
        for i in range(len(dict_ranking_gastos)):
            paso_y = (max(self.ids.id_ranking_ingresos.y_values) - min(self.ids.id_ranking_ingresos.y_values)) / len(
                dict_ranking_gastos)
            label_y_paso.append(min(self.ids.id_ranking_ingresos.y_values) + i * paso_y)

        self.ids.id_ranking_ingresos.x_values = [*range(len(dict_ranking_gastos))]
        self.ids.id_ranking_ingresos.x_labels = list(dict_ranking_gastos.keys())
        self.ids.id_ranking_ingresos.y_labels = label_y_paso

    def tabla_tasa_ahorro(self):
        # self.dict_eco_sorted
        list_of_dict_gastos = [d for d in self.dict_eco_sorted if d['categoria'] not in self.ingresos]
        list_of_dict_ingresos = [d for d in self.dict_eco_sorted if d['categoria'] in self.ingresos]
        a = 0

        self.date = AKDatePicker_ini(callback=self.callback_ini)
        self.date.open()


class Selectionlist_etapa(BaseDialog, ThemableBehavior):
    def on_enter(self, etapas_posibles):
        if platform == 'android':
            os.chdir('/storage/emulated/0/')
        with open('etapas_lista.csv', 'r', newline='', encoding='latin') as f:
            reader = csv.reader(f, delimiter=';')
            self.lista_etapas_posibles = list(reader)
        lista_estados_a_marcar = [True] * len(self.lista_etapas_posibles[0])
        self.inicial_etapas_tick = 0

        lista_estados_a_marcar = [False] * (len(self.lista_etapas_posibles[0]))
        # Leemos el csv con las que si estan marcadas
        if platform == 'android':
            os.chdir('/storage/emulated/0/')
        with open('etapas_seleccionadas.csv', 'r', newline='', encoding='latin') as f:
            reader = csv.reader(f, delimiter=';')
            lista_etapas_seleccionadas = list(reader)
        i = 0
        for element in self.lista_etapas_posibles[0]:
            if element in lista_etapas_seleccionadas[0]:
                if i == 0:
                    lista_estados_a_marcar[len(lista_estados_a_marcar) - 1] = True
                else:
                    lista_estados_a_marcar[i - 1] = True
            i = i + 1

        # Hay que duplicar esto por no se por que alguna razon no coge bien el tick del primer termino
        # lista_estados_a_marcar = [True, True, True, True, False]
        self.ids.selectionlist.clear_widgets()
        i = 0
        for x in etapas_posibles:
            estado_check_box = lista_estados_a_marcar[i]
            self.ids.selectionlist.add_widget(
                AKSelectListAvatarItem_etapa(first_label=x, estado_check=estado_check_box))
            i = i + 1
        self.ids.selectionlist.clear_widgets()
        i = 0
        for x in etapas_posibles:
            estado_check_box = lista_estados_a_marcar[i]
            self.ids.selectionlist.add_widget(
                AKSelectListAvatarItem_etapa(first_label=x, estado_check=estado_check_box))
            i = i + 1

    def cancel(self):
        self.on_leave()
        self.dismiss()

    def _choose(self):
        lista_seleccionadas = self.lista_etapas_posibles[0].copy()
        # Al clickar estas retirandolo, la lista contiente los que NO se deben seleccionar.
        # Entonces, cuando limpiemos, la lista debe estar completa

        for element in self.ids.selectionlist.get_selection():
            if element in self.lista_etapas_posibles[0]:
                lista_seleccionadas.remove(element)

        with open('etapas_seleccionadas.csv', 'w', newline='', encoding='latin') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow(lista_seleccionadas)
        self.on_leave()
        self.dismiss()

    def _unselect(self):
        pass
        # global lista_etapas_posibles
        # lista_seleccionadas = []
        # with open('etapas_seleccionadas.csv', 'w', newline='', encoding='latin') as f:
        #     writer = csv.writer(f, delimiter=';')
        #     writer.writerow(lista_seleccionadas)
        # for element in lista_etapas_posibles:
        #     self.ids.selectionlist.
        # self.on_enter(lista_etapas_posibles)

    def on_leave(self):
        return self.clear_selected()

    def get_selected(self):
        items = self.ids.selectionlist.get_selection()
        text = ""
        for x in items:
            text += ", %s" % x
        return text

    def clear_selected(self):
        return self.ids.selectionlist.clear_selection()

    def select_all(self):
        return self.ids.selectionlist.select_all()


class Selectionlist_categoria(BaseDialog, ThemableBehavior):
    def on_enter(self, categorias_posibles):
        if platform == 'android':
            os.chdir('/storage/emulated/0/')
        with open('categorias_lista.csv', 'r', newline='', encoding='latin') as f:
            reader = csv.reader(f, delimiter=';')
            self.lista_categorias_posibles = list(reader)
        lista_estados_a_marcar = [True] * len(self.lista_categorias_posibles[0])
        self.inicial_categorias_tick = 0

        lista_estados_a_marcar = [False] * (len(self.lista_categorias_posibles[0]))
        # Leemos el csv con las que si estan marcadas
        if platform == 'android':
            os.chdir('/storage/emulated/0/')
        with open('categorias_seleccionadas.csv', 'r', newline='', encoding='latin') as f:
            reader = csv.reader(f, delimiter=';')
            lista_categorias_seleccionadas = list(reader)
        i = 0
        for element in self.lista_categorias_posibles[0]:
            if element in lista_categorias_seleccionadas[0]:
                if i == 0:
                    lista_estados_a_marcar[len(lista_estados_a_marcar) - 1] = True
                else:
                    lista_estados_a_marcar[i - 1] = True
            i = i + 1

        # Hay que duplicar esto por no se por que alguna razon no coge bien el tick del primer termino
        # lista_estados_a_marcar = [True, True, True, True, False]
        self.ids.selectionlist_categoria.clear_widgets()
        i = 0
        for x in categorias_posibles:
            estado_check_box = lista_estados_a_marcar[i]
            self.ids.selectionlist_categoria.add_widget(
                AKSelectListAvatarItem_etapa(first_label=x, estado_check=estado_check_box))
            i = i + 1
        self.ids.selectionlist_categoria.clear_widgets()
        i = 0
        for x in categorias_posibles:
            estado_check_box = lista_estados_a_marcar[i]
            self.ids.selectionlist_categoria.add_widget(
                AKSelectListAvatarItem_etapa(first_label=x, estado_check=estado_check_box))
            i = i + 1

    def cancel(self):
        self.on_leave()
        self.dismiss()

    def _choose(self):
        lista_seleccionadas = self.lista_categorias_posibles[0].copy()
        for element in self.ids.selectionlist_categoria.get_selection():
            if element in self.lista_categorias_posibles[0]:
                lista_seleccionadas.remove(element)
        with open('categorias_seleccionadas.csv', 'w', newline='', encoding='latin') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow(lista_seleccionadas)
        self.on_leave()
        self.dismiss()

    def _unselect(self):
        pass

    def on_leave(self):
        return self.clear_selected()

    def get_selected(self):
        items = self.ids.selectionlist_categoria.get_selection()
        text = ""
        for x in items:
            text += ", %s" % x
        return text

    def clear_selected(self):
        return self.ids.selectionlist_categoria.clear_selection()

    def select_all(self):
        return self.ids.selectionlist_categoria.select_all()


Builder.load_string(
    """
<Evolucion_temporal@AKLineChart_Almu>
    size_hint_y: None
    height: dp(180)
    x_values: []
    y_values: []
    label_size: dp(12)
    
<Barras_mes@AKBarChart_anomes>
    size_hint_y: None
    height: dp(180)
    x_values: [0, 5, 8, 15]
    y_values: [0, 10, 6, 8]
    label_size: dp(12)

<Barras_ano@AKBarChart_ano>
    size_hint_y: None
    height: dp(180)
    x_values: [0, 5, 8, 15]
    y_values: [0, 10, 6, 8]
    label_size: dp(12)
    

<Barras_horizontal@AKBarChart_horizontal>
    size_hint_y: None
    height: dp(180)
    x_values: [0, 5, 8, 15]
    y_values: [0, 10, 6, 8]
    label_size: dp(12)

<MessagePopup_eco>:
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

<Economia>
    on_leave: pass

    MDBoxLayout:
        orientation: "vertical"

        MyToolbar:
            id: _toolbar

        ScrollView:
            size_hint_y: 0.95
            MDBoxLayout:
                orientation: "vertical"
                spacing: dp(25)
                padding: dp(25)
                adaptive_height: True
                MDLabel:
                    id:saldo_total
                    halign: "center"
                    text_color: 0, 0, 1, 1
                    
                Evolucion_temporal:
                    id: id_evtemp
                    labels: True
                    anim: True
                    circles: False
                    bg_color: 106/255, 188/255, 206/255, 1
                    #on_select: root.set_text_evtemp(args)
                    line_width:dp(1)
                
                Barras_mes:
                    id: id_barmes
                    labels: True
                    anim: True
                    bg_color: 106/255, 188/255, 206/255, 1
                    #lines_color: [40/255, 107/255, 122/255, 1]
                    line_width:dp(1)
                    #bars_color: [40/255, 107/255, 122/255, 1]
                    #labels_color: 40/255, 107/255, 122/255, 1
                    trim: True
                    #on_select: root.set_text(args)
                    
                Barras_ano:
                    id: id_barano
                    labels: True
                    anim: True
                    bg_color: 106/255, 188/255, 206/255, 1
                    #lines_color: [40/255, 107/255, 122/255, 1]
                    line_width:dp(1)
                    #bars_color: [40/255, 107/255, 122/255, 1]
                    labels_color: 40/255, 107/255, 122/255, 1
                    trim: True
                    #on_select: root.set_text(args)
                    
                MDLabel:
                    text: '% del ahorro objetivo:'
                    halign: "center"
                    valign: "center"
                    
                AKCircularProgress_ahorro:
                    id: progress_percent
                    pos_hint: {"center_x": .5, "center_y": .5}
                    size_hint: None, None
                    size: dp(100), dp(100)
                    circle_color: 106/255, 188/255, 206/255, 1
                    percent_color: 106/255, 188/255, 206/255, 1
                    background_circle_color:106/255, 188/255, 206/255, 1
                    percent_type: "percent"
                    start_deg: 180
                    end_deg: 540
                MDLabel:
                    text: 'Ahorro mensual a realizar:'
                    halign: "center"
                    valign: "center"
                MDLabel:
                    id:ahorro_mensual_obj
                    halign: "center"
                    valign: "center"
                MDLabel:
                    text: 'Gasto fijo en domiciliaciones al mes:'
                    halign: "center"
                    valign: "center"
                MDLabel:
                    id:domiciliaciones_mes
                    halign: "center"
                    valign: "center"
                MDLabel:
                    text: '% ingresos de cada etapa:'
                    halign: "center"
                    valign: "center"
                MDBoxLayout:
                    id: chart_box_etapaimporte
                    adaptive_height: True
                    padding:dp(24)
                    orientation: "vertical"
                MDLabel:
                    text: '% tiempo de cada etapa:'
                    halign: "center"
                    valign: "center"
                MDBoxLayout:
                    id: chart_box_etapatiempo
                    adaptive_height: True
                    padding:dp(24)
                    orientation: "vertical"
                MDLabel:
                    text: 'Ranking gastos:'
                    halign: "center"
                    valign: "center"    
                Barras_horizontal:
                    id: id_ranking_gastos
                    labels: True
                    anim: True
                    bg_color: 106/255, 188/255, 206/255, 1
                    #lines_color: [40/255, 107/255, 122/255, 1]
                    line_width:dp(1)
                    bars_color: 112/255, 196/255, 215/255, 1
                    labels_color: 0,0,0, 1
                    trim: True
                    #on_select: root.set_text(args)
                MDLabel:
                    text: 'Ranking ingresos:'
                    halign: "center"
                    valign: "center"    
                Barras_horizontal:
                    id: id_ranking_ingresos
                    labels: True
                    anim: True
                    bg_color: 106/255, 188/255, 206/255, 1
                    #lines_color: [40/255, 107/255, 122/255, 1]
                    line_width:dp(1)
                    bars_color: 112/255, 196/255, 215/255, 1
                    labels_color: 0,0,0, 1
                    trim: True
                    #on_select: root.set_text(args)
                MDRaisedButton:
                    md_bg_color: 143/255, 219/255, 236/255, 1
                    text: "Tabla Tasa de ahorro"
                    on_release: root.tabla_tasa_ahorro()

        MDBoxLayout:
            size_hint_y: 0.05
            MDRaisedButton:
                
                md_bg_color: 143/255, 219/255, 236/255, 1
                text: "Etapa"
                on_release: root.choose_etapa()
                
            MDRaisedButton:
                md_bg_color: 143/255, 219/255, 236/255, 1
                text: "Categoría"
                on_release: root.choose_categoria()
                
            MDRaisedButton:
                md_bg_color: 143/255, 219/255, 236/255, 1
                text: "Fecha"
                on_release: root.choose_fecha()
            MDRaisedButton:
                md_bg_color: 143/255, 219/255, 236/255, 1
                text: "Actualizar"
                on_release: root.update()

<Selectionlist_etapa>:
    size_hint: None, None
    size:
        (dp(302), dp(450)) \
        if root.theme_cls.device_orientation == "portrait" \
        else (dp(450), dp(350))
    BoxLayout:
        orientation: "vertical"
        canvas.before:
            Color:
                rgba: root.theme_cls.bg_normal
            RoundedRectangle:
                size: self.size
                pos: self.pos
        BoxLayout:
            orientation:"vertical"
            size_hint_y: .1
            height: dp(500)
            canvas.before:
                Color:
                    rgba: root.theme_cls.primary_color
                RoundedRectangle:
                    size: self.size
                    pos: self.pos
                    radius:[(10.0, 10.0), (10.0, 10.0), (0, 0), (0, 0)]
            MDLabeltitle2:
                
                text:'Seleccionar Etapa'
        BoxLayout:
            orientation:"vertical"
            size_hint_y: .9
            height: dp(500)
            canvas.before:
                Color:
                    #rgba: root.theme_cls.primary_color
                RoundedRectangle:
                    size: self.size
                    pos: self.pos
                    radius:[(10.0, 10.0), (10.0, 10.0), (0, 0), (0, 0)]
            
            ScrollView:    
                AKSelectList_etapa:
                    id: selectionlist
            BoxLayout:
                size_hint_y: None
                height: dp(40)
                padding: [dp(10), 0]
                spacing: dp(10)
                canvas.before:
                    Color:
                        rgba: root.theme_cls.bg_dark
                    RoundedRectangle:
                        size: self.size
                        pos: self.pos
                        radius: [(0.0, 10.0), (0.0, 10.0), (10, 10), (10, 10)]
                MDFlatButton:
                    text: "Cancelar"
                    pos_hint: {"center_x": .5, "center_y": .5}
                    on_release: root.cancel()
                MDFlatButton:
                    text: "Limpiar"
                    pos_hint: {"center_x": .5, "center_y": .5}
                    on_release: root._unselect()
                MDFlatButton:
                    text: "Seleccionar"
                    pos_hint: {"center_x": .5, "center_y": .5}
                    on_release: root._choose()
            
<Selectionlist_categoria>:
    size_hint: None, None
    size:
        (dp(302), dp(450)) \
        if root.theme_cls.device_orientation == "portrait" \
        else (dp(450), dp(350))
    BoxLayout:
        orientation: "vertical"
        canvas.before:
            Color:
                rgba: root.theme_cls.bg_normal
            RoundedRectangle:
                size: self.size
                pos: self.pos
        BoxLayout:
            orientation:"vertical"
            size_hint_y: .1
            height: dp(500)
            canvas.before:
                Color:
                    rgba: root.theme_cls.primary_color
                RoundedRectangle:
                    size: self.size
                    pos: self.pos
                    radius:[(10.0, 10.0), (10.0, 10.0), (0, 0), (0, 0)]
            MDLabeltitle2:
                
                text:'Seleccionar Categoría'
        BoxLayout:
            orientation:"vertical"
            size_hint_y: .9
            height: dp(500)
            canvas.before:
                Color:
                    #rgba: root.theme_cls.primary_color
                RoundedRectangle:
                    size: self.size
                    pos: self.pos
                    radius:[(10.0, 10.0), (10.0, 10.0), (0, 0), (0, 0)]
            
            ScrollView:    
                AKSelectList_etapa:
                    id: selectionlist_categoria
            BoxLayout:
                size_hint_y: None
                height: dp(40)
                padding: [dp(10), 0]
                spacing: dp(10)
                canvas.before:
                    Color:
                        rgba: root.theme_cls.bg_dark
                    RoundedRectangle:
                        size: self.size
                        pos: self.pos
                        radius: [(0.0, 10.0), (0.0, 10.0), (10, 10), (10, 10)]
                MDFlatButton:
                    text: "Cancelar"
                    pos_hint: {"center_x": .5, "center_y": .5}
                    on_release: root.cancel()
                MDFlatButton:
                    text: "Seleccionar"
                    pos_hint: {"center_x": .5, "center_y": .5}
                    on_release: root._choose()

"""
)
