from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen
from kivymd.uix.list import MDList, OneLineListItem

from kivymd_extensions.akivymd.uix.behaviors.addwidget import (
    AKAddWidgetAnimationBehavior,
)

Builder.load_string(
    """
<Selectdb>:

    MDBoxLayout:
        orientation: "vertical"

        MyToolbar:
            id: _toolbar

        ScrollView:

            AnimatedBox:
                id: list
                transition: "fade_size"
"""
)


class AnimatedBox(MDList, AKAddWidgetAnimationBehavior):
    pass


class Selectdb(Screen):
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
        pass

    def goto_deporte(self, *args):
        pass

    def goto_vblesglobales(self, *args):
        pass
