from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QCheckBox, QGroupBox, QFormLayout, QSpinBox, QComboBox
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QColorDialog

import consts
from mvvm.viewmodel.graph_builder_view_model import GraphBuilderViewModel
from mvvm.widgets.custom.color_edit import QColorEdit


def get_line_style_name(line_style):
    mapping = {
        Qt.SolidLine: 'сплошная',
        Qt.DashLine: 'пунктирная',
        Qt.DotLine: 'точечная',
    }
    return mapping[line_style]


class SettingsWidget(QWidget):
    def __init__(self, viewmodel: GraphBuilderViewModel, parent=None):
        super().__init__(parent)
        self._viewmodel = viewmodel
        self._init_ui()
        self._connect_signals()
        self._update_expression_group_visibility()

    def _init_ui(self):
        layout = QVBoxLayout()
        title = QLabel('Настройки')
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        # Группа настроек осей
        axes_group = QGroupBox('Настройки осей')
        axes_layout = QFormLayout()
        self.chk_show_x = QCheckBox('Показывать ось X')
        self.chk_show_y = QCheckBox('Показывать ось Y')
        self.chk_show_x.setChecked(consts.CoordinatePlane.Axis.X.show)
        self.chk_show_y.setChecked(consts.CoordinatePlane.Axis.Y.show)
        axes_layout.addWidget(self.chk_show_x)
        axes_layout.addWidget(self.chk_show_y)
        self.spin_axis_width = QSpinBox()
        self.spin_axis_width.setMinimum(consts.CoordinatePlane.Axis.width_min)
        self.spin_axis_width.setMaximum(consts.CoordinatePlane.Axis.width_max)
        self.spin_axis_width.setValue(consts.CoordinatePlane.Axis.width)
        self.axis_color_edit = QColorEdit()
        self.combo_axis_line_style = QComboBox()
        self.combo_axis_line_style.addItems(['сплошная', 'пунктирная', 'точечная'])
        axes_layout.addRow('Толщина осей', self.spin_axis_width)
        axes_layout.addRow('Цвет осей', self.axis_color_edit)
        axes_layout.addRow('Тип линии осей', self.combo_axis_line_style)
        axes_group.setLayout(axes_layout)
        layout.addWidget(axes_group)
        # Группа настроек фоновой сетки
        grid_group = QGroupBox('Фоновая сетка')
        grid_layout = QVBoxLayout()
        self.chk_show_grid = QCheckBox('Показывать сетку')
        self.chk_show_grid.setChecked(consts.CoordinatePlane.Grid.show)
        grid_layout.addWidget(self.chk_show_grid)
        grid_group.setLayout(grid_layout)
        layout.addWidget(grid_group)
        # Блок настроек для выбранного выражения
        self.expression_group = QGroupBox('Настройки выражения')
        expression_layout = QFormLayout()
        self.spin_line_width = QSpinBox()
        self.spin_line_width.setMinimum(consts.CoordinatePlane.Curve.width_min)
        self.spin_line_width.setMaximum(consts.CoordinatePlane.Curve.width_max)
        self.spin_line_width.setValue(consts.CoordinatePlane.Curve.width)
        self.curve_color_edit = QColorEdit()
        self.combo_curve_line_style = QComboBox()
        self.combo_curve_line_style.addItems(['сплошная', 'пунктирная', 'точечная'])
        self.chk_enable_expression = QCheckBox('Отображать кривую')
        self.chk_enable_expression.setChecked(True)
        expression_layout.addRow('Отображать кривую', self.chk_enable_expression)
        expression_layout.addRow('Толщина линии', self.spin_line_width)
        expression_layout.addRow('Цвет кривой', self.curve_color_edit)
        expression_layout.addRow('Тип линии', self.combo_curve_line_style)
        self.expression_group.setLayout(expression_layout)
        layout.addWidget(self.expression_group)
        layout.addStretch()
        self.setLayout(layout)

    def _connect_signals(self):
        self._viewmodel.selectedExpressionChanged.connect(self._update_selected_expression_settings)

        self.chk_show_x.toggled.connect(self._on_toggle_x_axis)
        self.chk_show_y.toggled.connect(self._on_toggle_y_axis)
        self.chk_show_grid.toggled.connect(self._on_toggle_grid)

        self.axis_color_edit.btn_choose_color.clicked.connect(self._on_choose_axis_color)
        self.axis_color_edit.edit_color.textChanged.connect(self._update_axis_color_preview)
        self.axis_color_edit.edit_color.textChanged.connect(self._update_axes_settings)
        self.spin_axis_width.valueChanged.connect(self._update_axes_settings)
        self.combo_axis_line_style.currentTextChanged.connect(self._update_axes_settings)

        self.curve_color_edit.btn_choose_color.clicked.connect(self._on_choose_curve_color)
        self.curve_color_edit.edit_color.textChanged.connect(self._update_curve_color_preview)
        self.combo_curve_line_style.currentTextChanged.connect(self._on_curve_line_style_changed)
        self.spin_line_width.valueChanged.connect(self._on_curve_line_width_changed)
        self.chk_enable_expression.toggled.connect(self._on_curve_enabled_changed)

    def _on_toggle_x_axis(self, checked: bool):
        self._viewmodel.coordinatePlaneVM.show_x_axis = checked

    def _on_toggle_y_axis(self, checked: bool):
        self._viewmodel.coordinatePlaneVM.show_y_axis = checked

    def _on_toggle_grid(self, checked: bool):
        self._viewmodel.coordinatePlaneVM.show_grid = checked

    def _on_choose_axis_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.axis_color_edit.edit_color.setText(color.name())

    def _update_expression_group_visibility(self):
        if self._viewmodel.selected_expression is None:
            self.expression_group.hide()
        else:
            self.expression_group.show()

    def _update_axis_color_preview(self, text):
        # Обновление квадратика-превью цвета
        self.axis_color_edit.lbl_color_preview.setStyleSheet('background-color: {};'.format(text if text else consts.Color.black.name()))

    def _update_axes_settings(self):
        # Обновление настроек осей в ViewModel (для перерисовки в CoordinatePlaneWidget)
        self._viewmodel.coordinatePlaneVM.axis_width = self.spin_axis_width.value()
        self._viewmodel.coordinatePlaneVM.axis_color = self.axis_color_edit.edit_color.text() or consts.Color.black.name()
        self._viewmodel.coordinatePlaneVM.axis_line_style = self.combo_axis_line_style.currentText()
        self._viewmodel.coordinatePlaneVM.showAxesChanged.emit()

    def _on_choose_curve_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.curve_color_edit.edit_color.setText(color.name())
            # При выборе цвета обновляем настройки у выбранного выражения
            if self._viewmodel.selected_expression is not None:
                self._viewmodel.selected_expression.curve_color = color
                self._viewmodel.coordinatePlaneVM.expressionsChanged.emit()

    def _update_curve_color_preview(self, text):
        self.curve_color_edit.lbl_color_preview.setStyleSheet(
            'background-color: {};'.format(text if text else consts.CoordinatePlane.Curve.color.name()))

    def _update_selected_expression_settings(self):
        selected_expr = self._viewmodel.selected_expression
        if selected_expr is None:
            self.expression_group.hide()
            return

        self.expression_group.show()
        # Обновляем поля настроек из выбранного ExpressionItemWidget
        self.spin_line_width.setValue(selected_expr.curve_line_width)
        self.curve_color_edit.edit_color.setText(selected_expr.curve_color.name())
        self.combo_curve_line_style.setCurrentText(get_line_style_name(selected_expr.curve_line_style))
        self.chk_enable_expression.setChecked(selected_expr.enabled)

    def _on_curve_line_width_changed(self, value):
        if self._viewmodel.selected_expression is not None:
            self._viewmodel.selected_expression.curve_line_width = value
            self._viewmodel.coordinatePlaneVM.expressionsChanged.emit()

    def _on_curve_color_changed(self, text):
        selected_expr = self._viewmodel.selected_expression
        if selected_expr is not None:
            selected_expr.curve_color = text or consts.CoordinatePlane.Curve.color.name()
            self._viewmodel.coordinatePlaneVM.expressionsChanged.emit()

    def _on_curve_line_style_changed(self, text):
        mapping = {
            'сплошная': Qt.SolidLine,
            'пунктирная': Qt.DashLine,
            'точечная': Qt.DotLine
        }
        pen_style = mapping.get(text, Qt.SolidLine)
        if self._viewmodel.selected_expression is not None:
            self._viewmodel.selected_expression.curve_line_style = pen_style
            self._viewmodel.coordinatePlaneVM.expressionsChanged.emit()

    def _on_curve_enabled_changed(self, checked):
        selected_expr = self._viewmodel.selected_expression
        if selected_expr is not None:
            selected_expr.enabled = checked
            self._viewmodel.coordinatePlaneVM.expressionsChanged.emit()
