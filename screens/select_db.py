from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen
from kivymd.uix.list import MDList, OneLineListItem

from kivymd_extensions.akivymd.uix.behaviors.addwidget import (
    AKAddWidgetAnimationBehavior,
)
from main import DemoApp
from kivymd.uix.screen import MDScreen
from kivy.uix.screenmanager import ScreenManager, Screen


class AnimatedBox(MDList, AKAddWidgetAnimationBehavior):
    pass


class WindowManager_select(ScreenManager):

    def load_movimientos(self, screen_name):
        self.clear_widgets()
        self.current = screen_name
        self.add_widget(DataBaseWid_movimientos())


class DataBaseWid_movimientos(MDScreen):

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


class Selectdb(MDScreen):
    # def __init__(self, **kwargs):
    #     super().__init__()
    #     self.WindowManager_select = WindowManager_select

    def on_enter(self):
        self.update()

    def update(self, *args):
        items = []
        # Añadimos todas las Bases de Datos que vamos a emplear a la lista
        items.append(OneLineListItem(text=f"movimientos", on_release=self.goto_movimientos))
        items.append(OneLineListItem(text=f"deporte", on_release=self.goto_deporte))
        items.append(OneLineListItem(text=f"variables globales", on_release=self.goto_vblesglobales))
        self.ids.list.items = items

    def on_leave(self):
        self.ids.list.clear_widgets()

    def goto_movimientos(self, *args):
        WindowManager_select.load_movimientos(self, 'db_movimientos')

    def goto_deporte(self, *args):
        pass

    def goto_vblesglobales(self, *args):
        pass


Builder.load_string(
    """
WindowManager_select:
    db_movimientos:
    selectdb:

<Selectdb>:
    name:"selectdb"
    MDBoxLayout:
        orientation: "vertical"

        MyToolbar:
            id: _toolbar

        ScrollView:

            AnimatedBox:
                id: list
                transition: "fade_size"

<DataBaseWid_movimientos>:
    name:"db_movimientos"
    MDBoxLayout:
        orientation: "vertical"

        MyToolbar:
            id: _toolbar
        MDBoxLayout:
            size_hint_y: 0.1
            MDFillRoundFlatButton: # -----------Go back
                font_size: self.height*0.45
                text: 'Atrás'
                on_press: root.return_button()
            MDFillRoundFlatButton: # -----------Add 10 rows
                font_size: self.height*0.45
                text: 'Añadir 10 filas'
                on_press: root.add_10_more()
            MDFillRoundFlatButton: # ---------Add
                font_size: self.height*0.45
                text: '+'
                on_press: root.create_new_product()
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

"""
)
