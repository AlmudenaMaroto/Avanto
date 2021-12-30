from kivy.animation import Animation
from kivy.lang import Builder
from kivy.properties import BooleanProperty, NumericProperty, StringProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivymd.theming import ThemableBehavior
from kivymd.uix.behaviors import CircularRippleBehavior

Builder.load_string(
    """
<AKSelectList_etapa>
    orientation: "lr-tb"
    spacing: dp(5)
    padding: dp(10)
    size_hint_y: None
    height: self.minimum_height
<AKSelectListAvatarItem_etapa>
    orientation: "vertical"
    size_hint: 1 / root.columns, None
    height: self.width * 0.5
    padding: dp(5)
    spacing: dp(5)
    on_release: root._choose_selection(_first_label.text)
    BoxLayout:
        size_hint_y: None
        height: dp(50)
        orientation: "horizontal"
        spacing: dp(4)
        MDLabel:
            id: _first_label
            size_hint_x:.9
            text: root.first_label
            font_size:root.width*.1
            theme_text_color: "Primary"
            halign: "center"
        CheckBox:
            size_hint_x:.1
            on_active: root.checkbox_click(self, self.active)
"""
)


class AKSelectListAvatarItem_etapa(
    ThemableBehavior, ButtonBehavior, CircularRippleBehavior, BoxLayout
):
    columns = NumericProperty(2)
    source = StringProperty("")
    first_label = StringProperty("")
    second_label = StringProperty("")
    animate_start = BooleanProperty(True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _choose_selection(self, select):

        selected_list = self.parent._selected_list

        if select not in selected_list:
            selected_list.append(select)
            self._selection_anim()

        else:
            selected_list.remove(select)
            self._deselection_anim()

        if not selected_list:
            selected_list = []

        self.parent._selected_list = selected_list

    def _selection_anim(self):
        pass
        # anim = Animation(font_size=self.width / 3, t="out_bounce", duration=0.1)
        # anim.start(self.ids._box)

    def _deselection_anim(self):
        pass
        # anim = Animation(
        #     font_size=0,
        #     size=self.ids._box.texture_size,
        #     t="in_bounce",
        #     duration=0.1,
        # )
        # anim.start(self.ids._box)

    def checkbox_click(self, a, b):
        pass


class AKSelectList_etapa(StackLayout):
    _selected_list = []

    def get_selection(self):
        return self._selected_list

    def clear_selection(self):
        if not self.children:
            return

        for child in self.children:
            if child.first_label in self._selected_list:
                child._deselection_anim()
        self._selected_list = []

    def select_all(self):
        for child in self.children:
            if child.first_label not in self._selected_list:
                child._selection_anim()
                self._selected_list.append(child.first_label)
