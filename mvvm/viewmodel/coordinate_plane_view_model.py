from typing import List

from PyQt5.QtCore import QObject, pyqtSignal

import consts
from mvvm.widgets.expression_item_widget import ExpressionItemWidget


class CoordinatePlaneViewModel(QObject):
    showAxesChanged = pyqtSignal()
    showGridChanged = pyqtSignal()
    expressionsAdded = pyqtSignal(object)
    expressionsRemoved = pyqtSignal(object)
    expressionsChanged = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._show_x_axis = consts.CoordinatePlane.Axis.X.show
        self._show_y_axis = consts.CoordinatePlane.Axis.Y.show
        self._show_grid = consts.CoordinatePlane.Grid.show
        self._expressions: List[ExpressionItemWidget] = []

    def add_expression(self, expression: ExpressionItemWidget):
        if expression not in self._expressions:
            self._expressions.append(expression)
            self.expressionsAdded.emit(expression)

    def remove_expression(self, expression: ExpressionItemWidget):
        if expression in self._expressions:
            self._expressions.remove(expression)
            self.expressionsRemoved.emit(expression)

    @property
    def show_x_axis(self) -> bool:
        return self._show_x_axis

    @show_x_axis.setter
    def show_x_axis(self, value: bool):
        if self._show_x_axis != value:
            self._show_x_axis = value
            self.showAxesChanged.emit()

    @property
    def show_y_axis(self) -> bool:
        return self._show_y_axis

    @show_y_axis.setter
    def show_y_axis(self, value: bool):
        if self._show_y_axis != value:
            self._show_y_axis = value
            self.showAxesChanged.emit()

    @property
    def show_grid(self) -> bool:
        return self._show_grid

    @show_grid.setter
    def show_grid(self, value: bool):
        if self._show_grid != value:
            self._show_grid = value
            self.showGridChanged.emit()

    @property
    def expressions(self) -> tuple[ExpressionItemWidget, ...]:
        return tuple(self._expressions)
