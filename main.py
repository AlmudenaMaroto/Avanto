import ast
import sys
from os import path
import os
import sqlite3
from kivy.utils import platform

# Marron para alimentos: #d47100
# Rojo para deporte:#d40700


# Esto cuando se me jodio la grafica, ya funciona
# if platform != 'android':
#     os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'

from kivy.config import Config

# Pantalla:
Config.set("graphics", "width", "340")
Config.set("graphics", "hight", "640")

sys.path.append(path.join(path.abspath(__file__).rsplit("examples", 1)[0]))
from kivy.factory import Factory  # noqa
from kivy.lang import Builder  # noqa
from kivy.properties import StringProperty  # noqa
from kivymd.app import MDApp  # noqa
from kivymd.uix.list import OneLineAvatarListItem  # noqa
from kivymd.uix.toolbar import MDToolbar  # noqa
from kivy.uix.screenmanager import ScreenManager, Screen
from tools.cardstack_choosetable import AKCardStack

from kivymd_extensions.akivymd.uix.statusbarcolor import (  # noqa
    change_statusbar_color,
)
import csv


# Funciones de creacion de tablas. Si ya estan creadas, no se vuelven a crear.
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


def create_table_tabladeporte(cursor):
    cursor.execute(
        '''
        CREATE TABLE tabladeporte(
        ID        INT   PRIMARY KEY NOT NULL,
        Concepto     TEXT               NOT NULL,
        kcal     INT              NOT NULL,
        Cardio     INT              NOT NULL,
        Brazo     INT              NOT NULL,
        Pecho     INT              NOT NULL,
        Espalda     INT              NOT NULL,
        Pierna       INT               NOT NULL
        )'''
    )
    # Generamos unos registros iniciales:
    ruta_excel = os.getcwd() + "/files/tabladeporte.csv"
    with open(ruta_excel, 'r', newline='', encoding='latin') as f:
        reader = csv.reader(f, delimiter=';')
        lineas = list(reader)
    salto_primera = 0
    for linea_i in lineas:
        if salto_primera:
            a1 = (linea_i[0], linea_i[1], linea_i[2], linea_i[3], linea_i[4], linea_i[5], linea_i[6], linea_i[7])
            s1 = 'INSERT INTO tabladeporte(ID, Concepto, kcal, Cardio, Brazo, Pecho, Espalda, Pierna)'
            s2 = 'VALUES(%s,"%s",%s,%s,%s,%s,%s,%s )' % a1
            try:
                cursor.execute(s1 + ' ' + s2)
            except Exception as e:
                pass
        salto_primera = 1


def create_table_inventario(cursor):
    cursor.execute(
        '''
        CREATE TABLE inventario(
        ID        INT   PRIMARY KEY NOT NULL,
        Concepto     TEXT               NOT NULL,
        Cantidad     INT              NOT NULL,
        Lista       INT               NOT NULL
        )'''
    )
    # Generamos unos registros iniciales:
    lista_inventario_inicial = ['Aceite', 'Aceitunas', 'Arroz redondo', 'Arroz largo', 'Atún', 'Azúcar', 'Berberechos',
                                'Café', 'Calamares', 'Champiñones', 'Espárragos', 'Fabada', 'Garbanzos bote',
                                'Garbanzos secos', 'Galletas', 'Guisantes', 'Harina Normal', 'Harina Bizcochona',
                                'Harina Pizza', 'Harina Fuerza', 'Harina Rebozar', 'Judías Verdes',
                                'Judías Blancas Bote', 'Judías Blancas Secas', 'Judías Pintas Bote',
                                'Judías Pintas Secas', 'Leche Desnatada', 'Leche Sin Lactosa', 'Leche Condensada',
                                'Lentejas Bote', 'Lentejas Secas', 'Maíz', 'Mayonesa', 'Melocotón', 'Mejillones',
                                'Mermelada', 'Macarrones', 'Fideos', 'Espaguetis', 'Lasaña', 'Lluvia', 'Colores',
                                'Pimientos Piquillo', 'Pimientos Morrón', 'Pisto', 'Piña', 'Tomate Crudo',
                                'Tomate Frito', 'Latas Variadas', 'Remolacha', 'Sardinillas', 'Sal']
    id = 1
    for alimento in lista_inventario_inicial:
        a1 = (id, alimento, 0, 1)
        s1 = 'INSERT INTO inventario(ID,	Concepto,	Cantidad, Lista)'
        s2 = 'VALUES(%s,"%s","%s","%s")' % a1
        id = id + 1
        try:
            cursor.execute(s1 + ' ' + s2)
        except Exception as e:
            pass


def create_table_vbles_globales(cursor):
    cursor.execute(
        '''
        CREATE TABLE globales(
        ID        INT   PRIMARY KEY NOT NULL,
        Obj_cuenta           FLOAT,
        Obj_fecha           TEXT,
        Obj_peso             FLOAT,
        Domiciliaciones      TEXT,
        Ingresos TEXT,
        Obj_tasa FLOAT
        )''')

    cursor.execute(
        '''INSERT INTO globales (ID, Obj_cuenta, Obj_fecha, Obj_peso, Domiciliaciones, Ingresos, Obj_tasa) VALUES (1,25000,'01/09/2022',60,'Abono, Spotify, Orange', 'Salario, Beca Erasmus, Fianza',80)'''
    )


# De forma inicial, creamos las tablas. Añadir nuevas tablas aqui!!
ruta_APP_PATH = os.getcwd()
ruta_DB_PATH_movimientos = ruta_APP_PATH + '/movimientos.db'
ruta_DB_PATH_deporte = ruta_APP_PATH + '/deporte.db'
ruta_DB_PATH_tabladeporte = ruta_APP_PATH + '/tabladeporte.db'
ruta_DB_PATH_inventario = ruta_APP_PATH + '/inventario.db'
ruta_DB_PATH_vblesglobales = ruta_APP_PATH + '/globales.db'

try:
    con = sqlite3.connect(ruta_DB_PATH_movimientos)
    cursor = con.cursor()
    create_table_movimientos(cursor)
    con.commit()
    con.close()
except Exception as e:
    pass
    # print(e)
try:
    con = sqlite3.connect(ruta_DB_PATH_deporte)
    cursor = con.cursor()
    create_table_deporte(cursor)
    con.commit()
    con.close()
except Exception as e:
    pass
    # print(e)
try:
    con = sqlite3.connect(ruta_DB_PATH_tabladeporte)
    cursor = con.cursor()
    create_table_tabladeporte(cursor)
    con.commit()
    con.close()
except Exception as e:
    pass
    # print(e)
try:
    con = sqlite3.connect(ruta_DB_PATH_inventario)
    cursor = con.cursor()
    create_table_inventario(cursor)
    con.commit()
    con.close()
except Exception as e:
    pass
    # print(e)

try:
    con = sqlite3.connect(ruta_DB_PATH_vblesglobales)
    cursor = con.cursor()
    create_table_vbles_globales(cursor)
    con.commit()
    con.close()
except Exception as e:
    pass
    # print(e)


class IconListItem(OneLineAvatarListItem):
    icon = StringProperty()


class DemoApp(MDApp):
    intro = """\n

    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls.primary_palette = "Cyan"
        self.theme_cls.primary_hue = "800"
        # Elegir entre
        # "Cyan": {
        #     "50": "E0F7FA",
        #     "100": "B2EBF2",
        #     "200": "80DEEA",
        #     "300": "4DD0E1",
        #     "400": "26C6DA",
        #     "500": "00BCD4",
        #     "600": "00ACC1",
        #     "700": "0097A7",
        #     "800": "00838F",
        #     "900": "006064",
        #     "A100": "84FFFF",
        #     "A200": "18FFFF",
        #     "A400": "00E5FF",
        #     "A700": "00B8D4",
        self.title = "              Avanto"
        change_statusbar_color(self.theme_cls.primary_color)

    def build(self):
        self.root = Builder.load_string(kv)

    def on_start(self):
        if platform == 'android':
            from jnius import autoclass

            PythonActivity = autoclass("org.kivy.android.PythonActivity")
            ActivityInfo = autoclass("android.content.pm.ActivityInfo")
            activity = PythonActivity.mActivity
            # set orientation according to user's preference
            activity.setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_USER)
        with open(
                path.join(path.dirname(__file__), "screens.json"), encoding='utf-8'
        ) as read_file:
            self.data_screens = ast.literal_eval(read_file.read())
            data_screens = list(self.data_screens.keys())
            data_screens.sort()
        # ocultamos las pantallas que no queramos ver con la variable menu del screens.json
        for list_item in data_screens:
            if self.data_screens[list_item]["menu"] == "si":
                self.root.ids.menu_list.add_widget(
                    IconListItem(
                        text=list_item,
                        icon=self.data_screens[list_item]["icon"],
                        on_release=lambda x=list_item: self.load_screen(x),
                    )
                )

    def load_screen(self, screen_name):
        manager = self.root.ids.screen_manager
        screen_details = self.data_screens[screen_name.text]

        if not manager.has_screen(screen_details["screen_name"]):
            exec("from screens import %s" % screen_details["import"])
            screen_object = eval("Factory.%s()" % screen_details["factory"])
            screen_object.name = screen_details["screen_name"]
            manager.add_widget(screen_object)

            if "_toolbar" in screen_object.ids:
                screen_object.ids._toolbar.title = screen_name.text

        self.root.ids.navdrawer.set_state("close")
        self.show_screen(screen_details["screen_name"])

    def show_screen(self, name, mode=""):
        if mode == "back":
            self.root.ids.screen_manager.transition.direction = "right"
        else:
            self.root.ids.screen_manager.transition.direction = "left"
        self.root.ids.screen_manager.current = name
        return True


kv = """
#: import StiffScrollEffect kivymd.effects.stiffscroll.StiffScrollEffect

<IconListItem@OneLineAvatarListItem>:

    IconLeftWidget:
        icon: root.icon

<MyToolbar@MDToolbar>:
    elevation: 10
    left_action_items: [["arrow-left", lambda x: app.show_screen("Home", "back")]]


MDScreen:

    ScreenManager:
        id: screen_manager

        MDScreen:
            name: "Home"

            Image:
                source: "assets/logo.png"
                opacity: .3
                size_hint_x: 1
                allow_stretch: True

            MDBoxLayout:
                orientation: "vertical"

                MyToolbar:
                    title: app.title
                    left_action_items:[["menu" , lambda x: navdrawer.set_state("open")]]

                BoxLayout:
                    padding:dp(20)

                    MDLabel:
                        text: app.intro
                        theme_text_color: "Primary"
                        halign: "left"

    MDNavigationDrawer:
        id: navdrawer

        ScrollView:
            # effect_cls: StiffScrollEffect
            MDBoxLayout:
                orientation: "vertical"
                adaptive_height: True

                MDRelativeLayout:
                    size_hint_y: None
                    height: title_box.height

                    FitImage:
                        source: "assets/texture_blur.png"

                    MDBoxLayout:
                        id: title_box
                        adaptive_height: True
                        padding: dp(24)

                        MDLabel:
                            text: "Menú"
                            font_style: "H5"
                            size_hint_y: None
                            height: self.texture_size[1]
                            shorten: True

                MDList:
                    id: menu_list
"""

if __name__ == '__main__':
    DemoApp().run()
