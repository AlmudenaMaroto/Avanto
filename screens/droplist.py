from kivy.lang import Builder
from kivy.properties import StringProperty
from kivymd.uix.screen import MDScreen

from kivymd.icon_definitions import md_icons
from kivymd.app import MDApp
from kivymd.uix.list import OneLineIconListItem

Builder.load_string(
    '''
#:import images_path kivymd.images_path
<CustomOneLineIconListItem>
    on_release:root.parent.parent.parent.parent.selected_categoria(self.text)
    IconLeftWidget:
        icon: root.icon
        

<Droplista>
    MDBoxLayout:
        orientation: 'vertical'
        spacing: dp(10)
        padding: dp(20)
        MDBoxLayout:
            adaptive_height: True
            MDIconButton:
                icon: 'magnify'
            MDTextField:
                id: search_field
                hint_text: 'Search icon'
                on_text: root.set_list_md_icons(self.text, True)
        RecycleView:
            id: rv
            key_viewclass: 'viewclass'
            key_size: 'height'
            RecycleBoxLayout:
                padding: dp(10)
                default_size: None, dp(48)
                default_size_hint: 1, None
                size_hint_y: None
                height: self.minimum_height
                orientation: 'vertical'

'''
)


class CustomOneLineIconListItem(OneLineIconListItem):
    icon = StringProperty()

    def selected_categoria(self):
        a = 0
        pass

class Droplista(MDScreen):

    def set_list_md_icons(self, text="", search=False):
        '''Builds a list of icons for the screen MDIcons.'''

        def add_icon_item(name_icon):
            self.ids.rv.data.append(
                {
                    "viewclass": "CustomOneLineIconListItem",
                    "text": name_icon,
                    "callback": lambda x: x,
                }
            )

        self.ids.rv.data = []
        lista_categorias = ['Abono', 'Agua', 'Alquiler', 'Amazon', 'Amazon Prime', 'Beca', 'Bizum', 'Caprichos', 'Cena',
                            'Comida', 'Comida', 'Compras', 'Depósito', 'Desayuno', 'Fianza', 'Gas', 'Gasolina',
                            'Gastos', 'HBO', 'Hostelería', 'Luz', 'Netflix', 'Ocio', 'Restaurante', 'Ropa', 'Salario',
                            'Subscripción', 'Supermercado', 'Teléfono', 'Transporte']
        for name_icon in lista_categorias:
            if search:
                if text in name_icon:
                    add_icon_item(name_icon)
            else:
                add_icon_item(name_icon)

    def selected_categoria(self, texto):
        self.ids.search_field.text = texto
        pass


