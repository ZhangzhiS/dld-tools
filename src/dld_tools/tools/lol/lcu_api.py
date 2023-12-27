import enum
from typing import Any, Dict, Optional
from dld_tools.tools.lol import data_schema


class METHOD(enum.Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"


class BaseRequest:
    url: str
    method: METHOD
    params: Optional[Dict[str, Any]] = None
    json: Optional[Dict[Any, Any]] = None
    path_params: Optional[Dict[str, Any]] = None
    response: Optional[Any] = None


class GetCurrentSummoner(BaseRequest):
    url = "/lol-summoner/v1/current-summoner"
    method = METHOD.GET
    response = data_schema.CurrentSummoner


class GetReadyCheckStatus(BaseRequest):
    url = "/lol-matchmaking/v1/ready-check"
    method = METHOD.GET
    response = data_schema.ReadyCheckStatus


class AcceptGame(BaseRequest):
    url = "/lol-matchmaking/v1/ready-check/accept"
    method = METHOD.POST


class GetProfileIcon(BaseRequest):
    url = "/lol-game-data/assets/v1/profile-icons/{avatar_id}.jpg"
    method = METHOD.GET
    response = bytes

    def __init__(self, avatar_id: int) -> None:
        self.path_params = {"avatar_id": avatar_id}
        self.path_params = dict(avatar_id=avatar_id)


class GetSummonerGames(BaseRequest):
    url = "/lol-match-history/v1/products/lol/{puuid}/matches"
    method = METHOD.GET
    response = data_schema.SummonerGamesInfo

    def __init__(self, puuid: str, begIndex: int = 0, endIndex: int = 4) -> None:
        self.path_params = dict(puuid=puuid)
        self.params = dict(begIndex=begIndex, endIndex=endIndex)


class GetUXState(BaseRequest):
    url = "/riotclient/ux-state"
    method = METHOD.GET
