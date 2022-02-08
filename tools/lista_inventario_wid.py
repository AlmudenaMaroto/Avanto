from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import (
    BooleanProperty,
    ColorProperty,
    ListProperty,
    NumericProperty,
    OptionProperty,
    StringProperty,
)
from kivy.uix.behaviors import ButtonBehavior

import kivymd.material_resources as m_res
# from kivymd import uix_path
from kivymd.theming import ThemableBehavior
from kivymd.uix.behaviors import (
    CircularRippleBehavior,
    RectangularRippleBehavior,
)
from kivymd.uix.button import MDIconButton
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.utils.fitimage import FitImage

__all__ = (
    "OneLineListItem_inventario",

)


class BaseListItem_inventario(
    ThemableBehavior, RectangularRippleBehavior, ButtonBehavior, MDFloatLayout
):
    """
    Base class to all ListItems. Not supposed to be instantiated on its own.
    """

    text = StringProperty()
    """
    Text shown in the first line.
    :attr:`text` is a :class:`~kivy.properties.StringProperty`
    and defaults to `''`.
    """

    text_color = ColorProperty(None)
    """
    Text color in ``rgba`` format used if :attr:`~theme_text_color` is set
    to `'Custom'`.
    :attr:`text_color` is a :class:`~kivy.properties.ColorProperty`
    and defaults to `None`.
    """

    font_style = StringProperty("Subtitle1")
    """
    Text font style. See ``kivymd.font_definitions.py``.
    :attr:`font_style` is a :class:`~kivy.properties.StringProperty`
    and defaults to `'Subtitle1'`.
    """

    theme_text_color = StringProperty("Primary", allownone=True)
    """
    Theme text color in ``rgba`` format for primary text.
    :attr:`theme_text_color` is a :class:`~kivy.properties.StringProperty`
    and defaults to `'Primary'`.
    """

    secondary_text = StringProperty()
    """
    Text shown in the second line.
    :attr:`secondary_text` is a :class:`~kivy.properties.StringProperty`
    and defaults to `''`.
    """

    tertiary_text = StringProperty()
    """
    The text is displayed on the third line.
    :attr:`tertiary_text` is a :class:`~kivy.properties.StringProperty`
    and defaults to `''`.
    """

    secondary_text_color = ColorProperty(None)
    """
    Text color in ``rgba`` format used for secondary text
    if :attr:`~secondary_theme_text_color` is set to `'Custom'`.
    :attr:`secondary_text_color` is a :class:`~kivy.properties.ColorProperty`
    and defaults to `None`.
    """

    tertiary_text_color = ColorProperty(None)
    """
    Text color in ``rgba`` format used for tertiary text
    if :attr:`~tertiary_theme_text_color` is set to 'Custom'.
    :attr:`tertiary_text_color` is a :class:`~kivy.properties.ColorProperty`
    and defaults to `None`.
    """

    secondary_theme_text_color = StringProperty("Secondary", allownone=True)
    """
    Theme text color for secondary text.
    :attr:`secondary_theme_text_color` is a :class:`~kivy.properties.StringProperty`
    and defaults to `'Secondary'`.
    """

    tertiary_theme_text_color = StringProperty("Secondary", allownone=True)
    """
    Theme text color for tertiary text.
    :attr:`tertiary_theme_text_color` is a :class:`~kivy.properties.StringProperty`
    and defaults to `'Secondary'`.
    """

    secondary_font_style = StringProperty("Body1")
    """
    Font style for secondary line. See ``kivymd.font_definitions.py``.
    :attr:`secondary_font_style` is a :class:`~kivy.properties.StringProperty`
    and defaults to `'Body1'`.
    """

    tertiary_font_style = StringProperty("Body1")
    """
    Font style for tertiary line. See ``kivymd.font_definitions.py``.
    :attr:`tertiary_font_style` is a :class:`~kivy.properties.StringProperty`
    and defaults to `'Body1'`.
    """

    divider = OptionProperty(
        "Full", options=["Full", "Inset", None], allownone=True
    )
    """
    Divider mode. Available options are: `'Full'`, `'Inset'`
    and default to `'Full'`.
    :attr:`divider` is a :class:`~kivy.properties.OptionProperty`
    and defaults to `'Full'`.
    """

    divider_color = ColorProperty(None)
    """
    Divider color.
    .. versionadded:: 1.0.0
    :attr:`divider_color` is a :class:`~kivy.properties.ColorProperty`
    and defaults to `None`.
    """

    bg_color = ColorProperty(None)
    """
    Background color for menu item.
    :attr:`bg_color` is a :class:`~kivy.properties.ColorProperty`
    and defaults to `None`.
    """

    _txt_left_pad = NumericProperty("16dp")
    _txt_top_pad = NumericProperty()
    _txt_bot_pad = NumericProperty()
    _txt_right_pad = NumericProperty(m_res.HORIZ_MARGINS)
    _num_lines = 3
    _no_ripple_effect = BooleanProperty(False)


class OneLineListItem_inventario(BaseListItem_inventario):
    """A one line list item."""

    _txt_top_pad = NumericProperty("16dp")
    _txt_bot_pad = NumericProperty("15dp")  # dp(20) - dp(5)
    _height = NumericProperty()
    _num_lines = 1

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.height = dp(48) if not self._height else self._height


Builder.load_string(
    """
<BaseListItem>
    size_hint_y: None

    canvas:
        Color:
            rgba:
                ( \
                self.theme_cls.divider_color \
                if root.divider is not None \
                else (0, 0, 0, 0) \
                ) \
                if not root.divider_color \
                else \
                root.divider_color

        Line:
            points:
                ( \
                root.x ,root.y, root.x + self.width, root.y) \
                if root.divider == "Full" else \
                (root.x + root._txt_left_pad, root.y, \
                root.x + self.width - root._txt_left_pad-root._txt_right_pad, \
                root.y \
                )
        Color:
            rgba: root.bg_color if root.bg_color else (0, 0, 0, 0)
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: root.radius

    BoxLayout:
        id: _text_container
        orientation: "vertical"
        pos: root.pos
        padding:
            root._txt_left_pad, root._txt_top_pad, \
            root._txt_right_pad, root._txt_bot_pad

        MDLabel:
            id: _lbl_primary
            text: root.text
            font_style: root.font_style
            theme_text_color: root.theme_text_color
            text_color: root.text_color
            size_hint_y: None
            height: self.texture_size[1]
            markup: True
            shorten_from: "right"
            shorten: True

        MDLabel:
            id: _lbl_secondary
            text: "" if root._num_lines == 1 else root.secondary_text
            font_style: root.secondary_font_style
            theme_text_color: root.secondary_theme_text_color
            text_color: root.secondary_text_color
            size_hint_y: None
            height: 0 if root._num_lines == 1 else self.texture_size[1]
            shorten: True
            shorten_from: "right"
            markup: True

        MDLabel:
            id: _lbl_tertiary
            text: "" if root._num_lines == 1 else root.tertiary_text
            font_style: root.tertiary_font_style
            theme_text_color: root.tertiary_theme_text_color
            text_color: root.tertiary_text_color
            size_hint_y: None
            height: 0 if root._num_lines == 1 else self.texture_size[1]
            shorten: True
            shorten_from: "right"
            markup: True
""")
