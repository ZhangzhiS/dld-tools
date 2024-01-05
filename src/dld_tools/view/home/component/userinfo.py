from typing import Optional
from dld_tools.component.avatar import AvatarLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QHBoxLayout, QLabel, QSizePolicy, QVBoxLayout, QWidget


class UserInfoWidget(QWidget):
    def __init__(self, parent: QWidget, display_name: str, icon_path: str) -> None:
        super().__init__(parent)
        self.setObjectName("userInfo")
        size_policy = QSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred
        )
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(2)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)

        self.userinfo_h_layout = QHBoxLayout(self)
        self.userinfo_h_layout.setObjectName("userinfo_h_layout")
        self.userinfo_h_layout.setSpacing(0)
        self.userinfo_h_layout.setContentsMargins(40, 0, 0, 0)

        self.display_name = display_name
        self.icon_path = icon_path

        self.__init_ui()

    def __init_ui(self):
        # 绘制头像
        self.avatar = AvatarLabel(parent=self)
        self.avatar.painter_avatar(self.icon_path)
        self.userinfo_h_layout.addWidget(self.avatar, 0, Qt.AlignmentFlag.AlignLeft)
        
        # 显示玩家昵称
        self.text_info_layout = QVBoxLayout()
        self.text_info_layout.setContentsMargins(0, 0, 40, 0)
        font = QFont()
        font.setPointSize(16)
        self.nickname = QLabel(self)
        self.nickname.setFont(font)
        self.nickname.setText(self.display_name)
        self.text_info_layout.addWidget(
            self.nickname,
            0,
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter,
        )
        self.userinfo_h_layout.addLayout(self.text_info_layout)

    def refresh_userinfo(
        self,
        icon_path: str,
        nickname: str,
    ):
        self.avatar.clear()
        self.avatar.painter_avatar(icon_path)
        self.nickname.setText(nickname)
