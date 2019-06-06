from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import \
    QGroupBox, \
    QGridLayout, \
    QVBoxLayout, \
    QCheckBox, \
    QWidget, \
    QLabel, \
    QTableWidget, \
    QSizePolicy, \
    QDoubleSpinBox, \
    QHBoxLayout, \
    QAbstractItemView, QHeaderView
from gui.custom_widgets import ColorButton, IndSliderWithDoubleSpinBox, CustomTab
from mapgenerator.utils import config


# noinspection PyUnresolvedReferences
class TerrainTab(QWidget):

    lvl_changed = pyqtSignal(str, float)
    biome_disabled = pyqtSignal(str)
    biome_enabled = pyqtSignal(str)
    biome_color_changed = pyqtSignal(str, str)
    settings_updated = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        # self.horizontalScrollBar().setEnabled(True)
        biomes = config["biomes"]
        # container = QWidget()
        container_layout = QHBoxLayout()
        # container.setLayout(container_layout)
        terrain_tab = QTableWidget(len(biomes), 4)
        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        terrain_tab.setSizePolicy(size_policy)
        # container.setSizePolicy(size_policy)
        #
        terrain_tab.verticalHeader().hide()
        terrain_tab.setHorizontalHeaderLabels(["Enabled", "Biome", "Color", "Level"])
        terrain_tab.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        #
        biomes = config["biomes"]
        self.color_buttons = []
        self.lvl_selectors = []
        self.checkboxes = []
        self.labels = []
        for n, biome in enumerate(biomes):
            biome_name = biome["name"]
            #
            cb_container = QWidget()
            cb_layout = QHBoxLayout()
            cb_container.setLayout(cb_layout)
            checkbox = QCheckBox()
            checkbox.setChecked(True)
            checkbox.stateChanged.connect(self._cb_on_state_changed(biome_name, n))
            cb_layout.addStretch(2)
            cb_layout.addWidget(checkbox)
            cb_layout.addStretch(2)
            terrain_tab.setCellWidget(n, 0, cb_container)
            self.checkboxes.append(checkbox)
            #
            name_label = QLabel(biome_name)
            terrain_tab.setCellWidget(n, 1, name_label)
            self.labels.append(name_label)
            #
            color_button = ColorButton()
            color_button.set_color(biome['color'])
            color_button.color_changed.connect(self._on_color_changed(biome_name))
            terrain_tab.setCellWidget(n, 2, color_button)
            self.color_buttons.append(color_button)
            #
            # lvl_sb = IndSliderWithDoubleSpinBox()
            lvl_sb = QDoubleSpinBox()
            lvl_sb.setRange(0, 1)
            lvl_sb.setSingleStep(0.01)
            lvl_sb.setValue(float(biome["base_lvl"]))
            terrain_tab.setCellWidget(n, 3, lvl_sb)
            self.lvl_selectors.append(lvl_sb)
            #
            # terrain_tab.setFocusPolicy(Qt.NoFocus)
        terrain_tab.resizeRowsToContents()
        terrain_tab.setSelectionMode(QAbstractItemView.NoSelection)
        terrain_tab.horizontalHeader().setSectionsClickable(False)
        container_layout.addWidget(terrain_tab)
        self.terrain_tab = terrain_tab
        self.setLayout(container_layout)
        self.state = {}
        self.update_state()
        #
        self.lvl_changed.connect(self.emit_state)
        self.biome_color_changed.connect(self.emit_state)
        self.biome_enabled.connect(self.emit_state)
        self.biome_disabled.connect(self.emit_state)

    def _set_row_state(self, row_num: int, state: bool):
        for col in range(1, self.terrain_tab.columnCount()):
            self.terrain_tab.cellWidget(row_num, col).setEnabled(state)

    def _cb_on_state_changed(self, name: str, row_num: int):
        def handler(value):
            if value:
                self.biome_enabled.emit(name)
                self.state[name]["enabled"] = True
                self._set_row_state(row_num, True)
            else:
                self.biome_disabled.emit(name)
                self.state[name]["enabled"] = False
                self._set_row_state(row_num, False)
        return handler

    def _on_color_changed(self, name):
        def handler(value):
            self.state[name]["color"] = value
            self.biome_color_changed.emit(name, value)
        return handler

    def _on_lvl_changed(self, name):
        def handler(value):
            self.state[name]["level"] = value
            self.lvl_changed.emit(name, value)
        return handler

    def color_height_dict(self) -> dict:
        res = {}
        for n, cb in enumerate(self.color_buttons):
            res[cb.color()] = self.lvl_selectors[n].value()
        return res

    def update_state(self):
        state = {}
        for n, biome_label in enumerate(self.labels):
            state[biome_label.text()] = {
                "color": self.color_buttons[n].color(),
                "enabled": self.checkboxes[n].isChecked(),
                "level": self.lvl_selectors[n].value(),
            }
        self.state = state

    def emit_state(self, *args):
        self.settings_updated.emit(self.state)


if __name__ == '__main__':
    import sys
    from PyQt5.Qt import QApplication

    app = QApplication(sys.argv)
    tab = TerrainTab()
    tab.setVisible(True)
    sys.exit(app.exec())
