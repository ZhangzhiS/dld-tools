import os
import json
import time
from urllib.parse import urljoin
from urllib3 import disable_warnings

import requests
from dld_tools.core.config import cfg
from dld_tools.tools.lol import lcu_api
from dld_tools.tools.lol.data_schema import (
    CurrentSummoner,
    ReadyCheckStatus,
    SummonerGamesInfo,
)
from dld_tools.tools.lol.lcu_api import BaseRequest

disable_warnings()


class RetryMaximumAttempts(BaseException):
    pass


def retry(count=5, retry_sep=0):
    def decorator(func):
        def wrapper(*args, **kwargs):
            exce = None
            for _ in range(count):
                print(count)
                while lol_connector.ref_cnt >= 3:
                    time.sleep(2)
                lol_connector.ref_cnt += 1
                try:
                    res = func(*args, **kwargs)
                except BaseException as e:
                    lol_connector.ref_cnt -= 1
                    time.sleep(retry_sep)
                    exce = e
                    continue
                else:
                    lol_connector.ref_cnt -= 1
                    break
            else:
                # 有异常抛异常, 没异常抛 RetryMaximumAttempts
                exce = (
                    exce
                    if exce
                    else RetryMaximumAttempts("Exceeded maximum retry attempts.")
                )

                # ReferenceError为LCU未就绪仍有请求发送时抛出, 直接吞掉不用提示
                # 其余异常弹一个提示
                if type(exce) is not ReferenceError:
                    lol_connector.ref_cnt -= 1
                raise exce

            return res

        return wrapper

    return decorator


class LOLConnector:
    def __init__(self) -> None:
        self.port = None
        self.token = None
        self.url = ""
        self.ref_cnt = 0

    def __prepare(self, request: BaseRequest) -> requests.PreparedRequest:
        uri = request.url
        if request.path_params is not None:
            uri = request.url.format(**request.path_params)
        url = urljoin(self.url, uri)
        req = requests.Request(
            method=request.method.value,
            url=url,
            params=request.params,
        )
        return req.prepare()

    def start(self, token: str, port: int):
        self.session = requests.Session()
        self.url = f"https://riot:{token}@127.0.0.1:{port}"

    def __request(self, req: BaseRequest):
        prepare_req = self.__prepare(req)
        resp = self.session.send(prepare_req, verify=False)
        
        if resp.status_code == 200:
            return resp
        elif resp.status_code == 204:
            return True

    @retry()
    def get_current_summoner(self) -> CurrentSummoner:
        """
        获取当前召唤师信息
        """
        resp = self.__request(lcu_api.GetCurrentSummoner())
        return CurrentSummoner.model_validate(resp.json())

    # @retry()
    def accept_game(self) -> None:
        self.__request(lcu_api.AcceptGame())

    # @retry()
    def get_ready_check_status(self) -> ReadyCheckStatus:
        resp = self.__request(lcu_api.GetReadyCheckStatus())
        print(resp.json())
        return ReadyCheckStatus.model_validate(resp.json())

    # @retry()
    def get_avatar(self, avatar_id: int = 1234) -> str:
        """获取头像"""
        avatar = os.path.join(cfg.ProfileIconPath, f"{avatar_id}.jpg")
        if not os.path.exists(cfg.ProfileIconPath):
            os.makedirs(cfg.ProfileIconPath)
        if not os.path.exists(avatar):
            res = self.__request(lcu_api.GetProfileIcon(avatar_id))
            with open(avatar, "wb") as f:
                f.write(res.content)
        return avatar

    # @retry()
    def get_ux_state(self) -> bool:
        resp = self.__request(lcu_api.GetUXState())
        if resp.status_code:
            return True
        return False

    # @retry()
    def get_summoner_games(
        self, puuid: str, begIndex: int = 0, endIndex: int = 19
    ) -> SummonerGamesInfo:
        resp = self.__request(lcu_api.GetSummonerGames(puuid, begIndex, endIndex))
        return SummonerGamesInfo.model_validate(resp.json())

    def close(self):
        self.session.close()


lol_connector = LOLConnector()
