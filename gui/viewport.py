from noise import pnoise2
from PyQt5.Qt import \
    QWidget, \
    QPixmap, \
    QImage, \
    QLabel, \
    QScrollArea, QHBoxLayout
from PyQt5.QtWidgets import QSizePolicy


class Viewport(QScrollArea):

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
        self.setWidget(widget)
        self.setWidgetResizable(True)

    # TODO: Refactor wrt docstring
    def set_map(self, col_map: bytearray, dim: int) -> None:
        """
        Set colored map to draw.
        Causes instant display

        :param dim: Map size in px
        :param col_map: bytearray
        :return: None
        """
        pixmap = QPixmap.fromImage(QImage(col_map,
                                          dim,
                                          dim,
                                          QImage.Format_Indexed8))
        self.display_widget.setPixmap(pixmap)


if __name__ == '__main__':
    import sys
    from PyQt5.Qt import QApplication
    from time import time

    app = QApplication(sys.argv)
    w = Viewport()
    w.setMinimumSize(700, 700)
    shape = [512, 512]
    t = time()
    hmap = bytearray([0 for _ in range(shape[0] * shape[1])])
    for i in range(shape[0]):
        for j in range(shape[1]):
            n = pnoise2(i / 16, j / 16, repeatx=100, repeaty=100)
            hmap[i * shape[1] + j] = int((n + 1) * 128)
    w.set_map(hmap, shape[0])
    print(time() - t)
    w.setVisible(True)
    sys.exit(app.exec())
