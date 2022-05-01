from pathlib import Path
from dicts.base_dict_loader import BaseDictLoader


class LoadBeepDict(BaseDictLoader):
    """
    Created an Compiled at the university of Cambridge, and the university of Durham,
    the rights belong there also.

    This dictionary is a bit dated (from 1996). But it provides over 250k pronunciations.
    """
    url="https://www.openslr.org/resources/14/beep.tar.gz"
    path_to_dict=Path(__file__).parent / "beep/beep-1.0"
    SEP = "\s+"

    def __init__(self):
        beepdict_tar_gz = self.download_dict(self.url)
        self.decompress_dict_tarball(beepdict_tar_gz)
