from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import \
    QMainWindow, \
    QWidget, \
    QSplitter, \
    QGridLayout

from gui.tabpanel import TabPanel
from gui.viewport import Viewport
from mapgenerator.gen_utils import generate_height_map


# noinspection PyUnresolvedReferences
class MainWindow(QMainWindow):

    gen_submitted = pyqtSignal(bytearray, int)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Perlin Map Generator")
        # Central container setup
        central_widget = QWidget(self)
        layout = QGridLayout()
        #
        splitter = QSplitter()
        splitter.setChildrenCollapsible(False)
        #
        self.tab_panel = TabPanel()
        splitter.addWidget(self.tab_panel)
        #
        self.viewport = Viewport()
        splitter.addWidget(self.viewport)
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 5)
        layout.addWidget(splitter)
        # Setting up signals
        self.tab_panel.gen_submitted.connect(self._set_map)
        self.gen_submitted.connect(self.viewport.set_map)
        #
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        #
        self._create_menu()
        self._create_status_bar()

    def _set_map(self, state: dict):
        dim = state["dim"]
        hmap = generate_height_map(dim=dim,
                                   octaves=state["octaves"],
                                   persistence=state["persistence"],
                                   repeatx=state["x_period"], repeaty=state["y_period"])
        self.gen_submitted.emit(hmap, dim)

    # TODO: implement
    def _create_menu(self):
        pass

    # TODO: implement
    def _create_status_bar(self):
        pass


if __name__ == '__main__':
    import sys
    from PyQt5.Qt import QApplication

    app = QApplication(sys.argv)
    tab = MainWindow()
    tab.showMaximized()
    sys.exit(app.exec())
