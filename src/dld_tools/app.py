"""
My first application
"""
import os
import sys
from importlib import metadata as importlib_metadata

from PySide6 import QtWidgets
from PySide6.QtGui import QIcon

from dld_tools.view.main_window import MainWindow


def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    app_module = sys.modules["__main__"].__package__ or ""
    # Retrieve the app's metadata
    metadata = importlib_metadata.metadata(app_module)

    QtWidgets.QApplication.setApplicationName(metadata["Formal-Name"])
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow(metadata["Version"])  # noqa
    main_window.show()
    app.setWindowIcon(QIcon("resources/dld-tools.png"))
    sys.exit(app.exec())
