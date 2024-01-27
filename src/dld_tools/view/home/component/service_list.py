from typing import Callable

from dld_tools.component.icon import ItemIcon
from PySide6.QtCore import QEvent, Qt, Signal
from PySide6.QtGui import QColor, QEnterEvent
from PySide6.QtWidgets import (
    QFrame,
    QGraphicsDropShadowEffect,
    QHBoxLayout,
    QLabel,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
    QWidget,
)


class ServiceItemWidget(QFrame):
    """
    配置项
        每个配置项可分为左右两部分
        左边为icon+title+[vip_icon]
        右边为[help_tip]switch
    """

    def __init__(
        self, parent, name: str, icon: str, action: Callable, title: str
    ):
        super().__init__(parent)
        self.name = name
        self.installEventFilter(self)
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
        self.click_action = action
        self.h_layout = QHBoxLayout(self)
        self.h_layout.setContentsMargins(0, 0, 0, 0)
        self.__init_ui(icon, title)

    def __init_ui(self, icon, title):
        # 添加阴影
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setColor(QColor(0, 0, 0, 50))  # 设置阴影的颜色和透明度
        self.shadow.setOffset(1, 4)  # 设置阴影的偏移量
        self.shadow.setBlurRadius(10)  # 设置阴影的模糊半径
        # 将阴影效果应用到 QLabel 上
        self.setGraphicsEffect(self.shadow)

        # 渲染左右两部分
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
        f_icon = ItemIcon("resources/icon/pack_comment.png", 20, self.left_widget)
        self.right_widget_layout.addWidget(f_icon)
        self.h_layout.addWidget(self.right_widget, 0, Qt.AlignmentFlag.AlignRight)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.shadow.setOffset(1, 2)
            self.click_action(self.name)

    def mouseReleaseEvent(self, event) -> None:
        self.shadow.setOffset(1, 5)
        return super().mouseReleaseEvent(event)

    def enterEvent(self, event: QEnterEvent) -> None:
        self.shadow.setOffset(1, 5)
        return super().enterEvent(event)

    def leaveEvent(self, event: QEvent) -> None:
        self.shadow.setOffset(1, 4)
        return super().leaveEvent(event)


class ItemListWidget(QWidget):
    service_signal = Signal(str)

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
        self.rune_service = ServiceItemWidget(
            self, "rune", "rune", self.service_signal.emit, "配置符文来源"
        )
        self.item_list_layout.addWidget(
            self.rune_service, 0, Qt.AlignmentFlag.AlignVCenter
        )
        self.v_layout.addWidget(self.item_list)
        self.spacer_v_item = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )
        self.v_layout.addItem(self.spacer_v_item)
