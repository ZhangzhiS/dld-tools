from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMenu, QSystemTrayIcon


class CustomTrayIcon(QSystemTrayIcon):
    open_app_signal = Signal()
    exit_app_signal = Signal()

    def __init__(self, parent: QObject) -> None:
        super().__init__(parent)
        self.setIcon(QIcon("resources/dld-tools.png"))

        self.menu = QMenu()
        self.menu.triggered.connect(self.__activate)
        self.action_open = self.menu.addAction("首页")
        self.action_open.triggered.connect(self.__open_app)
        self.action_exit = self.menu.addAction("退出")
        self.action_exit.triggered.connect(self.__exit_app)
        self.activated.connect(self.__activate)

        self.setContextMenu(self.menu)

    def __activate(self, reason) -> None:
        pass

    def __open_app(self) -> None:
        self.open_app_signal.emit()

    def __exit_app(self) -> None:
        self.exit_app_signal.emit()
