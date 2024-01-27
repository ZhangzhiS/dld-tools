from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QLabel


class ItemIcon(QLabel):
    def __init__(self, icon: str, diameter, parent=None) -> None:
        super().__init__(parent)

        self.setMaximumSize(diameter, diameter)
        self.setMinimumSize(diameter, diameter)
        self.image = QPixmap(icon)
        self.setPixmap(self.image)
        self.setScaledContents(True)