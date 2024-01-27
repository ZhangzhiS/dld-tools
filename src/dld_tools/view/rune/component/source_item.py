
from collections.abc import Callable
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QCheckBox, QFrame, QHBoxLayout, QLabel, QWidget

class CheckBox(QCheckBox):
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
            width: 30px;
            height: 30px;
            border: none;
        }}

        #{obj_name}::indicator:unchecked {{
            image: url('resources/icon/checkbox.png');
        }}

        #{obj_name}::indicator:checked {{
            image: url('resources/icon/checkbox_checked.png');
        }}
        """
        )


class SourceItemWidget(QFrame):

    def __init__(
        self, parent, name: str, status: bool, action: Callable, title: str
    ):
        super().__init__(parent)
        self.name = name.replace(".", "_")
        self.action = action
        self.installEventFilter(self)
        self.setMaximumHeight(50)
        self.setMinimumHeight(50)
        self.setObjectName(self.name)
        self.click_action = action
        self.h_layout = QHBoxLayout(self)
        self.h_layout.setContentsMargins(10, 0, 10, 0)
        self.__init_ui(title, status)
        self.__connect()

    def __init_ui(self, title, status):
        # 渲染左右两部分
        self.left_widget = QWidget(self)
        self.left_widget_layout = QHBoxLayout(self.left_widget)
        label = QLabel(self.left_widget)
        label.setText(title)
        self.left_widget_layout.addWidget(label)
        self.h_layout.addWidget(self.left_widget, 0, Qt.AlignmentFlag.AlignLeft)
        self.right_widget = QWidget(self)
        self.right_widget_layout = QHBoxLayout(self.right_widget)
        self.check_button = CheckBox(f"{self.name}_switch")
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

    def __checked_changed(self, status):
        self.action(self.name.replace("_", "."), status)

    def __connect(self):
        self.check_button.stateChanged.connect(self.__checked_changed)
