from PyQt5.Qt import \
    QWidget, \
    QPixmap, \
    QImage, \
    QLabel, \
    QScrollArea, QHBoxLayout, QMouseEvent
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtCore import pyqtSignal

from mapgenerator.utils import biome_with_color


class Viewport(QScrollArea):

    mouse_moved = pyqtSignal(int, int, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        widget = QWidget(self)
        layout = QHBoxLayout()
        self.display_widget = QLabel(self)
        widget.setStyleSheet("background-color: rgb(192, 192, 192);")
        # widget.setMinimumSize(400, 400)
        widget.setSizePolicy(QSizePolicy(QSizePolicy.Maximum,
                                         QSizePolicy.Maximum))
        widget.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,
                                         QSizePolicy.Expanding))
        layout.addStretch()
        layout.addWidget(self.display_widget)
        layout.addStretch()
        widget.setLayout(layout)
        self.col_map = bytearray()
        self.dim = 0
        self.setWidget(widget)
        self.setWidgetResizable(True)

    def set_map(self, col_map: bytearray, dim: int) -> None:
        """
        Set colored map to draw.
        Causes instant display

        :param dim: Map size in px
        :param col_map: bytearray
        :return: None
        """
        self.col_map = col_map
        self.dim = dim
        pixmap = QPixmap.fromImage(QImage(col_map,
                                          dim,
                                          dim,
                                          QImage.Format_RGB888))
        self.display_widget.setPixmap(pixmap)

    def mouseMoveEvent(self, a0: QMouseEvent):
        x = a0.x()
        y = a0.y()
        lin_coord = x * self.dim + y
        rgb = self.col_map[lin_coord: lin_coord + 3]
        color = f"#{hex(rgb[0])[2:]}{hex(rgb[1])[2:]}{hex(rgb[2])[2:]}"
        biome = biome_with_color(color)
        if biome:
            self.mouse_moved.emit(x, y, biome)


if __name__ == '__main__':
    import sys
    from PyQt5.Qt import QApplication
    from time import time

    from mapgenerator.gen_utils import generate_colored_map
    from mapgenerator.utils import config

    app = QApplication(sys.argv)
    w = Viewport()
    w.setMinimumSize(700, 700)
    colors = {biome["color"]: float(biome["base_lvl"]) for biome in config["biomes"]}
    dim = 512
    pers = 0.5
    octaves = 1
    t = time()
    col_map = generate_colored_map(dim=dim,
                                   octaves=octaves,
                                   persistence=pers,
                                   repeatx=1024,
                                   repeaty=1024,
                                   colors=colors)
    w.set_map(col_map, dim)
    print(time() - t)
    w.setVisible(True)
    sys.exit(app.exec())
