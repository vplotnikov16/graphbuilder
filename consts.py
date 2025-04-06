from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor


class MainWindow:
    class Size:
        width = 1000
        height = 700


class Color:
    black = QColor(0, 0, 0)
    white = QColor(255, 255, 255)
    red = QColor(255, 0, 0)
    green = QColor(0, 255, 0)
    blue = QColor(0, 0, 255)

    pale_red = QColor(255, 0, 0, alpha=128)
    pale_green = QColor(0, 255, 0, alpha=128)
    pale_blue = QColor(0, 255, 0, alpha=128)


class Expression:
    invalid_input_bg_color = Color.pale_red
    show = True


class CoordinatePlane:
    bg_color = Color.white

    class Grid:
        show = True

    class Axis:
        width_min = 1
        width_max = 20
        width = 2
        color = Color.black
        line_style = Qt.SolidLine

        class X:
            angle = 0
            show = True

        class Y:
            angle = 90
            show = True

    class Curve:
        width_min = 1
        width_max = 20
        width = 2
        color = Color.black
        line_style = Qt.SolidLine
        show = Expression.show
