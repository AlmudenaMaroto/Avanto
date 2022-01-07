from datetime import datetime

from kivy.lang import Builder
from kivy.properties import ListProperty, OptionProperty, StringProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivymd.theming import ThemableBehavior
from kivymd.uix.behaviors import RectangularRippleBehavior
from kivymd.uix.dialog import BaseDialog
from datetime import date

today = date.today()

Builder.load_string(
    """
<MDLabeltitle_22_2@MDLabel>:
    theme_text_color: "Custom"
    text_color: 1, 1, 1, 1
    halign: "center"
    vlighn: "center"
    fon_style: "H5"
<MDLabeltitle_2@MDLabel>
    theme_text_color: "Primary"
    halign: "center"
    vlighn: "center"
    fon_style: "Caption"
<ButtonBase2>
    size_hint_y: None
    height: dp(40)
    BoxLayout:
        MDLabel:
            id: value
            text: root.text
            theme_text_color: "Primary"
            halign: "center"
            vlighn: "center"
        MDLabel:
            text: 'prueba'
            theme_text_color: "Primary"
            halign: "center"
            vlighn: "center"
<Tabla_tasa_ahorro>:
    size_hint: None, None
    size:
        (dp(302), dp(450)) \
        if root.theme_cls.device_orientation == "portrait" \
        else (dp(450), dp(350))
    BoxLayout:
        orientation: "vertical"
        canvas.before:
            Color:
                rgba: root.theme_cls.bg_normal
            RoundedRectangle:
                size: self.size
                pos: self.pos
        BoxLayout:
            size_hint_y: None
            height: dp(50)
            canvas.before:
                Color:
                    rgba: 95/255,166/255,182/255,1
                RoundedRectangle:
                    size: self.size
                    pos: self.pos
                    radius:[(10.0, 10.0), (10.0, 10.0), (0, 0), (0, 0)]
            MDLabeltitle_22_2:
                text:'Fecha de inicio'
        BoxLayout:
            size_hint_y: None
            height: dp(50)
            canvas.before:
                Color:
                    rgba: 95/255,166/255,182/255,1
                RoundedRectangle:
                    size: self.size
                    pos: self.pos
                    radius:[(0.0, 0.0), (0.0, 0.0), (0, 0), (0, 0)]
                 
        BoxLayout:
            size_hint_y: None
            height: dp(50)
            canvas.before:
                Color:
                    rgba: root.theme_cls.bg_dark
                Rectangle:
                    size: self.size
                    pos: self.pos
            MDLabeltitle_2:
                text: "Año-Mes"
            MDLabeltitle_2:
                text: "Ingresos"
            MDLabeltitle_2:
                text: "Gastos"
            MDLabeltitle_2:
                text: "Tasa"
        BoxLayout:
            ScrollView:
                MDBoxLayout:
                    id: year_view
                    orientation: "vertical"
                    adaptive_height: True

        BoxLayout:
            size_hint_y: None
            height: dp(40)
            padding: [dp(10), 0]
            spacing: dp(10)
            canvas.before:
                Color:
                    rgba: root.theme_cls.bg_dark
                RoundedRectangle:
                    size: self.size
                    pos: self.pos
                    radius: [(0.0, 10.0), (0.0, 10.0), (10, 10), (10, 10)]
            MDFlatButton:
                text: "Cancelar"
                pos_hint: {"center_x": .5, "center_y": .5}
                on_release: root.cancel()
            MDFlatButton:
                text: "Seleccionar"
                pos_hint: {"center_x": .5, "center_y": .5}
                on_release: root._choose()

"""
)


class Tabla_tasa_ahorro(BaseDialog, ThemableBehavior):
    year_today = today.strftime("%Y")
    year_range = ListProperty([1990, int(year_today) + 1])
    month_type = OptionProperty("string", options=["string", "int"])
    _day_title = StringProperty("-")
    _month_title = StringProperty("-")
    _year_title = StringProperty("-")

    def __init__(self, tabla_dict, callback=None, **kwargs):
        super(Tabla_tasa_ahorro, self).__init__(**kwargs)

        for fila in tabla_dict:
            self.ids.year_view.add_widget(
                ButtonBase2(text="%s" % fila.get('anomes'))
            )

        # for fila in tabla_dict:
        #     self.ids.month_view.add_widget(
        #         ButtonBase2(text="%s %s" % (fila.get('anomes'), str(fila.get('gastos'))), on_release=self._set_year)
        #     )
        self.callback = callback
        # for x in reversed(range(self.year_range[0], self.year_range[1])):
        #     self.ids.year_view.add_widget(
        #         ButtonBase2(text="%d %d" % (x, x), on_release=self._set_year)
        #     )

    def _set_day(self, instance):
        self._day_title = instance.text

    def _set_month(self, instance):
        self._month_title = instance.text

    def _set_year(self, instance):
        self._year_title = instance.text

    def on_dismiss(self):
        self._year_title = "-"
        self._month_title = "-"
        self._day_title = "-"
        return

    def _choose(self):
        if not self.callback:
            return False

        if self.month_type == "string":
            for k, v in self.month_dic.items():
                if v == self._month_title:
                    self._month_title = k
                    break

        try:
            date = datetime(
                int(self._year_title),
                int(self._month_title),
                int(self._day_title),
            )
        except BaseException:
            date = False

        self.callback(date)
        self.cancel()

    def cancel(self):
        self.dismiss()


class ButtonBase2(RectangularRippleBehavior, ButtonBehavior, BoxLayout):
    text = StringProperty()
