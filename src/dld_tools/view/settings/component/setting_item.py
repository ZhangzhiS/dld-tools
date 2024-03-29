from typing import Callable
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QCheckBox, QFrame, QHBoxLayout, QLabel, QWidget
from dld_tools.component.icon import ItemIcon


class SwitchButton(QCheckBox):
    def __init__(self, obj_name: str):
        super().__init__()
        self.setObjectName(obj_name)
        self.setStyleSheet(
            f"""
        #{obj_name} {{
            font-size: 15px;
        }}

        #{obj_name}::indicator {{
            padding-top: 1px;
            width: 40px;
            height: 30px;
            border: none;
        }}

        #{obj_name}::indicator:unchecked {{
            image: url('resources/icon/switch_off.png');
        }}

        #{obj_name}::indicator:checked {{
            image: url('resources/icon/switch_on.png');
        }}
        """
        )


class SettingItem(QFrame):

    def __init__(
        self, parent, name: str, icon: str, status: bool, action: Callable, title: str
    ):
        super().__init__(parent)
        self.setMaximumHeight(50)
        self.setMinimumHeight(50)
        self.setObjectName(name)
        self.name = name
        self.h_layout = QHBoxLayout(self)
        self.h_layout.setContentsMargins(0, 0, 0, 0)
        self.__init_ui(icon, status, title)
        self.__connect(action)

    def __init_ui(self, icon, status, title):
        self.left_widget = QWidget(self)
        self.left_widget_layout = QHBoxLayout(self.left_widget)
        l_icon = ItemIcon(f"resources/icon/{icon}.png", 20, self.left_widget)
        self.left_widget_layout.addWidget(l_icon)
        label = QLabel(self.left_widget)
        label.setText(title)
        self.left_widget_layout.addWidget(label)
        self.h_layout.addWidget(self.left_widget, 0, Qt.AlignmentFlag.AlignLeft)
        self.right_widget = QWidget(self)
        self.right_widget_layout = QHBoxLayout(self.right_widget)
        self.right_widget_layout.setContentsMargins(0, 0, 25, 0)
        self.check_button = SwitchButton(f"{self.name}_switch")
        self.check_button.setChecked(status)
        self.right_widget_layout.addWidget(self.check_button)
        self.h_layout.addWidget(self.right_widget, 0, Qt.AlignmentFlag.AlignRight)
        self.__set_style()

    def __set_style(self):
        self.setStyleSheet(
            f"""
        #{self.name} {{
            background-color: rgb(255,255,255);
            border-radius: 15px;
        }}
        """
        )

    def __connect(self, action):
        self.check_button.stateChanged.connect(action)
