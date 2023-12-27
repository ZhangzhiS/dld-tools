from typing import Callable
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QWidget,
)


class MenuBarBtn(QPushButton):
    """
    自定义菜单按钮
    统一尺寸和点击效果
    """

    def __init__(self, name, parent) -> None:
        super().__init__(parent)
        self.setObjectName(name)
        q_size_policy = QSizePolicy(
            QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed
        )
        q_size_policy.setHorizontalStretch(0)
        q_size_policy.setVerticalStretch(0)
        q_size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(q_size_policy)
        self.setMaximumSize(30, 30)
        self.setMinimumSize(30, 30)
        self.setStyleSheet(
            f"""
            #{name} {{
                border: none;
            }}
            #{name}:hover {{
                padding-bottom:4px;
            }}
            """
        )
        icon = QPixmap(f"resources/icon/{name}.png")
        self.setIcon(icon)


class MenuBar(QWidget):
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.setParent(parent)
        self.setObjectName("menu")

        # 设置菜单在main布局中的拉伸策略
        # 水平方向不设置，垂直设置为1
        size_policy = QSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred
        )
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(1)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)

        self.menu_h_layout = QHBoxLayout(self)
        self.menu_h_layout.setObjectName("menu_h_layout")
        self.menu_h_layout.setSpacing(0)
        self.menu_h_layout.setContentsMargins(15, 0, 5, 0)

        self.title = QLabel(self)
        self.title.setText("大乱斗助手")
        self.menu_h_layout.addWidget(self.title)

        self.h_space = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )
        self.menu_h_layout.addItem(self.h_space)

        self.question_btn = MenuBarBtn("question", self)
        self.menu_h_layout.addWidget(self.question_btn)
        self.settings_btn = MenuBarBtn("settings", self)
        self.menu_h_layout.addWidget(self.settings_btn)
        self.close_btn = MenuBarBtn("close", self)
        self.menu_h_layout.addWidget(self.close_btn)

        self.settings_btn.hide()
        self.question_btn.hide()

    def menu_btn_connect(self, btn: QPushButton, func: Callable):
        """
        按钮绑定点击函数
        先断开旧链接
        """
        if btn.property("clicked_connect"):
            btn.clicked.disconnect()
        btn.clicked.connect(func)
        btn.setProperty("clicked_connect", True)







