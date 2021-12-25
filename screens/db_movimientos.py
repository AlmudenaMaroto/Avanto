from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen
from kivymd.uix.list import MDList, OneLineListItem

from kivymd_extensions.akivymd.uix.behaviors.addwidget import (
    AKAddWidgetAnimationBehavior,
)

Builder.load_string(
    """
<DataBaseWid_movimientos>:
    id:db_movimientos
    MDBoxLayout:
        orientation: "vertical"

        MyToolbar:
            id: _toolbar
        BoxLayout:
            size_hint_y: 0.1
            Button: # -----------Go back
                font_size: self.height*0.25
                text: 'Atrás'
                pos: 1, 1
                size: 10, 50
                on_press: root.return_button()
            Button: # -----------Add 10 rows
                font_size: self.height*0.25
                text: 'Añadir 10 filas'
                pos: 1, 1
                size: 10, 50
                on_press: root.add_10_more()
            Button: # ---------Add
                font_size: self.height*0.6
                text: '+'
                pos: 1, 1
                size: 10, 50
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


class AnimatedBox(MDList, AKAddWidgetAnimationBehavior):
    pass


class DataBaseWid_movimientos(Screen):
    pass
