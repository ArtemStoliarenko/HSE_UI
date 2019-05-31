from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtCore import pyqtSignal

from gui.terrain_tab import TerrainTab
from gui.heightmap_tab import HeightMapTab
from gui.assets_tab import AssetsTab
from gui.editing_tab import EditingTab


class TabPanel(QTabWidget):

    lvl_changed = pyqtSignal(str, float)
    gen_submitted = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.terrain_tab = TerrainTab()
        self.assets_tab = AssetsTab()
        self.heightmap_tab = HeightMapTab()
        self.editing_tab = EditingTab()
        #
        self.heightmap_tab.gen_submitted.connect(self.gen_submitted)
        #
        self.addTab(self.heightmap_tab, "Generation")
        self.addTab(self.terrain_tab, "Terrain")
        self.addTab(self.editing_tab, "Editing")
        self.addTab(self.assets_tab, "Assets")


if __name__ == '__main__':
    import sys
    from PyQt5.Qt import QApplication

    app = QApplication(sys.argv)
    tab = TabPanel()
    tab.setVisible(True)
    sys.exit(app.exec())
