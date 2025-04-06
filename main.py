import sys
from PyQt5.QtWidgets import QApplication

import consts
from mvvm.model.model import GraphBuilderModel
from mvvm.viewmodel.graph_builder_view_model import GraphBuilderViewModel
from mvvm.view.view import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    model = GraphBuilderModel()
    viewmodel = GraphBuilderViewModel(model)
    main_window = MainWindow(viewmodel)
    main_window.resize(consts.MainWindow.Size.width, consts.MainWindow.Size.height)
    main_window.show()
    sys.exit(app.exec_())
