from PyQt5.Qt import QMainWindow, QHBoxLayout, QOpenGLWidget


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Perlin Map Generator")
        self.setLayout(QHBoxLayout())
        self.ogl_widget = QOpenGLWidget()
        self.setCentralWidget(self.ogl_widget)
        self.showMaximized()
