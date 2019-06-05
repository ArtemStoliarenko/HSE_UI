from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import \
    QGridLayout, \
    QWidget, \
    QLabel, \
    QPushButton, \
    QSpinBox, \
    QVBoxLayout, \
    QDoubleSpinBox

from gui.custom_widgets import \
    IndicatedSlider, \
    SliderSpinBox, \
    DupSpinbox, \
    CustomTab
from mapgenerator.utils import config


# noinspection PyUnresolvedReferences
class HeightMapTab(CustomTab):

    gen_submitted = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        main_widget = QWidget()
        high_level_layout = QVBoxLayout()
        container = QWidget()
        container.setLayout(high_level_layout)
        layout = QGridLayout()
        main_widget.setLayout(layout)
        row = 0
        # Map dimensions
        dim_label = QLabel("Map size (px)")
        self.dim_sb = DupSpinbox()
        self.dim_sb.setRange(0, 2048)
        self.dim_sb.setValue(512)
        layout.addWidget(dim_label, row, 0)
        layout.addWidget(self.dim_sb, row, 1)
        row += 1
        # Scale
        scale_label = QLabel("Scale")
        self.scale_sb = SliderSpinBox()
        self.scale_sb.slider.setSingleStep(0.05)
        self.scale_sb.set_value(1)
        layout.addWidget(scale_label, row, 0)
        layout.addWidget(self.scale_sb, row, 1)
        row += 1
        # Octaves
        max_octaves = int(config["max_octaves"])
        self.oct_slider = IndicatedSlider(max_octaves)
        oct_label = QLabel("Octaves:")
        layout.addWidget(oct_label, row, 0)
        layout.addWidget(self.oct_slider, row, 1)
        row += 1
        # Persistence
        self.pers_slider = SliderSpinBox()
        self.pers_slider.set_value(0.5)
        pers_label = QLabel("Persistence:")
        layout.addWidget(pers_label, row, 0)
        layout.addWidget(self.pers_slider, row, 1)
        row += 1
        # Period
        x_period_label = QLabel("X axis repeat period")
        self.x_period_sb = QSpinBox()
        self.x_period_sb.setRange(10, 2048)
        self.x_period_sb.setValue(2048)
        self.x_period_sb.setSingleStep(10)
        layout.addWidget(x_period_label, row, 0)
        layout.addWidget(self.x_period_sb, row, 1)
        row += 1

        y_period_label = QLabel("Y axis repeat period")
        self.y_period_sb = QSpinBox()
        self.y_period_sb.setRange(10, 2048)
        self.y_period_sb.setValue(2048)
        self.y_period_sb.setSingleStep(10)
        layout.addWidget(y_period_label, row, 0)
        layout.addWidget(self.y_period_sb, row, 1)
        row += 1
        #
        generate_button = QPushButton("Generate")
        generate_button.clicked.connect(self._on_submitted)
        layout.addWidget(generate_button, row, 0, 2, 2)
        #
        high_level_layout.addWidget(main_widget)
        high_level_layout.addStretch(2)
        self.setWidget(container)

    def _on_submitted(self):
        state = {
            "dim": self.dim_sb.value(),
            "scale": self.scale_sb.value(),
            "octaves": self.oct_slider.value(),
            "persistence": self.pers_slider.value(),
            "x_period": self.x_period_sb.value(),
            "y_period": self.y_period_sb.value()
        }
        self.gen_submitted.emit(state)


if __name__ == '__main__':
    import sys
    from PyQt5.Qt import QApplication

    app = QApplication(sys.argv)
    tab = HeightMapTab()
    tab.setVisible(True)
    sys.exit(app.exec())
