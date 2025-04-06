import weakref

from PyQt5 import sip
from PyQt5.QtCore import Qt
import pyqtgraph as pg
import numpy as np
from PyQt5.QtGui import QColor

import consts
from mvvm.viewmodel.graph_builder_view_model import CoordinatePlaneViewModel
from mvvm.widgets.expression_item_widget import ExpressionItemWidget


def tr_line_style(style_str):
    mapping = {
        'сплошная': Qt.SolidLine,
        'пунктирная': Qt.DashLine,
        'точечная': Qt.DotLine
    }
    return mapping.get(style_str, Qt.SolidLine)


class CoordinatePlaneWidget(pg.PlotWidget):
    def __init__(self, viewmodel: CoordinatePlaneViewModel, parent=None):
        super().__init__(parent)
        self._viewmodel = viewmodel
        self._axis_items = {}
        self._curve_items: weakref.WeakKeyDictionary = weakref.WeakKeyDictionary()
        self._init_ui()
        self._connect_signals()

    def _init_ui(self):
        self.setBackground('w')
        self.setMouseEnabled(x=True, y=True)
        self.plotItem.showGrid(x=self._viewmodel.show_grid, y=self._viewmodel.show_grid)
        self._draw_axes()
        self._draw_curves()
        self.getViewBox().disableAutoRange()
        self.getViewBox().setAspectLocked(True)

    def _connect_signals(self):
        self._viewmodel.showAxesChanged.connect(self._update_axes)
        self._viewmodel.showGridChanged.connect(self._update_grid)
        self._viewmodel.expressionsAdded.connect(self._on_expression_added)
        self._viewmodel.expressionsRemoved.connect(self._on_expression_removed)
        self._viewmodel.expressionsChanged.connect(self._on_expression_enabled_changed)
        self.getViewBox().sigRangeChanged.connect(self._on_view_range_changed)

    def _draw_axes(self):
        self._clear_axes()
        axis = consts.CoordinatePlane.Axis
        pen = pg.mkPen(
            self._viewmodel.axis_color if hasattr(self._viewmodel, 'axis_color') else axis.color,
            width=self._viewmodel.axis_width if hasattr(self._viewmodel, 'axis_width') else axis.width,
            style=tr_line_style(self._viewmodel.axis_line_style) if hasattr(self._viewmodel, 'axis_line_style') else axis.line_style
        )
        if self._viewmodel.show_x_axis:
            x_axis = pg.InfiniteLine(angle=axis.X.angle, pen=pen)
            self.addItem(x_axis)
            self._axis_items['x'] = x_axis
        if self._viewmodel.show_y_axis:
            y_axis = pg.InfiniteLine(angle=axis.Y.angle, pen=pen)
            self.addItem(y_axis)
            self._axis_items['y'] = y_axis

    def _clear_axes(self):
        for item in self._axis_items.values():
            self.removeItem(item)
        self._axis_items.clear()

    def _update_axes(self):
        self._draw_axes()

    def _update_grid(self):
        self.plotItem.showGrid(x=self._viewmodel.show_grid, y=self._viewmodel.show_grid)

    def _draw_curve(self, expression_item: ExpressionItemWidget) -> bool:
        """
        Рисует кривую по ее аналитическому представлению, поддерживая форматы:
         1) y = f(x) (например, y=x**2+x+1)
         2) f(x,y)=const
         3) y=const
         4) x=const
         5) f(x) (т.е. y=f(x))
        """
        linspacenum = 1000
        expr_str = expression_item.expression.strip()
        if not expr_str or not expression_item.enabled:
            return False

        expr_str = expr_str.replace('^', '**')

        try:
            xmin, xmax = self.getViewBox().viewRange()[0]
            ymin, ymax = self.getViewBox().viewRange()[1]

            local_vars = {
                'np': np,
                'sin': np.sin,
                'cos': np.cos,
                'sqrt': np.sqrt,
                'pi': np.pi,
                'log': lambda base, arg: np.log(arg) / np.log(base),
                'ln': np.log
            }
            if '=' in expr_str:
                lower_expr = expr_str.lower()
                if lower_expr.startswith('y='):
                    rhs = expr_str[2:].strip()
                    if all(v not in rhs for v in ['x', 'np', 'sin', 'cos', 'sqrt', 'log', 'ln']):
                        const_val = float(eval(rhs, local_vars))
                        x_vals = np.linspace(xmin, xmax, 2)
                        y_vals = np.full_like(x_vals, const_val)
                    else:
                        code = f'def f(x):\n    return {rhs}'
                        exec(code, local_vars)
                        func = local_vars['f']
                        x_vals = np.linspace(xmin, xmax, linspacenum)
                        y_vals = func(x_vals)
                elif lower_expr.startswith('x='):
                    rhs = expr_str[2:].strip()
                    const_val = float(eval(rhs, local_vars))
                    y_vals = np.linspace(ymin, ymax, 2)
                    x_vals = np.full_like(y_vals, const_val)
                else:
                    parts = expr_str.split('=', 1)
                    if len(parts) != 2:
                        return False
                    left, right = parts
                    expr = f"({left.strip()}) - ({right.strip()})"
                    x_lin = np.linspace(xmin, xmax, linspacenum)
                    y_lin = np.linspace(ymin, ymax, linspacenum)
                    X, Y = np.meshgrid(x_lin, y_lin)
                    local_vars.update({'x': X, 'y': Y})
                    Z = eval(expr, local_vars)
                    threshold = (xmax - xmin) / linspacenum
                    mask = np.abs(Z) < threshold
                    if not np.any(mask):
                        return False
                    x_vals = X[mask]
                    y_vals = Y[mask]
                    scatter = self.plotItem.plot(x_vals, y_vals, pen=None, symbol='o', symbolSize=2, symbolBrush=consts.Color.black)
                    self._curve_items[expression_item] = scatter
                    vb = self.getViewBox()
                    vb.blockSignals(True)
                    current_range = vb.viewRange()
                    vb.setRange(xRange=current_range[0], yRange=current_range[1], padding=0)
                    vb.blockSignals(False)
                    return True
            else:
                code = f'def f(x):\n    return {expr_str}'
                exec(code, local_vars)
                func = local_vars['f']
                x_vals = np.linspace(xmin, xmax, linspacenum)
                y_vals = func(x_vals)

            x_vals = np.array(x_vals)
            y_vals = np.array(y_vals)
            # Обработка сингулярностей
            mask = np.isfinite(y_vals) & (np.abs(y_vals) < 1e6)
            mask &= (y_vals >= ymin) & (y_vals <= ymax)
            x_vals = x_vals[mask]
            y_vals = y_vals[mask]
            if x_vals.size == 0 or y_vals.size == 0:
                return False

            pen = pg.mkPen(
                expression_item.curve_color if hasattr(expression_item, 'curve_color') else consts.CoordinatePlane.Curve.color,
                width=expression_item.curve_line_width if hasattr(expression_item, 'curve_line_width') else consts.CoordinatePlane.Curve.width,
                style= expression_item.curve_line_style if hasattr(expression_item, 'curve_line_style') else consts.CoordinatePlane.Curve.line_style
            )
            curve = self.plotItem.plot(x_vals, y_vals, pen=pen)
            self._curve_items[expression_item] = curve

            # Исправление бесконечного рекурсивного автомасштабирования
            vb = self.getViewBox()
            vb.blockSignals(True)
            current_range = vb.viewRange()
            vb.setRange(xRange=current_range[0], yRange=current_range[1], padding=0)
            vb.blockSignals(False)
            return True

        except Exception as e:
            print('Error in drawing curve:', e)
            return False

    def _draw_curves(self):
        self._clear_curves()
        for expr in list(self._curve_items.keys()):
            result = self._draw_curve(expr)
            if result:
                expr.setStyleSheet('')
            else:
                color = consts.Expression.invalid_input_bg_color
                expr.setStyleSheet(f'background-color: {color.name(QColor.HexArgb)};')

    def _clear_curves(self):
        for expr, curve_item in list(self._curve_items.items()):
            if curve_item is not None:
                self.plotItem.removeItem(curve_item)

    def _on_expression_added(self, expression_item: ExpressionItemWidget):
        self._curve_items[expression_item] = None
        expression_item.expressionChanged.connect(
            lambda text, ei=expression_item: self._on_expression_updated(ei, text)
        )
        expression_item.enabledChanged.connect(self._on_expression_enabled_changed)
        expression_item.destroyed.connect(lambda: self._on_expression_removed(expression_item))
        self._draw_curves()

    def _on_expression_updated(self, expression_item: ExpressionItemWidget, text: str):
        self._draw_curves()

    def _on_expression_enabled_changed(self, value: bool = None):
        self._draw_curves()

    def _on_expression_removed(self, expression_item: ExpressionItemWidget):
        if expression_item in self._curve_items:
            curve_item = self._curve_items.pop(expression_item)
            if curve_item is not None:
                self.plotItem.removeItem(curve_item)
        self._draw_curves()

    def _on_view_range_changed(self, viewbox, range_):
        self._draw_curves()
