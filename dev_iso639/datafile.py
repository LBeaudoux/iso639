from .config import DATA_DIR, DATA_FILES, DOWNLOAD_DIR, DOWNLOAD_FILES


class DataFile:
    """An ISO 639 reference data file."""

    FILENAME_CODE_SET = {
        "ISO-639-2_utf-8.txt": "639-2",
        "ISO-639-2_code_changes.tsv": "639-2",
        "iso-639-3.tab": "639-3",
        "iso-639-3_Retirements.tab": "639-3",
        "iso-639-3-macrolanguages.tab": "639-3",
        "iso-639-3_Name_Index.tab": "639-3",
        "iso639-5.tsv": "639-5",
        "iso639-5_changes.tsv": "639-5",
    }
    CODE_SET_DOWNLOAD_ENDPOINT = {
        "639-2": "https://www.loc.gov/standards/iso639-2/",
        "639-3": "https://iso639-3.sil.org/sites/iso639-3/files/downloads/",
        "639-5": "http://id.loc.gov/vocabulary/",
    }
    CODE_SET_SCRAP_FILE = {
        "639-2": "code_changes.php",
        "639-5": "changes.php",
    }
    CODE_SET_SCRAP_ENDPOINT = {
        "639-2": "https://www.loc.gov/standards/iso639-2/php/",
        "639-5": "https://www.loc.gov/standards/iso639-5/",
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
        "ISO-639-2_code_changes.tsv": {
            "header": 0,
            "names": [
                "Part1",
                "Part2",
                "English_Name",
                "French_Name",
                "Date_Added_Or_Changed",
                "Category_Of_Change",
                "Notes",
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

    def __init__(self, file_name):
        self._name = file_name

    @property
    def name(self):
        return self._name

    @property
    def download_url(self):
        code_set = self.FILENAME_CODE_SET[self._name]
        file_url = self.CODE_SET_DOWNLOAD_ENDPOINT[code_set] + self._name
        return file_url

    @property
    def scrap_url(self):
        code_set = self.FILENAME_CODE_SET[self._name]
        scrap_endpoint = self.CODE_SET_SCRAP_ENDPOINT[code_set]
        scrap_filename = self.CODE_SET_SCRAP_FILE[code_set]
        return scrap_endpoint + scrap_filename

    @property
    def path(self):
        if self._name in DOWNLOAD_FILES:
            return DOWNLOAD_DIR + self._name
        elif self._name in DATA_FILES:
            return DATA_DIR + self._name
        return ""

    @property
    def params(self):
        file_params = self.FILENAME_CSV_PARAMS.get(self._name, {})
        return {**self.DEFAULT_CSV_PARAMS, **file_params}
