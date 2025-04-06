from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QPushButton, QHBoxLayout, QListWidgetItem
from PyQt5.QtCore import Qt
from mvvm.viewmodel.graph_builder_view_model import GraphBuilderViewModel
from mvvm.widgets.expression_item_widget import ExpressionItemWidget

class ExpressionsWidget(QWidget):
    def __init__(self, viewmodel: GraphBuilderViewModel, parent=None):
        super().__init__(parent)
        self._viewmodel = viewmodel
        self._init_ui()
        self._connect_signals()

    def _init_ui(self):
        layout = QVBoxLayout()
        title = QLabel('Выражения')
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)
        btn_layout = QHBoxLayout()
        self.btn_add = QPushButton('Добавить')
        self.btn_remove = QPushButton('Удалить')
        btn_layout.addWidget(self.btn_add)
        btn_layout.addWidget(self.btn_remove)
        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def _connect_signals(self):
        self.btn_add.clicked.connect(self._on_add_expression)
        self.btn_remove.clicked.connect(self._on_remove_expression)
        self.list_widget.itemSelectionChanged.connect(self._on_selection_changed)

    def _on_add_expression(self):
        widget = ExpressionItemWidget("", True)
        widget.editingStarted.connect(self._on_item_editing_started)
        item = QListWidgetItem(self.list_widget)
        item.setSizeHint(widget.sizeHint())
        self.list_widget.addItem(item)
        self.list_widget.setItemWidget(item, widget)
        self._viewmodel.coordinatePlaneVM.add_expression(widget)

    def _on_remove_expression(self):
        selected_items = self.list_widget.selectedItems()
        if not selected_items:
            return
        for item in selected_items:
            row = self.list_widget.row(item)
            self.list_widget.takeItem(row)
        self._viewmodel.selected_expression = None
        self._viewmodel.coordinatePlaneVM.remove_expression(selected_items[0])

    def _on_selection_changed(self):
        selected_items = self.list_widget.selectedItems()
        if selected_items:
            widget = self.list_widget.itemWidget(selected_items[0])
            self._viewmodel.selected_expression = widget
        else:
            self._viewmodel.selected_expression = None

    def _on_item_editing_started(self):
        sender = self.sender()  # sender должен быть ExpressionItemWidget
        for index in range(self.list_widget.count()):
            item = self.list_widget.item(index)
            widget = self.list_widget.itemWidget(item)
            if widget is sender:
                self.list_widget.setCurrentItem(item)
                self._viewmodel.selected_expression = widget
                break

