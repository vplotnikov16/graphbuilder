from PyQt5.QtCore import QObject


class BaseViewModel(QObject):
    def __init__(self, model, parent=None):
        super().__init__(parent)
        self._model = model
