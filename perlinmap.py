import sys

from PyQt5.Qt import QApplication

from gui.mainwindow import MainWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.showMaximized()
    sys.exit(app.exec())
