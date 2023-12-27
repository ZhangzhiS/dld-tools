from typing import Optional
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QHBoxLayout, QLabel, QSizePolicy, QWidget

from dld_tools.tools.lol.data_schema import SummonerGamesInfo


class RecentInfoWidget(QWidget):
    """
    分为四部分内容，对局label，对局数据比，KDA的labe，KDA数据
    """

    def __init__(self, parent: QWidget, games_info: SummonerGamesInfo) -> None:
        super().__init__(parent)
        self.setObjectName("recentInfo")
        size_policy = QSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred
        )
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(1)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)

        self.__init_ui()
        self.refresh_info(games_info)

    def __init_ui(self):

        self.h_layout = QHBoxLayout(self)
        self.h_layout.setContentsMargins(30,12,30,12)

        self.recent_bar_widget = QWidget(self)
        self.recent_bar_widget.setObjectName("recentBar")
        self.recent_bar_widget.setStyleSheet(
            """#recentBar {
            background-color: rgb(255, 255, 255);
            border-radius: 10px;
            }"""
        )
        self.recent_bar_layout = QHBoxLayout(self.recent_bar_widget)
        self.recent_bar_layout.setSpacing(0)
        self.recent_bar_layout.setContentsMargins(12, 0, 12, 0)

        self.h_layout.addWidget(self.recent_bar_widget)
        self.render_win_vs_lose()
        self.render_kda()

    def render_win_vs_lose(self):
        """
        近20场胜负数据组件
        """
        self.win_lose_widget = QWidget(self.recent_bar_widget)
        self.win_lose_layout = QHBoxLayout(self.win_lose_widget)
        self.win_lose_layout.setContentsMargins(0, 0, 0, 0)
        self.win_lose_layout.setSpacing(0)

        font = QFont()
        font.setBold(True)
        self.win_vs_lose_label = QLabel(self.win_lose_widget)
        self.win_vs_lose_label.setFont(font)
        self.win_lose_layout.addWidget(self.win_vs_lose_label, 0)
        self.win_vs_lose_label.setText("近20场对局：")
        self.win_num = QLabel(self.win_lose_widget)
        self.win_num.setText("0")
        self.win_num.setStyleSheet("""color: rgb(65,174,60);""")
        self.win_lose_layout.addWidget(self.win_num, 0)
        slash1 = QLabel(self.win_lose_widget)
        slash1.setText("/")
        self.win_lose_layout.addWidget(slash1, 0)
        self.lose_num = QLabel(self.win_lose_widget)
        self.lose_num.setText("0")
        self.lose_num.setStyleSheet("""color: rgb(204,22,58);""")
        self.win_lose_layout.addWidget(self.lose_num, 0)
        self.recent_bar_layout.addWidget(
            self.win_lose_widget, 0, Qt.AlignmentFlag.AlignHCenter
        )

    def render_kda(self):
        """
        KDA组件
        """
        self.kda_widget = QWidget(self.recent_bar_widget)
        self.kda_layout = QHBoxLayout(self.kda_widget)
        self.kda_layout.setContentsMargins(0,0,0,0)
        self.kda_layout.setSpacing(0)
        font = QFont()
        font.setBold(True)
        self.kda_label = QLabel(self)
        self.kda_label.setFont(font)
        self.kda_layout.addWidget(self.kda_label, 0)
        self.kda_label.setText("KDA：")
        self.k = QLabel(self)
        self.k.setText("0")
        self.kda_layout.addWidget(self.k, 0)
        slash1 = QLabel(self)
        slash1.setText("/")
        self.kda_layout.addWidget(slash1, 0)
        self.d = QLabel(self)
        self.d.setText("0")
        self.kda_layout.addWidget(self.d, 0)
        slash1 = QLabel(self)
        slash1.setText("/")
        self.kda_layout.addWidget(slash1, 0)
        self.a = QLabel(self)
        self.a.setText("0")
        self.kda_layout.addWidget(self.a, 0)
        self.recent_bar_layout.addWidget(
            self.kda_widget, 0, Qt.AlignmentFlag.AlignHCenter
        )

    def refresh_info(self, games_info: Optional[SummonerGamesInfo]):
        k = 0
        d = 0
        a = 0
        win = 0
        lose = 0
        if games_info:
            for game in games_info.games.games:
                stats = game.participants[0].stats
                k += stats.kills
                d += stats.deaths
                a += stats.assists
                if stats.win:
                    win += 1
                else:
                    lose += 1

        self.k.setText(str(k))
        self.d.setText(str(d))
        self.a.setText(str(a))
        self.win_num.setText(str(win))
        self.lose_num.setText(str(lose))

