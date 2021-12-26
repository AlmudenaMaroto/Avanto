from kivy.lang.builder import Builder
from kivymd.uix.screen import MDScreen
import sqlite3
import os
from datetime import datetime
import time
from calendar import timegm


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
        saldo = 0

        con = sqlite3.connect(self.path_app + '/movimientos.db')
        cursor = con.cursor()
        orden_execute = 'select * from movimientos ORDER BY ID ASC'
        cursor.execute(orden_execute)
        for i in cursor:
            saldo = saldo + i[4]
            if i[0] % 5 == 0:
                try:
                    utc_time = time.strptime(i[1], "%d/%m/%Y")
                    epoch_time = timegm(utc_time)
                    fechas.append(i[1])
                    epochs.append(epoch_time)
                    importes.append(i[4])
                    saldos.append(saldo)
                except ValueError:
                    pass
        con.close()
        # Para no petar el grafico, cogemos solo 30 valores.

        self.ids.chart1.x_values = epochs
        self.ids.chart1.x_labels = fechas
        self.ids.chart1.y_values = saldos
        # self.ids.chart1.y_labels = saldos


    def set_text(self, args):
        self.ids._label.text = f"{args[1]} [{args[2]},{args[3]}]"

    def update(self):
        chart1 = self.ids.chart1
        chart1.x_values = [2, 8, 12, 35, 40, 43, 56]
        chart1.y_values = [3, 2, 1, 16, 0, 1, 10]
        chart1.update()

        chart2 = self.ids.chart2
        chart2.x_values = [2, 8, 12, 35, 40, 43, 56]
        chart2.y_values = [3, 2, 1, 15, 0, 1, 10]
        chart2.update()

        chart3 = self.ids.chart3
        chart3.x_values = [2, 8, 12, 35, 40, 43, 56]
        chart3.y_values = [3, 2, 1, 15, 0, 1, 10]
        chart3.update()

        chart4 = self.ids.chart4
        chart4.x_labels = ["XYZ", "Second", "Third", "Last"]
        chart4.y_labels = ["XYZ", "Second", "Third", "Last"]
        chart4.update()

    def choose_etapa(self):
        pass

    def choose_categoria(self):
        pass

    def choose_fecha(self):
        pass


Builder.load_string(
    """
<Evolucion_temporal@AKLineChart>
    size_hint_y: None
    height: dp(180)
    x_values: []
    y_values: []
    label_size: dp(12)
    
<MyAKLineChart@AKLineChart>
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
                    labels: False
                    anim: True
                    #bg_color: 0.6, 0, 0, 1
                    #circles_color: [0.4, 0.4, 1, 1]
                    circles: False
                    labels: False
                    on_select: root.set_text(args)
                    line_width:dp(1)

                MyAKLineChart:
                    id: chart2
                    labels: False
                    anim: True
                    on_select: root.set_text(args)

                MyAKLineChart:
                    id: chart3
                    labels: True
                    anim: True
                    lines: False
                    on_select: root.set_text(args)

                MyAKLineChart:
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
