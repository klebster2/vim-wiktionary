import requests
from pathlib import Path

from dicts.base_dict_loader import BaseDictLoader

class LoadBritfoneDict(BaseDictLoader):
    RELEASE_URL = "https://api.github.com/repos/klebster2/Britfone/releases/latest"
    path_to_dict=Path(__file__).parent / "latest" / "britfone.main.3.1.0.csv"
    SEP = ",\s+"

    def __init__(self):
        pass
