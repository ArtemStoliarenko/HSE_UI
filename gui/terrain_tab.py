from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import \
    QGroupBox, \
    QGridLayout, \
    QVBoxLayout, \
    QCheckBox, \
    QWidget, \
    QLabel
from gui.custom_widgets import ColorButton, SliderSpinBox, CustomTab
from mapgenerator.utils import config


# noinspection PyUnresolvedReferences
class TerrainTab(CustomTab):

    lvl_changed = pyqtSignal(str, float)
    biome_disabled = pyqtSignal(str)
    biome_enabled = pyqtSignal(str)
    biome_color_changed = pyqtSignal(str, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        terrain_tab = QWidget()
        tab_layout = QVBoxLayout()
        terrain_tab.setLayout(tab_layout)
        biomes = config["biomes"]
        for biome in biomes:
            biome_widget = QGroupBox()
            biome_name = biome["name"]
            biome_widget.setTitle(biome_name)
            layout = QGridLayout()
            biome_widget.setLayout(layout)
            #
            checkbox = QCheckBox("Enabled")
            checkbox.setChecked(True)
            checkbox.stateChanged.connect(self._cb_on_state_changed(biome_name))
            layout.addWidget(checkbox, 0, 0)
            #
            layout.addWidget(QLabel("Biome color"), 1, 0)
            color_button = ColorButton()
            layout.addWidget(color_button, 1, 2)
            color_button.setStyleSheet(f"background-color: {biome['color']};"
                                       f"border:1px solid black;")
            color_button.color_changed.connect(self._on_color_changed(biome_name))
            #
            layout.addWidget(QLabel("Level:"), 2, 0)
            ssb = SliderSpinBox()
            ssb.set_value(float(biome["base_lvl"]))
            layout.addWidget(ssb, 3, 0, 1, 4)
            #
            tab_layout.addWidget(biome_widget)
        self.setWidget(terrain_tab)

    def _cb_on_state_changed(self, name):
        def handler(value):
            if value:
                self.biome_enabled.emit(name)
            else:
                self.biome_disabled.emit(name)
        return handler

    def _on_color_changed(self, name):
        def handler(value):
            self.biome_color_changed.emit(name, value)
        return handler

    def _on_lvl_changed(self, name):
        def handler(value):
            self.lvl_changed.emit(name, value)
        return handler


if __name__ == '__main__':
    import sys
    from PyQt5.Qt import QApplication

    app = QApplication(sys.argv)
    tab = TerrainTab()
    tab.setVisible(True)
    sys.exit(app.exec())
