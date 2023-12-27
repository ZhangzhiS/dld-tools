import json
import os
from time import time

from pydantic import BaseModel
from dld_tools.core.config import cfg


def write_to_file(data: BaseModel):
    if cfg.DeBug:
        if not os.path.exists(cfg.LogPath):
            os.makedirs(cfg.LogPath)
        with open(os.path.join(cfg.LogPath, f"{time()}.json"), "w") as f:
            json.dump(data.model_dump(), f)
