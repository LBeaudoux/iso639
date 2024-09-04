from typing import Dict, Optional

from .config import DATA_DIR, DATA_FILES, DOWNLOAD_DIR, DOWNLOAD_FILES

FILENAME_CODE_SET = {
    "ISO-639-2_utf-8.txt": "ISO 639-2",
    "iso-639-3.tab": "ISO 639-3",
    "iso-639-3_Retirements.tab": "ISO 639-3",
    "iso-639-3-macrolanguages.tab": "ISO 639-3",
    "iso-639-3_Name_Index.tab": "ISO 639-3",
    "iso639-5.tsv": "ISO 639-5",
}
CODE_SET_DOWNLOAD_URL = {
    "ISO 639-2": "https://www.loc.gov/standards/iso639-2/",
    "ISO 639-3": "https://iso639-3.sil.org/sites/iso639-3/files/downloads/",
    "ISO 639-5": "http://id.loc.gov/vocabulary/",
}

DEFAULT_CSV_PARAMS = {
    "keep_default_na": False,
    "na_values": [""],
    "index_col": 0,
    "delimiter": "\t",
}
FILENAME_CSV_PARAMS = {
    "ISO-639-2_utf-8.txt": {
        "encoding": "utf-8-sig",
        "delimiter": "|",
        "names": [
            "Part2b",
            "Part2t",
            "Part1",
            "English_Name",
            "French_Name",
        ],
    },
    "iso-639-3.tab": {
        "header": 0,
        "names": [
            "Id",
            "Part2b",
            "Part2t",
            "Part1",
            "Scope",
            "Type",
            "Ref_Name",
            "Comment",
        ],
    },
    "iso639-5.tsv": {
        "header": 0,
        "names": ["Uri", "Code", "Label_English", "Label_French"],
    },
}


class DataFile:
    """An ISO 639 reference data file."""

    def __init__(self, file_name) -> None:
        self._name = file_name

    @property
    def name(self):
        return self._name

    @property
    def url(self) -> str:
        code_set = FILENAME_CODE_SET[self._name]
        file_url = CODE_SET_DOWNLOAD_URL.get(code_set) + self._name
        return file_url

    @property
    def path(self) -> Optional[str]:
        if self._name in DOWNLOAD_FILES:
            return DOWNLOAD_DIR + self._name
        elif self._name in DATA_FILES:
            return DATA_DIR + self._name
        return

    @property
    def params(self) -> Dict[str, str]:
        file_params = FILENAME_CSV_PARAMS.get(self._name, {})
        return {**DEFAULT_CSV_PARAMS, **file_params}
