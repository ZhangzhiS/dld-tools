import base64
import json
import ssl
import os
from time import time

import websocket
from dld_tools.core.config import cfg
from dld_tools.tools.help import write_to_file
from dld_tools.tools.lol.data_schema import GameFlowEvent
from dld_tools.tools.lol.utils import get_lol_process_pid, is_lol_game_process_exist
from PySide6.QtCore import QObject, QThread, Signal
from dld_tools.tools.lol.connector import lol_connector

# websocket.enableTrace(True)


class LOLProcessSignal(QObject):
    client_status = Signal(int, bool)


class LOLProcessListener(QThread):
    """
    LOL 进程是否存在的监听器
    """

    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.lol_client_signal = LOLProcessSignal()

    def run(self) -> None:
        isRunning = False
        while True:
            pid = get_lol_process_pid()
            if pid != 0:
                if not isRunning:
                    isRunning = True
                    self.lol_client_signal.client_status.emit(pid, isRunning)
            else:
                if isRunning and not is_lol_game_process_exist():
                    isRunning = False
                    self.lol_client_signal.client_status.emit(0, isRunning)
            self.sleep(2)


class LOLEventSingle(QObject):
    game_flow_status_changed = Signal(GameFlowEvent)
    ws_status_changed = Signal(bool)


class LOLEventListener(QThread):
    _headers = {"Content-Type": "application/json", "Accept": "application/json"}

    def __init__(self, parent, token, port) -> None:
        super().__init__(parent)
        self.lol_event_signal = LOLEventSingle()
        self.token = token
        self.port = port
        self.client = None
        self._subscribe_event = {
            "/lol-gameflow/v1/gameflow-phase": {
                "data_model": GameFlowEvent,
                "signal": self.lol_event_signal.game_flow_status_changed,
            }
        }
        creds = f"riot:{self.token}".encode()
        self._headers["Authorization"] = "Basic %s" % base64.b64encode(creds).decode()
        self.url = f"wss://127.0.0.1:{self.port}"

    def on_message(self, _, message):
        try:
            data = json.loads(message)[2]
        except Exception:
            return
        uri = data["uri"]
        if cfg.DeBug:
            if not os.path.exists(cfg.LogPath):
                os.makedirs(cfg.LogPath)
            with open(os.path.join(cfg.LogPath, f"{time()}-{uri}.json"), "w") as f:
                json.dump(data.model_dump(), f)

        if uri in self._subscribe_event:
            data_model = self._subscribe_event[uri]["data_model"].model_validate(
                data
            )
            write_to_file(data_model)
            self._subscribe_event[uri]["signal"].emit(data_model)

    def on_open(self, _):
        self.send([5, "OnJsonApiEvent"])
        self.lol_event_signal.ws_status_changed.emit(True)

    def on_error(self, ws_client, msg):  # noqa
        pass

    def on_close(self, ws, close_status_code, close_msg):
        self.lol_event_signal.ws_status_changed.emit(False)

    def close_websocket(self):
        if self.client is not None:
            self.client.close()

    def send(self, data):
        data = json.dumps(data)
        if self.client:
            self.client.send(data)

    def run(self) -> None:
        while True:
            try:
                resp = lol_connector.get_ux_state()
                print(resp)
            except Exception:
                resp = False
            if resp:
                break
            self.sleep(1)

        self.client = websocket.WebSocketApp(
            self.url,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
            on_open=self.on_open,
            header=self._headers,
        )
        self.client.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
