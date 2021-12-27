from kivy.lang.builder import Builder
from kivymd.uix.screen import MDScreen
import sqlite3
import os
from datetime import datetime
import time
from calendar import timegm
import charts_almu
import datetime

class Economia(MDScreen):
    def __init__(self, **kwargs):
        super(Economia, self).__init__()
        self.path_app = os.getcwd()

        # Linea temporal:
        con = sqlite3.connect(self.path_app + '/movimientos.db')
        cursor = con.cursor()
        orden_execute = 'select * from movimientos'
        cursor.execute(orden_execute)
        longitud = len(cursor.fetchall())
        con.close()
        fechas = []
        epochs = []
        importes = []
        saldos = []
        saldos_str = []
        saldo = 0

        con = sqlite3.connect(self.path_app + '/movimientos.db')
        cursor = con.cursor()
        orden_execute = 'select * from movimientos ORDER BY ID ASC'
        cursor.execute(orden_execute)
        for i in cursor:
            saldo = round(saldo + i[4], 2)
            if i[0] % 20 == 0:
                try:
                    utc_time = time.strptime(i[1], "%d/%m/%Y")
                    epoch_time = timegm(utc_time)
                    if i[0] % 50 == 0:
                        # Ponemos solo la fecha de año/mes
                        ano_mes = datetime.datetime.strptime(str(i[1]), '%d/%m/%Y').strftime('%m/%y')
                        fechas.append(ano_mes)
                        saldos_str.append(str(saldo))
                    else:
                        fechas.append('')
                        saldos_str.append('')
                    epochs.append(epoch_time)
                    importes.append(i[4])
                    saldos.append(saldo)
                except ValueError:
                    pass
        con.close()
        # Para no petar el grafico, cogemos menos valores
        maximo_saldo = max(saldos)
        minimo_saldo = min(saldos)
        max_epoch = max(epochs)
        min_epoch = min(epochs)
        for i in range(5):
            pass


        self.ids.chart1.x_values = epochs
        self.ids.chart1.x_labels = fechas
        self.ids.chart1.y_values = saldos
        self.ids.chart1.y_labels = saldos_str

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

                MyAKLineChart_Almu:
                    id: chart4
                    labels: True
                    anim: True
                    lines: False
                    x_labels: ["XYZ", "Second", "Third", "Last"]
                    y_labels: ["XYZ", "Second", "Third", "Last"]
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
