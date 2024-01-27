import threading

from dld_tools.component.footer import Footer
from dld_tools.component.menu_bar import MenuBar
from dld_tools.component.refresh import QtBoxFuncProgressBar
from dld_tools.component.tray import CustomTrayIcon
from dld_tools.core.config import cfg
from dld_tools.tools.lol.connector import lol_connector
from dld_tools.tools.lol.data_schema import (
    CurrentSummoner,
    GameFlowEvent,
    LolReadyCheckResponse,
    SummonerGamesInfo,
)
from dld_tools.tools.lol.listener import LOLEventListener, LOLProcessListener
from dld_tools.tools.lol.utils import parse_lol_auth_info
from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget
from dld_tools.view.about.about import AboutInterface

from dld_tools.view.home.home import HomeInterface
from dld_tools.view.rune.rune import RuneSourceInterface
from dld_tools.view.settings.settings import SettingsInterface

WINDOW_WIDTH = 375
WINDOW_HEIGHT = 600
MAIN_WINDOW_QSIZE = QSize(WINDOW_WIDTH, WINDOW_HEIGHT)


class MainWindow(QMainWindow):
    init_home_single = Signal(CurrentSummoner, SummonerGamesInfo)

    def __init__(self, version):
        super().__init__()
        # 设置窗口背景透明以及无默认菜单栏
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        # 限制窗口的大小
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setMaximumSize(MAIN_WINDOW_QSIZE)
        self.setMinimumSize(MAIN_WINDOW_QSIZE)

        self.version = version
        self.lol_process = False
        self.lol_event_listener = None
        self.lol_client_listener = None
        self.tray_icon = CustomTrayIcon(self)
        self.tray_icon.open_app_signal.connect(self.__on_show)
        self.tray_icon.exit_app_signal.connect(self.__custome_close)
        self.tray_icon.show()
        self.__init_signal()
        self.__on_open()

    def __init_signal(self):
        self.init_home_single.connect(self.init_home_interface)

    def __on_open(self):
        self.__init_ui()

        self.lol_client_listener = LOLProcessListener(self)
        self.lol_client_listener.lol_client_signal.client_status.connect(
            self.lol_process_handler
        )
        self.lol_client_listener.start()

    def __on_hide(self):
        self.hide()

    def __on_show(self):
        self.show()

    def __on_close(self):
        if cfg.CloseToTray:
            self.__on_hide()
            return
        self.__custome_close()
        
    def __custome_close(self):
        self.show()
        self.close()
        if self.lol_client_listener is not None:
            self.lol_client_listener.close_listener()
            self.lol_client_listener.wait()
        if self.lol_event_listener is not None:
            self.lol_event_listener.close_websocket()
            self.lol_event_listener.wait()

    def __init_ui(self):
        """初始化UI"""
        self.setWindowTitle("daluandouzhushou")
        self.main = QWidget(self)
        self.main.setObjectName("main")
        self.main_layout = QVBoxLayout(self.main)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.menu = MenuBar(self.main)
        # 点击菜单栏可拖动窗口
        self.menu.mousePressEvent = self.__on_mouse_press
        self.menu.mouseMoveEvent = self.__on_mouse_move
        self.menu.menu_btn_connect(self.menu.close_btn, self.__on_close)
        self.main_layout.addWidget(self.menu)

        # 连接LOL客户端的加载动画
        self.refresh = QtBoxFuncProgressBar()
        self.main_layout.addWidget(self.refresh)

        # 底部信息
        self.footer = Footer(self.main, self.version)
        self.main_layout.addWidget(self.footer)

        self.__set_style()

        self.setCentralWidget(self.main)

    def __set_style(self):
        self.main.setStyleSheet(
            """
            #main {
                background-color: rgb(223,236,213);
                border-radius: 12;
            }
            """
        )

    def __on_mouse_press(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = (
                event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            )

    def __on_mouse_move(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton:
            if self.drag_position is not None:
                self.move(event.globalPosition().toPoint() - self.drag_position)
                event.accept()

    def lol_process_handler(self, pid: int, status):
        if status:
            self.lol_process = True
            lol_auth_info = parse_lol_auth_info(pid)
            self.lol_token = lol_auth_info["remoting-auth-token"]
            self.lol_port = lol_auth_info["app-port"]
            lol_connector.start(self.lol_token, self.lol_port)
            self.lol_event_listener = LOLEventListener(
                self, self.lol_token, self.lol_port
            )
            self.lol_event_listener.lol_event_signal.ws_status_changed.connect(
                self.lcu_ws_status_handler
            )
            self.lol_event_listener.lol_event_signal.game_flow_status_changed.connect(
                self.__game_flow_handler
            )
            self.lol_event_listener.start()
        else:
            if self.lol_event_listener:
                self.lol_event_listener.terminate()
            self.on_disconnect_lcu()
            self.lol_event_listener = None

    def back_home(self, interface):
        """
        回到首页
        """
        interface.hide()
        self.main_layout.removeWidget(interface)
        self.main_layout.insertWidget(1, self.home)
        self.menu.settings_btn.show()
        self.menu.question_btn.show()
        self.home.show()
        self.menu.menu_btn_connect(self.menu.close_btn, self.__on_close)

    def init_home_interface(self, userinfo, recent_info):
        """初始化首页并显示"""
        self.refresh.hide()
        self.home = HomeInterface(self.main, userinfo, recent_info)
        self.home.server_list_widget.service_signal.connect(self.init_rune_source)
        self.main_layout.removeWidget(self.refresh)
        self.main_layout.insertWidget(1, self.home)
        self.menu.question_btn.show()
        self.menu.settings_btn.show()
        self.menu.menu_btn_connect(self.menu.settings_btn, self.init_settings_interface)
        self.menu.menu_btn_connect(self.menu.question_btn, self.init_about)
        self.home.show()

    def init_settings_interface(self):
        """
        打开设置页面
        """
        self.home.hide()
        self.menu.settings_btn.hide()
        self.menu.question_btn.hide()
        self.settings = SettingsInterface(self.main)
        self.main_layout.removeWidget(self.home)
        self.main_layout.insertWidget(1, self.settings)
        self.menu.menu_btn_connect(
            self.menu.close_btn, lambda: self.back_home(self.settings)
        )

    def init_about(self):
        """
        打开关于页面
        """
        self.home.hide()
        self.menu.settings_btn.hide()
        self.menu.question_btn.hide()
        # if not self.about:
        self.about = AboutInterface(self.main)
        self.main_layout.removeWidget(self.home)
        self.main_layout.insertWidget(1, self.about)
        self.menu.menu_btn_connect(
            self.menu.close_btn, lambda: self.back_home(self.about)
        )

    def init_rune_source(self):
        self.home.hide()
        self.menu.settings_btn.hide()
        self.menu.question_btn.hide()
        self.rune_source = RuneSourceInterface(self.main)
        self.main_layout.removeWidget(self.home)
        self.main_layout.insertWidget(1, self.rune_source)
        self.menu.menu_btn_connect(
            self.menu.close_btn, lambda: self.back_home(self.rune_source)
        )

    def on_disconnect_lcu(self):
        """当连接 lcu 的 ws 断开"""
        if self.home:
            self.home.hide()
            self.refresh.show()
            self.menu.settings_btn.hide()
            self.menu.question_btn.hide()
            self.main_layout.removeWidget(self.home)
            self.main_layout.insertWidget(1, self.refresh)
            self.lol_process = False


    def lcu_ws_status_handler(self, status: bool):
        def _task():
            current_summoner = lol_connector.get_current_summoner()
            icon_path = lol_connector.get_avatar(current_summoner.profileIconId)
            current_summoner.icon_path = icon_path
            history_match_games = lol_connector.get_summoner_games(
                current_summoner.puuid
            )
            self.init_home_single.emit(current_summoner, history_match_games)
        if status:
            threading.Thread(target=_task).start()
            return
        # self.on_disconnect_lcu()

    def __auto_accept_game(self):
        def _task():
            status = lol_connector.get_ready_check_status()
            if status.playerResponse != LolReadyCheckResponse.Declined:
                lol_connector.accept_game()
        threading.Thread(target=_task).start()

    def __game_flow_handler(self, game_flow: GameFlowEvent):
        if game_flow.data == "None":
            pass
        elif game_flow.data == "ReadyCheck":
            if cfg.AutoAcceptGame:
                self.__auto_accept_game()
