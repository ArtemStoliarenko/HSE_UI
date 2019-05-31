from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QDir

from collections import OrderedDict
import json
from os.path import dirname, join

from resources import resources


config = json.load(open(join(dirname(__file__), "config.json")),
                   object_pairs_hook=OrderedDict)


def terr_obj_assets():
    dir_path = ":/assets/"
    files = QDir(dir_path).entryList()
    for img in files:
        yield img, QPixmap(dir_path + img)


def icons() -> dict:
    dir_path = ":/icons/"
    return {img: QPixmap(dir_path + img) for img in QDir(dir_path).entryList()}


if __name__ == '__main__':
    import sys
    from PyQt5.Qt import QApplication

    app = QApplication(sys.argv)
    terr_obj_assets()
    sys.exit(app.exec())

