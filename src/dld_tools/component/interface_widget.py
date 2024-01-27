from PySide6.QtWidgets import QSizePolicy, QWidget


class InterfaceWidget(QWidget):

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        size_policy = QSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred
        )
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(15)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
