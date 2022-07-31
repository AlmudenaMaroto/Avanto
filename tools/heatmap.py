from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color
from kivy.properties import (ListProperty, NumericProperty, ObjectProperty)
from kivy.lang import Builder

from matplotlib.pyplot import get_cmap  #

class Heatmap(Widget):

    values = ListProperty([])  # must be a list of lists containing numbers

    colormap = ObjectProperty(get_cmap('RdBu'))

    instructions = ListProperty([])

    def __init__(self, *args, **kwargs):
        super(Heatmap, self).__init__(*args, **kwargs)
        self.bind(values=self._do_layout,
                  pos=self._do_layout,
                  size=self._do_layout)

    def force_update(self):
        # allow the user to manually force a redraw
        self._do_layout()

    def _do_layout(self, *args):
        # draw all the Rectangles

        max_value = max([max(row) for row in self.values])
        min_value = min([min(row) for row in self.values])

        num_rects_horizontal = len(self.values[0])
        num_rects_vertical = len(self.values)
        num_rects = num_rects_horizontal * num_rects_vertical

        # require that the values is a square array
        assert all(len(row) == num_rects_horizontal for row in self.values)

        # check that the number of instructions we already have is consistent
        assert len(self.instructions) % 2 == 0  # should be a Color and a Rectangle for each value

        # add more rectangles if necessary
        while len(self.instructions) < 2 * num_rects:
            with self.canvas:
                self.instructions.append(Color())
                self.instructions.append(Rectangle())

        # remove some rectangles if necessary
        while len(self.instructions) > 2 * num_rects:
            self.canvas.remove(self.instructions.pop())  # a Rectangle
            self.canvas.remove(self.instructions.pop())  # a Color

        # at this point, self.instructions contains just the right
        # number of canvas instructions to draw all our rectangles

        rect_height = self.height / num_rects_vertical
        rect_width = self.width / num_rects_horizontal


        values = self.values
        instructions = self.instructions
        for row in range(num_rects_vertical):
            for column in range(num_rects_horizontal):
                value = values[row][column]
                color = instructions[2 * (row * num_rects_horizontal + column)]
                rectangle = instructions[2 * (row * num_rects_horizontal + column) + 1]

                colormap_value = (value - min_value) / (max_value - min_value)

                r, g, b, a = self.colormap(float(colormap_value))

                color.rgba = (r, g, b, a)
                self_x, self_y = self.pos
                rectangle.pos = (self_x + column * rect_width, self_y + row * rect_height)
                rectangle.size = (rect_width, rect_height)


if __name__ == "__main__":
    from kivy.base import runTouchApp

    root = Builder.load_string("""
#:import np numpy
BoxLayout:
    orientation: 'vertical'
    Heatmap:
        id: heatmap
        values: [[1, 2, 3, 4], [5, 6, 7, 8], [8, 7, 6, 5], [4, 3, 2, 1]]
    Slider:
        id: slider
        size_hint_y: None
        height: dp(40)
        min: 2
        max: 100
    Button:
        size_hint_y: None
        height: dp(40)
        on_press: heatmap.values = np.random.random((int(slider.value), int(slider.value)))
    """)

    runTouchApp(root)