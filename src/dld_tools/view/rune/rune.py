# 配置符文来源

from dld_tools.component.interface_widget import InterfaceWidget
from dld_tools.core.config import cfg
from PySide6.QtWidgets import QSizePolicy, QSpacerItem, QVBoxLayout, QWidget

from dld_tools.tools.data_source import DATASOURCE
from dld_tools.view.rune.component.source_item import SourceItemWidget


class RuneSourceInterface(InterfaceWidget):
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.setObjectName("rune")
        self.__init_ui()

    def __init_ui(self):
        self.v_layout = QVBoxLayout(self)
        self.v_layout.setSpacing(0)
        self.v_layout.setContentsMargins(20, 20, 20, 20)

        self.item_widget = QWidget(self)
        self.item_widget.setObjectName("itemList")
        self.item_widget_layout = QVBoxLayout(self.item_widget)
        self.item_widget_layout.setContentsMargins(12, 12, 12, 12)

        for i in list(DATASOURCE):
            if i.value in cfg.DataSource:
                tmp = SourceItemWidget(
                    self, i.value, cfg.DataSource.get(i.value, False), self.change_config, i.value
                )
                self.item_widget_layout.addWidget(tmp)
            else:
                tmp = SourceItemWidget(
                    self, i.value, False, self.change_config, i.value
                )
                self.item_widget_layout.addWidget(tmp)

        self.v_layout.addWidget(self.item_widget, 0)
        self.spacer_v_item = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )
        self.item_widget_layout.addItem(self.spacer_v_item)

    def change_config(self, data_source, status):
        cfg.DataSource[data_source] = bool(status)
        cfg.save()
