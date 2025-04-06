from PyQt5.QtCore import pyqtSignal

from mvvm.viewmodel.base_view_model import BaseViewModel
from mvvm.viewmodel.coordinate_plane_view_model import CoordinatePlaneViewModel


class GraphBuilderViewModel(BaseViewModel):
    selectedExpressionChanged = pyqtSignal()

    def __init__(self, model, parent=None):
        super().__init__(model, parent)
        self.coordinatePlaneVM = CoordinatePlaneViewModel(parent=self)
        self._selected_expression = None

    @property
    def selected_expression(self):
        return self._selected_expression

    @selected_expression.setter
    def selected_expression(self, value):
        if self._selected_expression != value:
            self._selected_expression = value
            self.selectedExpressionChanged.emit()
