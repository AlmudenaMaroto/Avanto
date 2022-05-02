from kivy.lang.builder import Builder
from kivymd.uix.screen import MDScreen
from tools.charts_almu import AKBarChart_anomes

# from kivymd_extensions.akivymd.uix.selectionlist import AKSelectListAvatarItem


class Ejercicio(MDScreen):
    def __init__(self, **kwargs):
        super(Ejercicio, self).__init__()
        self.inicializacion()

    def inicializacion(self):
        self.ids.id_evtemp.x_values = [0, 1, 2, 3]
        self.ids.id_evtemp.x_labels = ['a', 'b', 'c', 'd']
        self.ids.id_evtemp.y_values = [10, 21, 32, 32]
        self.ids.id_evtemp.y_labels = [10, 21, 32, 32]
        self.ids.id_evtemp.objetivo = 10

Builder.load_string(
    """
    
<Evolucion_semanal_dep@AKBarChart_semanal>
    size_hint_y: None
    height: dp(180)
    x_values: []
    y_values: []
    label_size: dp(12)

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
                    
                Evolucion_semanal_dep:
                    id: id_evtemp
                    labels: True
                    anim: False
                    trim: False
                    circles: False
                    bg_color: 106/255, 188/255, 206/255, 1
                    #on_select: root.set_text_evtemp(args)
                    line_width:dp(1)

"""
)
