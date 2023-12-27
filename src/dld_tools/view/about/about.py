from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QSizePolicy, QSpacerItem, QVBoxLayout, QWidget


class AboutInterface(QWidget):
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.setObjectName("about")
        size_policy = QSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred
        )
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(15)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)

        self.v_layout = QVBoxLayout(self)
        self.v_layout.setSpacing(0)
        self.v_layout.setContentsMargins(20, 20, 20, 20)

        self.item_widget = QWidget(self)
        self.item_widget.setObjectName("itemList")
        self.item_widget_layout = QVBoxLayout(self.item_widget)
        self.item_widget_layout.setContentsMargins(12, 12, 12, 12)

        self.item_widget_layout.addWidget(
            QLabel("关于"),
            0,
            Qt.AlignmentFlag.AlignCenter
        )


        self.v_layout.addWidget(self.item_widget, 0)
        self.spacer_v_item = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )
        self.item_widget_layout.addItem(self.spacer_v_item)

