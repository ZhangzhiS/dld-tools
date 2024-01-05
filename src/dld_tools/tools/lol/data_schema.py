import enum
from typing import Any, List, Optional

from pydantic import BaseModel


class LolReadyCheckResponse(enum.Enum):
    Accepted = "Accepted"
    Declined = "Declined"
    NONE = "None"


class GameFlowStatus(enum.Enum):
    NONE = "None"


class CurrentSummoner(BaseModel):
    accountId: int
    displayName: str
    summonerId: int
    summonerLevel: int
    xpSinceLastLevel: int
    xpUntilNextLevel: int
    profileIconId: int
    puuid: str
    icon_path: Optional[str] = ""


class ReadyCheckStatus(BaseModel):
    declinerIds: Any
    playerResponse: LolReadyCheckResponse
    dodgeWarning: str
    state: str


class MatchGameParticipantsStatistics(BaseModel):
    assists: int
    win: int
    kills: int
    deaths: int


class MatchGameParticipants(BaseModel):
    championId: int
    stats: MatchGameParticipantsStatistics


class MatchGameDetail(BaseModel):
    gameCreation: int
    gameCreationDate: str
    gameDuration: int
    gameId: int
    gameMode: str
    gameType: str
    gameVersion: str
    mapId: int
    participants: List[MatchGameParticipants]


class MatchGameInfo(BaseModel):
    gameBeginDate: str
    gameCount: int
    gameEndDate: str
    gameIndexBegin: int
    gameIndexEnd: int
    games: List[MatchGameDetail]


class SummonerGamesInfo(BaseModel):
    accountId: int
    games: MatchGameInfo
    platformId: str


class LCUEventBase(BaseModel):
    uri: str
    eventType: str
    data: Optional[Any]


class SummonerChangeEvent(LCUEventBase):
    data: CurrentSummoner


class GameFlowEvent(LCUEventBase):
    data: str
