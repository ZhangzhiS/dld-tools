from typing import Callable
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QLabel, QSizePolicy, QVBoxLayout, QHBoxLayout, QWidget, QCheckBox, QSpacerItem
from dld_tools.component.icon import ItemIcon


class ServiceItemWidget(QFrame):
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
        self.check_button = QCheckBox()
        self.check_button.setChecked(self.status)
        self.right_widget_layout.addWidget(self.check_button)
        self.h_layout.addWidget(self.right_widget, 0, Qt.AlignmentFlag.AlignRight)

    def __connect(self):
        self.check_button.stateChanged.connect(self.check_action)


class ItemListWidget(QWidget):
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.setObjectName("serverList")
        size_policy = QSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred
        )
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(5)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.v_layout = QVBoxLayout(self)
        self.v_layout.setContentsMargins(20, 1, 20, 12)
        self.__init_ui()
        
    def __init_ui(self):
        self.item_list = QWidget(self)
        self.item_list_layout = QVBoxLayout(self.item_list)
        self.rune_service = ServiceItemWidget(self, "rune", "rune", True, lambda: 1+2, "自定义符文")

        # self.label = QLabel("其他功能区")
        self.item_list_layout.addWidget(
            self.rune_service, 0, Qt.AlignmentFlag.AlignVCenter
        )

        self.v_layout.addWidget(self.item_list)
        self.spacer_v_item = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )
        self.v_layout.addItem(self.spacer_v_item)

    def __set_style(self):
        pass