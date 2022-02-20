from kivy.lang.builder import Builder
from kivymd.uix.screen import MDScreen


# from kivymd_extensions.akivymd.uix.selectionlist import AKSelectListAvatarItem


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
