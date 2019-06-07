from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import \
    QGridLayout, \
    QWidget, \
    QLabel

from gui.custom_widgets import CustomTab
from mapgenerator.utils import terr_obj_assets


class AssetsTab(CustomTab):

    def __init__(self, parent=None):
        super().__init__(parent)
        main_widget = QWidget()
        layout = QGridLayout()
        #
        for index, (name, asset) in enumerate(terr_obj_assets()):
            icon = QLabel()
            icon.setPixmap(asset.scaled(96, 96,
                                        Qt.KeepAspectRatio,
                                        Qt.FastTransformation))
            icon.setToolTip(name)
            icon.setStyleSheet("border:1px solid black;")
            layout.addWidget(icon, index // 2, index % 2)
        #
        main_widget.setLayout(layout)
        self.setWidget(main_widget)


if __name__ == '__main__':
    import sys
    from PyQt5.Qt import QApplication

    app = QApplication(sys.argv)
    tab = AssetsTab()
    tab.setVisible(True)
    sys.exit(app.exec())
