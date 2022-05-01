from collections import defaultdict
import re
import tarfile
import requests
import shutil
import json
import glob
from pathlib import Path

class BaseDictLoader:

    def __init__(self):
        pass

    def download_file(self, url: str) -> str:
        """
        """
        local_filename = url.split('/')[-1]
        local_filename = local_filename if local_filename.endswith('.tar.gz') else local_filename + '.tar.gz'
        with requests.get(url, stream=True) as r:
            with open(local_filename, 'wb') as f:
                shutil.copyfileobj(r.raw, f)

        return local_filename

    def load(self):
        """
        """
        # first check any dict exists
        max_version = -1
        max_file = []
        max_version_filepath = None
        dict_path = glob.glob(str(self.path_to_dict.parent / "*/*.csv"))
        if not dict_path:
            # pre download
            latest_release_tarball_url = self._get_latest_release_tarball()
            # download
            latest_release_tarball = self.download_file(latest_release_tarball_url)
            # unpack
            self.decompress_dict_tarball(latest_release_tarball, self.path_to_dict.parent)

            dict_path = glob.glob(str(self.path_to_dict.parent / "*/*.csv"))

        for file in dict_path:
            check_version = re.search('[A-Za-z\-\.]*(\d\.+\d)?', Path(file).name)
            if check_version:
                max_version_filepath = file if max_version < float(check_version.group(1)) else path
                max_version = float(check_version.group(1)) if max_version < float(check_version.group(1)) else version

        _phonedict     = defaultdict(list)
        _phonedict_rev = defaultdict(list)
        with open(max_version_filepath, 'r') as f:
            for idx, line in enumerate(f.readlines()):
                if line[0] == "#":
                    continue
                try:
                    word, phones = re.match(rf'(\S+){self.SEP}(.*)', line).groups()
                except:
                    import pdb; pdb.set_trace()
                    raise ValueError("Unable to parse idx:{idx} line:{line}")

                _phonedict[phones].append(word)
                _phonedict_rev[word].append(phones)
        return _phonedict, _phonedict_rev

    def decompress_dict_tarball(self, dict_tar_gz, path):
        """
        extract tarball to path
        """
        file = tarfile.open(dict_tar_gz)
        file.extractall(path)
        file.close()

    def _get_latest_release_tarball(self):
        """
        get latest release URL from github
        """
        r = requests.get(self.RELEASE_URL)
        return json.loads(r.text).get('tarball_url')
