from PyQt5.QtWidgets import QWidget, QLineEdit, QLabel, QPushButton, QHBoxLayout


class QColorEdit(QWidget):
    def __init__(self):
        super().__init__()
        self.edit_color = QLineEdit()
        self.edit_color.setPlaceholderText('Выберите цвет...')
        self.btn_choose_color = QPushButton('Выбрать...')
        self.lbl_color_preview = QLabel()
        self.lbl_color_preview.setFixedSize(20, 20)
        self.lbl_color_preview.setStyleSheet('background-color: #000000;')

        layout = QHBoxLayout()
        layout.addWidget(self.edit_color)
        layout.addWidget(self.lbl_color_preview)
        layout.addWidget(self.btn_choose_color)

        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
