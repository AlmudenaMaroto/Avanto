from kivy.lang.builder import Builder
from kivymd.uix.screen import MDScreen
import sqlite3
import os
from datetime import datetime
import time
from calendar import timegm
import charts_almu
import datetime


def epoch2human(epoch):
    return time.strftime('%m/%y',
                         time.localtime(int(epoch)))


class Economia(MDScreen):
    def __init__(self, **kwargs):
        super(Economia, self).__init__()
        self.path_app = os.getcwd()
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
                dict_eco.append(row_i)
                row_i = {}

            except ValueError:
                pass
        con.close()
        dict_eco_sorted = sorted(dict_eco, key=lambda d: d['epoch'], reverse=False)

        # Para no petar el grafico, cogemos menos valores
        maximo_saldo = max(dict_eco_sorted, key=lambda x: x['saldo']).get('saldo')
        minimo_saldo = min(dict_eco_sorted, key=lambda x: x['saldo']).get('saldo')
        max_epoch = max(dict_eco_sorted, key=lambda x: x['epoch']).get('epoch')
        min_epoch = min(dict_eco_sorted, key=lambda x: x['epoch']).get('epoch')

        eje_y_max = round(maximo_saldo, -3) + 1000
        eje_y_min = round(minimo_saldo, -3)

        num_saltos = 5
        label_x_paso = []
        label_y_paso = []
        for i in range(num_saltos):
            paso_y = (eje_y_max - eje_y_min) / num_saltos
            paso_x = (max_epoch - min_epoch) / num_saltos
            label_x_paso.append(min_epoch + i * paso_x)
            label_y_paso.append(eje_y_min + i * paso_y)
        label_x_paso = [epoch2human(t) for t in label_x_paso]

        self.ids.chart1.x_values = [d['epoch'] for d in dict_eco_sorted if 'epoch' in d]
        self.ids.chart1.x_labels = label_x_paso
        self.ids.chart1.y_values = [d['saldo'] for d in dict_eco_sorted if 'saldo' in d]
        self.ids.chart1.y_labels = label_y_paso

        # Cuenta actual
        self.ids.saldo_total.text = str(dict_eco_sorted[-1].get('saldo')) + ' €'
        a ='end'

    def set_text(self, args):
        self.ids._label.text = f"{args[1]} [{args[2]},{args[3]}]"

    def update(self):
        pass

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
    
<MyAKLineChart_Almu@AKLineChart_Almu>
    size_hint_y: None
    height: dp(180)
    x_values: [0, 5, 8, 15]
    y_values: [0, 10, 6, 8]
    label_size: dp(12)

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
                    id: chart1
                    labels: True
                    anim: True
                    circles: False
                    bg_color: 106/255, 188/255, 206/255, 1
                    on_select: root.set_text(args)
                    line_width:dp(1)
                    
                MyAKLineChart_Almu:
                    id: chart2
                    labels: False
                    anim: True
                    on_select: root.set_text(args)

                MyAKLineChart_Almu:
                    id: chart3
                    labels: True
                    anim: True
                    lines: False
                    on_select: root.set_text(args)

        MDFloatLayout:
            size_hint_y: 0.05
            MDRaisedButton:
                
                md_bg_color: 143/255, 219/255, 236/255, 1
                text: "Etapa"
                on_release: root.choose_etapa()
                
            MDRaisedButton:
                pos_hint: {"center_x": .5}
                md_bg_color: 143/255, 219/255, 236/255, 1
                text: "Categoría"
                on_release: root.choose_categoria()
                
            MDRaisedButton:
                pos_hint: {"center_x": .87}
                md_bg_color: 143/255, 219/255, 236/255, 1
                text: "Fecha"
                on_release: root.choose_fecha()

            MDLabel:
                id: _label
                halign: "center"
                valign: "center"

"""
)
