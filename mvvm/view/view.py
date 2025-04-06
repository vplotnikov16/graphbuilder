import sys
from PyQt5.QtWidgets import QMainWindow, QDockWidget, QApplication, QAction
from PyQt5.QtCore import Qt
from mvvm.widgets.expressions_widget import ExpressionsWidget
from mvvm.widgets.coordinate_widget import CoordinatePlaneWidget
from mvvm.widgets.settings_widget import SettingsWidget
from mvvm.viewmodel.graph_builder_view_model import GraphBuilderViewModel


class MainWindow(QMainWindow):
    def __init__(self, viewmodel: GraphBuilderViewModel, parent=None):
        super().__init__(parent)
        self._viewmodel = viewmodel
        self.setWindowTitle("Графопостроитель")
        self._init_ui()
        self._create_menu()

    def _init_ui(self):
        self.coordinate_widget = CoordinatePlaneWidget(self._viewmodel.coordinatePlaneVM)
        self.setCentralWidget(self.coordinate_widget)

        # Док-виджет для Выражений
        self.dock_expressions = QDockWidget("Выражения", self)
        self.expressions_widget = ExpressionsWidget(self._viewmodel)
        self.dock_expressions.setWidget(self.expressions_widget)
        self.dock_expressions.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dock_expressions)
        self.dock_expressions.visibilityChanged.connect(
            lambda visible: self._update_menu_action("Выражения", visible)
        )

        # Док-виджет для Настроек
        self.dock_settings = QDockWidget("Настройки", self)
        self.settings_widget = SettingsWidget(self._viewmodel)
        self.dock_settings.setWidget(self.settings_widget)
        self.dock_settings.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dock_settings)
        self.dock_settings.visibilityChanged.connect(
            lambda visible: self._update_menu_action("Настройки", visible)
        )

    def _create_menu(self):
        self.menu_actions = {}
        menubar = self.menuBar()
        view_menu = menubar.addMenu("Вид")

        action_expressions = QAction("Выражения", self, checkable=True)
        action_expressions.setChecked(True)
        action_expressions.triggered.connect(lambda checked: self._toggle_dock("Выражения", checked))
        view_menu.addAction(action_expressions)
        self.menu_actions["Выражения"] = action_expressions

        action_settings = QAction("Настройки", self, checkable=True)
        action_settings.setChecked(True)
        action_settings.triggered.connect(lambda checked: self._toggle_dock("Настройки", checked))
        view_menu.addAction(action_settings)
        self.menu_actions["Настройки"] = action_settings

    def _toggle_dock(self, name, checked):
        if name == "Выражения":
            if checked:
                self.dock_expressions.show()
            else:
                self.dock_expressions.close()
        elif name == "Настройки":
            if checked:
                self.dock_settings.show()
            else:
                self.dock_settings.close()

    def _update_menu_action(self, name, visible):
        if name in self.menu_actions:
            self.menu_actions[name].setChecked(visible)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    from mvvm.model.model import GraphBuilderModel
    from mvvm.viewmodel.graph_builder_view_model import GraphBuilderViewModel

    model = GraphBuilderModel()
    viewmodel = GraphBuilderViewModel(model)
    main_window = MainWindow(viewmodel)
    main_window.resize(1000, 700)
    main_window.show()
    sys.exit(app.exec_())
