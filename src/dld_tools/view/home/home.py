from PySide6.QtWidgets import QSizePolicy, QVBoxLayout, QWidget
from dld_tools.component.interface_widget import InterfaceWidget
from dld_tools.tools.lol.data_schema import CurrentSummoner, SummonerGamesInfo
from dld_tools.view.home.component.recent_info import RecentInfoWidget
from dld_tools.view.home.component.service_list import ItemListWidget

from dld_tools.view.home.component.userinfo import UserInfoWidget


class HomeInterface(InterfaceWidget):
    """主页组件"""

    def __init__(
        self, parent: QWidget, userinfo: CurrentSummoner, recent_info: SummonerGamesInfo
    ) -> None:
        super().__init__(parent)
        self.setObjectName("home")
        self.userinfo = userinfo
        self.recent_info = recent_info

        self.__init_ui()

    def __init_ui(self):
        home_layout = QVBoxLayout(self)
        # 设置组件间距以及边距
        home_layout.setSpacing(0)
        home_layout.setContentsMargins(0, 0, 0, 0)

        # 用户头像昵称
        self.userinfo_widget = UserInfoWidget(
            self, self.userinfo.displayName, self.userinfo.icon_path or ""
        )
        home_layout.addWidget(self.userinfo_widget)

        # 最近对局情况
        self.recent_widget = RecentInfoWidget(self, games_info=self.recent_info)
        home_layout.addWidget(self.recent_widget)

        self.server_list_widget = ItemListWidget(self)
        home_layout.addWidget(self.server_list_widget)

        # self.userinfo_single_thread.connect(self.userinfo_widget.refresh_userinfo)
        # self.match_game_single_thread.connect(self.recent_widget.refresh_info)

    def refresh_recent_info(self, games_info: SummonerGamesInfo):
        self.recent_widget.refresh_info(games_info)

    def refresh_userinfo(self, userinfo: dict):
        self.userinfo_widget.refresh_userinfo(
            userinfo["displayName"], userinfo["Avatar"]
        )
