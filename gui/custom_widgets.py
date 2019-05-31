from PyQt5.QtWidgets import \
    QGridLayout, \
    QWidget, \
    QLabel, \
    QColorDialog, \
    QPushButton, \
    QSlider, \
    QDoubleSpinBox, \
    QSpinBox, \
    QHBoxLayout, \
    QScrollArea, \
    QSizePolicy
from PyQt5.QtCore import Qt, pyqtSignal


# noinspection PyUnresolvedReferences
class SliderSpinBox(QWidget):

    value_changed = pyqtSignal(float)

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QGridLayout()
        self.setLayout(layout)
        self.spinbox = QDoubleSpinBox()
        self.spinbox.setRange(0, 1)
        self.spinbox.setSingleStep(0.01)
        self.spinbox.valueChanged.connect(self._update_slider)
        self.slider = QSlider(Qt.Horizontal)
        self.slider.valueChanged.connect(self._update_spinbox)
        layout.addWidget(self.slider, 0, 0, 1, 3)
        layout.addWidget(self.spinbox, 0, 3, 1, 1)

    def value(self) -> float:
        return self.spinbox.value()

    def set_value(self, value: float):
        assert 0 <= value <= 1
        self.spinbox.setValue(value)

    def _update_slider(self):
        sb_value = self.spinbox.value()
        self.slider.setValue(int(sb_value * 100 - 1))
        self.value_changed.emit(sb_value)

    def _update_spinbox(self):
        new_val = (self.slider.value() + 1) / 100
        self.spinbox.setValue(new_val)
        self.value_changed.emit(new_val)


# noinspection PyUnresolvedReferences
class IndicatedSlider(QWidget):

    value_changed = pyqtSignal(int)

    def __init__(self, n_ticks, parent=None):
        super().__init__(parent)
        layout = QGridLayout()
        self.setLayout(layout)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(1, n_ticks)
        self.slider.setTickInterval(1)
        self.slider.setTickPosition(QSlider.TicksBelow)
        layout.addWidget(self.slider, 0, 0, 1, 3)

        self.label = QLabel(str(self.slider.value()))
        layout.addWidget(self.label, 0, 3, 1, 1)

        self.slider.valueChanged.connect(lambda a: self.label.setText(str(a)))
        self.slider.valueChanged.connect(self.value_changed)

    def value(self) -> int:
        return self.slider.value()


# noinspection PyUnresolvedReferences
class ColorButton(QPushButton):

    color_changed = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(20, 20)
        self.clicked.connect(self.change_color)

    def setStyleSheet(self, p_str):
        super().setStyleSheet(p_str)
        self.show()
        self.setAutoFillBackground(True)

    def change_color(self):
        new_color = QColorDialog.getColor().name()
        self.setStyleSheet(f"background-color: {new_color};"
                           f"border:1px solid rgb(0, 0, 0);")
        self.color_changed.emit(new_color)


# noinspection PyUnresolvedReferences
class DupSpinbox(QWidget):

    value_changed = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout()
        self.setLayout(layout)
        self.sb = QSpinBox()
        self.sb.setSingleStep(10)
        self.label = QLabel(f"x {self.sb.value()}")
        self.sb.valueChanged.connect(lambda a: self.label.setText(f"x {self.sb.value()}"))
        self.sb.valueChanged.connect(self.value_changed)
        layout.addWidget(self.sb)
        layout.addWidget(self.label)
        self.setValue = self.sb.setValue
        self.setRange = self.sb.setRange

    def value(self):
        return self.sb.value()


class CustomTab(QScrollArea):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.horizontalScrollBar().setDisabled(True)
        size_policy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Expanding)
        self.setSizePolicy(size_policy)


if __name__ == '__main__':
    import sys
    from PyQt5.Qt import QApplication

    app = QApplication(sys.argv)
    tab = DupSpinbox()
    tab.setVisible(True)
    sys.exit(app.exec())
