from typing import Callable
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QCheckBox, QFrame, QHBoxLayout, QLabel, QWidget


class ItemIcon(QLabel):
    def __init__(self, icon, diameter, parent=None) -> None:
        super().__init__(parent)

        self.setMaximumSize(diameter, diameter)
        self.setMinimumSize(diameter, diameter)
        self.image = QPixmap(icon)
        self.setPixmap(self.image)
        self.setScaledContents(True)


class CheckBox(QCheckBox):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(
            """
        QCheckBox {
            font-size: 15px;
        }

        QCheckBox::indicator {
            padding-top: 1px;
            width: 40px;
            height: 30px;
            border: none;
        }

        QCheckBox::indicator:unchecked {
            image: url('resources/icon/switch_off.png');
        }

        QCheckBox::indicator:checked {
            image: url('resources/icon/switch_on.png');
        }
        """
        )


class SettingItem(QFrame):
    """
    配置项
        每个配置项可分为左右两部分
        左边为icon+title+[vip_icon]
        右边为[help_tip]switch
    """

    def __init__(
        self, parent, name: str, icon: str, status: bool, action: Callable, title: str
    ):
        super().__init__(parent)
        self.setMaximumHeight(50)
        self.setMinimumHeight(50)
        self.setObjectName(name)
        self.setStyleSheet(
            f"""
        #{name} {{
            background-color: rgb(255,255,255);
            border-radius: 15px;
        }}
        """
        )
        self.icon = icon
        self.check_action = action
        self.status = status
        self.h_layout = QHBoxLayout(self)
        self.h_layout.setContentsMargins(0, 0, 0, 0)
        self.title = title
        self.render_left()
        self.render_right()
        self.__connect()

    def render_left(self):
        self.left_widget = QWidget(self)
        self.left_widget_layout = QHBoxLayout(self.left_widget)
        icon = ItemIcon(f"resources/icon/{self.icon}.png", 20, self.left_widget)
        self.left_widget_layout.addWidget(icon)
        label = QLabel(self.left_widget)
        label.setText(self.title)
        self.left_widget_layout.addWidget(label)
        self.h_layout.addWidget(self.left_widget, 0, Qt.AlignmentFlag.AlignLeft)

    def render_right(self):
        self.right_widget = QWidget(self)
        self.right_widget_layout = QHBoxLayout(self.right_widget)
        self.right_widget_layout.setContentsMargins(0, 0, 25, 0)
        self.check_button = CheckBox()
        self.check_button.setChecked(self.status)
        self.right_widget_layout.addWidget(self.check_button)
        self.h_layout.addWidget(self.right_widget, 0, Qt.AlignmentFlag.AlignRight)

    def __connect(self):
        self.check_button.stateChanged.connect(self.check_action)
