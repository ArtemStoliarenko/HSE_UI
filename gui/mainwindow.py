from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import \
    QMainWindow, \
    QWidget, \
    QSplitter, \
    QGridLayout, \
    QMenuBar, \
    QAction, qApp
from PyQt5.QtGui import QCloseEvent
import numpy as np

from gui.tabpanel import TabPanel
from gui.viewport import Viewport
from mapgenerator.gen_utils import generate_colored_map, numpy_to_bytes
from mapgenerator.utils import config


# noinspection PyUnresolvedReferences
class MainWindow(QMainWindow):
    gen_submitted = pyqtSignal(bytes, int)

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
        self.viewport.mouse_moved.connect(self._update_status_bar)
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
        self.setMenuBar(self._create_menu())
        self._create_status_bar()

    def _set_map(self, height_state: dict):
        dim = height_state["dim"]
        terr_state = self.tab_panel.terrain_state()
        colors = {terr_state[biome]["color"]: terr_state[biome]["level"]
                  for biome in terr_state}
        hmap = generate_colored_map(dim=dim,
                                    scale=height_state["scale"],
                                    octaves=height_state["octaves"],
                                    persistence=height_state["persistence"],
                                    repeatx=height_state["x_period"],
                                    repeaty=height_state["y_period"],
                                    colors=colors)
        self.gen_submitted.emit(numpy_to_bytes(hmap), dim)

    # TODO: implement
    def _create_menu(self) -> QMenuBar:
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("&File")
        view_menu = menu_bar.addMenu("&View")
        help_menu = menu_bar.addMenu("&Help")
        #
        open_action = QAction("Open...", self)
        open_action.setShortcut("Ctrl+O")
        file_menu.addAction(open_action)
        file_menu.addSeparator()
        save_action = QAction("Save...", self)
        save_action.setShortcut("Ctrl+S")
        file_menu.addAction(save_action)
        save_as_action = QAction("Save as...", self)
        save_as_action.setShortcut("Ctrl+Shift+S")
        file_menu.addAction(save_as_action)
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.closeEvent)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)
        #
        return menu_bar

    def _create_status_bar(self):
        self.statusBar()

    def _update_status_bar(self, x: int, y: int, biome: str):
        self.statusBar().showMessage(f"x: {x}\ty: {y}\tbiome: {biome}")

    # TODO: implement save logic
    def closeEvent(self, a0: QCloseEvent):
        qApp.exit(0)
        pass

# TODO:
# Автоматическая растановка графических ассетов
# Как в ВоВ
# Плотность в биомах
# Реальные сценарии


if __name__ == '__main__':
    import sys
    from PyQt5.Qt import QApplication

    app = QApplication(sys.argv)
    tab = MainWindow()
    tab.showMaximized()
    sys.exit(app.exec())
