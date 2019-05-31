from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import \
    QGridLayout, \
    QWidget, \
    QLabel, \
    QComboBox, \
    QSpinBox
from PyQt5.QtGui import QIcon

from gui.custom_widgets import CustomTab
from mapgenerator.utils import config
from resources import resources


class EditingTab(CustomTab):

    def __init__(self, parent=None):
        super().__init__(parent)
        main_widget = QWidget()
        layout = QGridLayout()
        #
        shape_cb = QComboBox()
        shape_cb.addItem(QIcon(":/icons/square.png"), "Rectangle")
        shape_cb.addItem(QIcon(":/icons/circle.png"), "Round")
        layout.addWidget(QLabel("Brush shape:"), 0, 0)
        layout.addWidget(shape_cb, 0, 1)
        #
        size_sp = QSpinBox()
        size_sp.setRange(1, 50)
        size_sp.setValue(5)
        layout.addWidget(QLabel("Brush size (px):"), 1, 0)
        layout.addWidget(size_sp, 1, 1)
        #
        color_cb = QComboBox()
        for biome in config["biomes"]:
            color_cb.addItem(biome["name"])
        layout.addWidget(QLabel("Brush color:"), 2, 0)
        layout.addWidget(color_cb, 2, 1)
        #
        main_widget.setLayout(layout)
        self.setWidget(main_widget)


if __name__ == '__main__':
    import sys
    from PyQt5.Qt import QApplication

    app = QApplication(sys.argv)
    tab = EditingTab()
    tab.setVisible(True)
    sys.exit(app.exec())
