from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QCheckBox
from PyQt5.QtCore import pyqtSignal

import consts


class ExpressionItemWidget(QWidget):
    expressionChanged = pyqtSignal(str)
    enabledChanged = pyqtSignal(bool)
    editingStarted = pyqtSignal()

    def __init__(self, expression: str = "", show: bool = consts.Expression.show, parent=None):
        super().__init__(parent)
        self._expression = expression
        self._show = show
        self._curve_color = consts.CoordinatePlane.Curve.color
        self._curve_line_width = consts.CoordinatePlane.Curve.width
        self._curve_line_style = consts.CoordinatePlane.Curve.line_style
        self._init_ui()

    def _init_ui(self):
        layout = QHBoxLayout()
        self.chk_enabled = QCheckBox()
        self.chk_enabled.setChecked(self._show)
        self.edit_expression = QLineEdit()
        self.edit_expression.setPlaceholderText('Введите выражение...')
        layout.addWidget(self.chk_enabled)
        layout.addWidget(self.edit_expression)
        self.setLayout(layout)
        self.chk_enabled.toggled.connect(self._on_enabled_toggled)
        self.edit_expression.textChanged.connect(self._on_expression_changed)

    def _on_enabled_toggled(self, state):
        self._show = state
        self.enabledChanged.emit(state)

    def _on_expression_changed(self, text):
        self._expression = text
        self.expressionChanged.emit(text)

    def focusInEvent(self, event):
        super().focusInEvent(event)
        self.editingStarted.emit()

    @property
    def expression(self):
        return self._expression

    @expression.setter
    def expression(self, value):
        self._expression = value
        self.edit_expression.setText(value)

    @property
    def enabled(self):
        return self._show

    @enabled.setter
    def enabled(self, value):
        self._show = value
        self.chk_enabled.setChecked(value)

    @property
    def curve_color(self):
        return self._curve_color

    @curve_color.setter
    def curve_color(self, value):
        # Ожидается, что value - QColor или строка, которую можно преобразовать в QColor
        if isinstance(value, str):
            self._curve_color = consts.Color.black if not value else QColor(value)
        else:
            self._curve_color = value

    @property
    def curve_line_width(self):
        return self._curve_line_width

    @curve_line_width.setter
    def curve_line_width(self, value):
        self._curve_line_width = value

    @property
    def curve_line_style(self):
        return self._curve_line_style

    @curve_line_style.setter
    def curve_line_style(self, value):
        self._curve_line_style = value
