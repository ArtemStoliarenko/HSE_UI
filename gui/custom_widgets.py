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
    QSizePolicy, QStackedLayout, QStackedWidget
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QMouseEvent, QFocusEvent, QPalette


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

    def __init__(self, n_ticks: int, parent=None):
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

        self.slider.valueChanged.connect(self._set_label)
        self.slider.valueChanged.connect(self.value_changed)

    @pyqtSlot(int)
    def _set_label(self, value: int):
        self.label.setText(str(value))

    def value(self) -> int:
        return self.slider.value()

    @pyqtSlot(int)
    def set_value(self, value: int):
        self.slider.setValue(value)


class MyDSpinBox(QDoubleSpinBox):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setAttribute(Qt.WA_NoMousePropagation, True)

    def focusOutEvent(self, e: QFocusEvent):
        e.accept()


class IndSliderWithDoubleSpinBox(QStackedWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setFocusPolicy(Qt.ClickFocus)
        self.ind_slider = IndicatedSlider(5, parent=self)
        self.ind_slider.slider.setRange(1, 100)
        self.ind_slider.slider.setTickPosition(QSlider.NoTicks)
        self.ind_slider.slider.disconnect()
        self.ind_slider.slider.valueChanged.connect(self._update_spinbox)
        self.ind_slider.slider.valueChanged.connect(self._set_label_with_int)
        self.ind_slider.label.setText("0.01")
        self.addWidget(self.ind_slider)
        #
        self.spinbox = MyDSpinBox(parent=self)
        self.spinbox.setValue(0.01)
        self.spinbox.setRange(0, 1)
        self.spinbox.setSingleStep(0.01)
        self.spinbox.valueChanged.connect(self._update_slider)
        self.spinbox.valueChanged.connect(self._set_label_with_float)
        self.addWidget(self.spinbox)

    @pyqtSlot(float)
    def _update_slider(self, value: float):
        self.ind_slider.slider.blockSignals(True)
        # print(f"updating slider: {value} -> {int(value * 100)}")
        self.ind_slider.slider.setValue(int(value * 100))
        self.ind_slider.slider.blockSignals(False)

    @pyqtSlot(int)
    def _update_spinbox(self, value: int):
        self.spinbox.blockSignals(True)
        # print(f"updating spinbox: {value} -> {value / 100}")
        self.spinbox.setValue(value / 100)
        self.spinbox.blockSignals(False)

    @pyqtSlot(int)
    def _set_label_with_int(self, value: int):
        self.ind_slider.label.setText("{:.2f}".format(value / 100, 2))

    @pyqtSlot(float)
    def _set_label_with_float(self, value: float):
        self.ind_slider.label.setText("{:.2f}".format(value, 2))

    def mouseDoubleClickEvent(self, a0: QMouseEvent):
        self.setCurrentIndex(1)

    def focusOutEvent(self, a0: QFocusEvent):
        print("Focus out event received")
        self.setCurrentIndex(0)

    def setValue(self, value: float):
        self.spinbox.setValue(value)


# noinspection PyUnresolvedReferences
class ColorButton(QPushButton):
    color_changed = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(20, 20)
        self.clicked.connect(self.change_color)
        size_policy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.setSizePolicy(size_policy)

    def set_color(self, color: str):
        self.setStyleSheet(f"background-color: {color};"
                           f"border:1px solid black;")

    def setStyleSheet(self, p_str):
        super().setStyleSheet(p_str)
        # self.show()
        self.setAutoFillBackground(True)

    def change_color(self):
        initial = self.palette().color(QPalette.Background)
        new_color = QColorDialog.getColor(initial)
        if new_color.isValid():
            self.setStyleSheet(f"background-color: {new_color.name()};"
                               f"border:1px solid rgb(0, 0, 0);")
            self.color_changed.emit(new_color.name())


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
        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setSizePolicy(size_policy)
        self.setWidgetResizable(True)


if __name__ == '__main__':
    import sys
    from PyQt5.Qt import QApplication

    app = QApplication(sys.argv)
    w = IndSliderWithDoubleSpinBox()
    w.setVisible(True)
    sys.exit(app.exec())
