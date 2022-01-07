import ast
import sys
from os import path
import os
import sqlite3
from kivy.utils import platform

# Permisos de acceso a las carpetas del movil para poder importar y exportar
if platform == 'android':
    from android.permissions import request_permissions, Permission
    # from jnius import autoclass
    #
    # PythonActivity = autoclass("org.kivy.android.PythonActivity")
    # ActivityInfo = autoclass("android.content.pm.ActivityInfo")
    # activity = PythonActivity.mActivity
    # # set orientation according to user's preference
    # activity.setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_USER)

    request_permissions([Permission.WRITE_EXTERNAL_STORAGE])
# Esto cuando se me jodio la grafica, ya funciona
if platform != 'android':
    pass
    # os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'

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

from kivymd_extensions.akivymd.uix.statusbarcolor import (  # noqa
    change_statusbar_color,
)

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
        '''INSERT INTO globales (ID, Obj_cuenta, Obj_fecha, Obj_peso, Domiciliaciones, Ingresos, Obj_tasa) VALUES (1,25000,'01/09/2022',60,'Abono, Spotify, Orange', 'SALARIO',80)'''
    )


# De forma inicial, creamos las tablas. Añadir nuevas tablas aqui!!
ruta_APP_PATH = os.getcwd()
ruta_DB_PATH_movimientos = ruta_APP_PATH + '/movimientos.db'
ruta_DB_PATH_deporte = ruta_APP_PATH + '/deporte.db'
ruta_DB_PATH_vblesglobales = ruta_APP_PATH + '/globales.db'

try:
    con = sqlite3.connect(ruta_DB_PATH_movimientos)
    cursor = con.cursor()
    create_table_movimientos(cursor)
    con.commit()
    con.close()
except Exception as e:
    print(e)
try:
    con = sqlite3.connect(ruta_DB_PATH_deporte)
    cursor = con.cursor()
    create_table_deporte(cursor)
    con.commit()
    con.close()
except Exception as e:
    print(e)
try:
    con = sqlite3.connect(ruta_DB_PATH_vblesglobales)
    cursor = con.cursor()
    create_table_vbles_globales(cursor)
    con.commit()
    con.close()
except Exception as e:
    print(e)


class IconListItem(OneLineAvatarListItem):
    icon = StringProperty()


class DemoApp(MDApp):
    intro = """\n\n\n\n¡Bienvenid@ a Avanto! \n\n\n\n\n\n\n
        Para empezar a añadir registros, haz click en "Seleccionar Tabla".
        Hay varias tablas en las que registrar diferente información.
        Para hacer una importación masiva haz click en "Importar/Exportar" 
        El formato debe ser el adecuado.
        También puedes exportar los datos guardados en un csv para no perderlos. 
        Para todo lo demás, las pestañas de análisis.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls.primary_palette = "Cyan"
        self.title = "              Avanto"
        change_statusbar_color(self.theme_cls.primary_color)

    def build(self):
        self.root = Builder.load_string(kv)

    def on_start(self):
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
