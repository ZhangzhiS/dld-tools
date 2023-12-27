from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QLabel, QSizePolicy, QWidget


class Footer(QWidget):
    def __init__(self, parent: QWidget, version: str) -> None:
        super().__init__(parent)
        self.setObjectName("footer")
        size_policy = QSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred
        )
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(1)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.footer_layout = QHBoxLayout(self)
        self.footer_layout.setSpacing(0)
        self.footer_layout.setContentsMargins(0, 0, 0, 20)
        self.label = QLabel(self)
        self.label.setObjectName("version_label")
        self.label.setText("Version:")
        self.footer_layout.addWidget(self.label, 0, Qt.AlignmentFlag.AlignRight)
        self.version = QLabel(self)
        self.version.setObjectName("version")
        self.version.setText(version)
        self.footer_layout.addWidget(self.version, 0, Qt.AlignmentFlag.AlignLeft)
