from PySide6.QtWidgets import QSizePolicy, QSpacerItem, QVBoxLayout, QWidget

from dld_tools.view.settings.component.setting_item import SettingItem
from dld_tools.core.config import cfg


class SettingsInterface(QWidget):
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.setObjectName("settings")
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

        self.render_auto_accept()
        self.render_close_to_tray()

        self.v_layout.addWidget(self.item_widget, 0)
        self.spacer_v_item = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )
        self.item_widget_layout.addItem(self.spacer_v_item)

    def __auto_accept_changed(self, status):
        cfg.AutoAcceptGame = bool(status)
        cfg.save()

    def __close_to_tray_changed(self, status):
        cfg.CloseToTray = bool(status)
        cfg.save()

    def render_auto_accept(self):
        self.auto_accept = SettingItem(
            parent=self.item_widget,
            name="auto_accept",
            icon="flash",
            status=cfg.AutoAcceptGame,
            action=self.__auto_accept_changed,
            title="自动接受对局"
        )
        self.item_widget_layout.addWidget(self.auto_accept)

    def render_close_to_tray(self):
        self.close_to_tray = SettingItem(
            parent=self.item_widget,
            name="close_to_tray",
            icon="quit",
            status=cfg.CloseToTray,
            action=self.__close_to_tray_changed,
            title="关闭到菜单栏"
        )
        self.item_widget_layout.addWidget(self.close_to_tray)
