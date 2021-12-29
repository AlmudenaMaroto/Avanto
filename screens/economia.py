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
import datetime
from itertools import groupby
from datetime import date
from kivy.uix.popup import Popup

today = date.today()


def epoch2human(epoch):
    return time.strftime('%m/%y',
                         time.localtime(int(epoch)))


def epoch2human_year(epoch):
    return time.strftime('%Y',
                         time.localtime(int(epoch)))


def filtrar_dict_fechas(dic, epoch_ini, epoch_fin):
    return (dic['epoch'] > epoch_ini and dic['epoch'] < epoch_fin)


def filtrar_ingresos(dic):
    return dic['importe'] > 0


def filtrar_gastos(dic):
    return dic['importe'] < 0


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
            self.obj_tasa = i[5]
        con.close()
        self.calculos()
        self.barchart_datos()
        self.barchart_ano()
        self.calc_ahorros()

        id_evtemp = self.ids.id_evtemp
        id_barmes = self.ids.id_barmes
        id_barano = self.ids.id_barano
        id_evtemp.update()
        id_barmes.update()
        id_barano.update()

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
        for i in cursor:
            saldo = round(saldo + i[4], 2)
            try:
                utc_time = time.strptime(i[1], "%d/%m/%Y")
                epoch_time = timegm(utc_time)
                ano_mes = datetime.datetime.strptime(str(i[1]), '%d/%m/%Y').strftime('%m/%y')
                # Agrupamos en un diccionario para cada linea, para poder ordenarlo
                row_i['fecha'] = str(i[1])
                row_i['anomes'] = ano_mes
                row_i['epoch'] = epoch_time
                row_i['importe'] = i[4]
                row_i['saldo'] = saldo
                row_i['concepto'] = i[2]
                row_i['categoria'] = i[3]
                row_i['etapa'] = i[5]
                row_i['ubicacion'] = i[6]
                dict_eco.append(row_i)
                row_i = {}

            except ValueError:
                pass
        con.close()

        self.dict_eco_sorted = sorted(dict_eco, key=lambda d: d['epoch'], reverse=False)

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
        self.saldo_total = self.dict_eco_sorted[-1].get('saldo')
        self.ids.saldo_total.text = str(self.saldo_total) + ' €'

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
        num_saltos = 4
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
        self.ids.ahorro_mensual_obj.text = str(round((self.obj_cuenta - self.saldo_total) * 30 / (diff_fechas))) + ' €'
        # Gasto en domiciliaciones al mes (ultimos 30 dias)
        domiciliaciones_list = self.domiciliaciones.replace(' ', '').split(',')
        epoch_fin = datetime.datetime.strptime(today.strftime("%d/%m/%Y"), '%d/%m/%Y').timestamp()
        epoch_ini = (datetime.datetime.strptime(today.strftime("%d/%m/%Y"), '%d/%m/%Y') - datetime.timedelta(
            days=30)).timestamp()
        dict_domic = list(filter(lambda d: d['categoria'] in domiciliaciones_list, self.dict_eco_sorted))
        dict_domic_fech = [d for d in dict_domic if filtrar_dict_fechas(d, epoch_ini, epoch_fin)]
        self.ids.domiciliaciones_mes.text = str(-round(sum(item['importe'] for item in dict_domic_fech), 2)) + ' €'
        A = 'STOP'

    def tasa_ahorro_tabla(self):
        tabla1 = MDDataTable(column_data = [("Col 1", dp(30)), ("Col 2", dp(30)), ("Col 3", dp(30))])

    def choose_etapa(self):
        pass

    def choose_categoria(self):
        pass

    def choose_fecha(self):
        pass


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
                    lines_color: [40/255, 107/255, 122/255, 1]
                    line_width:dp(1)
                    bars_color: [40/255, 107/255, 122/255, 1]
                    labels_color: 40/255, 107/255, 122/255, 1
                    trim: True
                    #on_select: root.set_text(args)
                    
                Barras_ano:
                    id: id_barano
                    labels: True
                    anim: True
                    bg_color: 106/255, 188/255, 206/255, 1
                    lines_color: [40/255, 107/255, 122/255, 1]
                    line_width:dp(1)
                    bars_color: [40/255, 107/255, 122/255, 1]
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

            MDLabel:
                id: _label
                halign: "center"
                valign: "center"

"""
)
