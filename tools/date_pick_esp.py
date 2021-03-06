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
<MDLabeltitle2@MDLabel>:
    theme_text_color: "Custom"
    text_color: 1, 1, 1, 1
    halign: "center"
    vlighn: "center"
    fon_style: "H5"
<MDLabeltitle@MDLabel>
    theme_text_color: "Primary"
    halign: "center"
    vlighn: "center"
    fon_style: "Caption"
<ButtonBase>
    size_hint_y: None
    height: dp(40)
    MDLabel:
        id: value
        text: root.text
        theme_text_color: "Primary"
        halign: "center"
        vlighn: "center"
<AKDatePicker_ini>:
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
            MDLabeltitle2:
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
                 
            MDLabeltitle2:
                text: root._year_title
            MDLabeltitle2:
                text: root._month_title
            MDLabeltitle2:
                text: root._day_title
        BoxLayout:
            size_hint_y: None
            height: dp(50)
            canvas.before:
                Color:
                    rgba: root.theme_cls.bg_dark
                Rectangle:
                    size: self.size
                    pos: self.pos
            MDLabeltitle:
                text: "Year"
            MDLabeltitle:
                text: "Month"
            MDLabeltitle:
                text: "Day"
        BoxLayout:
            ScrollView:
                MDBoxLayout:
                    id: year_view
                    orientation: "vertical"
                    adaptive_height: True
            ScrollView:
                MDBoxLayout:
                    id: month_view
                    orientation: "vertical"
                    adaptive_height: True
            ScrollView:
                MDBoxLayout:
                    id: day_view
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
<AKDatePicker_fin>:
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
            MDLabeltitle2:
                text:'Fecha de fin'
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
                 
            MDLabeltitle2:
                text: root._year_title
            MDLabeltitle2:
                text: root._month_title
            MDLabeltitle2:
                text: root._day_title
        BoxLayout:
            size_hint_y: None
            height: dp(50)
            canvas.before:
                Color:
                    rgba: root.theme_cls.bg_dark
                Rectangle:
                    size: self.size
                    pos: self.pos
            MDLabeltitle:
                text: "Year"
            MDLabeltitle:
                text: "Month"
            MDLabeltitle:
                text: "Day"
        BoxLayout:
            ScrollView:
                MDBoxLayout:
                    id: year_view
                    orientation: "vertical"
                    adaptive_height: True
            ScrollView:
                MDBoxLayout:
                    id: month_view
                    orientation: "vertical"
                    adaptive_height: True
            ScrollView:
                MDBoxLayout:
                    id: day_view
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


class AKDatePicker_ini(BaseDialog, ThemableBehavior):
    year_today = today.strftime("%Y")
    year_range = ListProperty([1990, int(year_today)+1])
    month_type = OptionProperty("string", options=["string", "int"])
    _day_title = StringProperty("-")
    _month_title = StringProperty("-")
    _year_title = StringProperty("-")

    def __init__(self, callback=None, **kwargs):
        super(AKDatePicker_ini, self).__init__(**kwargs)
        self.month_dic = {
            "1": "Enero",
            "2": "Febrero",
            "3": "Marzo",
            "4": "Abril",
            "5": "Mayo",
            "6": "Junio",
            "7": "Julio",
            "8": "Agosto",
            "9": "Septiembre",
            "10": "Octubre",
            "11": "Noviembre",
            "12": "Diciembre",
        }

        self.callback = callback
        for x in reversed(range(self.year_range[0], self.year_range[1])):
            self.ids.year_view.add_widget(
                ButtonBase(text="%d" % x, on_release=self._set_year)
            )
        for x in reversed(range(1, 13)):
            if self.month_type == "string":
                month = self.month_dic[str(x)]
            else:
                month = str(x)

            self.ids.month_view.add_widget(
                ButtonBase(text=month, on_release=self._set_month)
            )
        for x in reversed(range(1, 32)):
            self.ids.day_view.add_widget(
                ButtonBase(text="%d" % x, on_release=self._set_day)
            )

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


class AKDatePicker_fin(BaseDialog, ThemableBehavior):
    year_today = today.strftime("%Y")
    year_range = ListProperty([1990, int(year_today)+1])
    month_type = OptionProperty("string", options=["string", "int"])
    _day_title = StringProperty("-")
    _month_title = StringProperty("-")
    _year_title = StringProperty("-")

    def __init__(self, callback=None, **kwargs):
        super(AKDatePicker_fin, self).__init__(**kwargs)
        self.month_dic = {
            "1": "Enero",
            "2": "Febrero",
            "3": "Marzo",
            "4": "Abril",
            "5": "Mayo",
            "6": "Junio",
            "7": "Julio",
            "8": "Agosto",
            "9": "Septiembre",
            "10": "Octubre",
            "11": "Noviembre",
            "12": "Diciembre",
        }

        self.callback = callback
        for x in reversed(range(self.year_range[0], self.year_range[1])):
            self.ids.year_view.add_widget(
                ButtonBase(text="%d" % x, on_release=self._set_year)
            )
        for x in reversed(range(1, 13)):
            if self.month_type == "string":
                month = self.month_dic[str(x)]
            else:
                month = str(x)

            self.ids.month_view.add_widget(
                ButtonBase(text=month, on_release=self._set_month)
            )
        for x in reversed(range(1, 32)):
            self.ids.day_view.add_widget(
                ButtonBase(text="%d" % x, on_release=self._set_day)
            )

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


class ButtonBase(RectangularRippleBehavior, ButtonBehavior, BoxLayout):
    text = StringProperty()