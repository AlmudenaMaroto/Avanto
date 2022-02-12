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
from tools.tasa_ahorro import Tabla_tasa_ahorro
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


class Ejercicio(MDScreen):
    def __init__(self, **kwargs):
        super(Ejercicio, self).__init__()


Builder.load_string(
    """
<Ejercicio>
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
                    text:"Ejercicio"

"""
)
