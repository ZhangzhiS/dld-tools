# -- coding: utf-8 --**
import os
import json

from pydantic import BaseModel


class Config(BaseModel):
    DeBug: bool = False
    LogPath: str = os.path.join(os.path.expanduser("~"), "logs", "loldld")

    ResourcePath: str = "resources"

    ProfileIconPath: str = os.path.join(ResourcePath, "game", "profile")

    # 自动接受对局
    AutoAcceptGame: bool = False
    # 关闭窗口到任务栏
    CloseToTray: bool = False

    def save(self):
        config_path = os.path.dirname(os.path.abspath(__file__))
        old_path = os.path.join(config_path, "config.json")
        with open(old_path, "w", encoding="utf-8") as w:
            json.dump(self.model_dump(), w)


def load():
    config_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(config_dir, "config.json")
    if not os.path.exists(config_path):
        obj = Config()
        config_data = obj.model_dump()
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config_data, f)
    else:
        with open(config_path, "r", encoding="utf-8") as f:
            obj = Config.model_validate(json.load(f))
    return obj


cfg = load()
