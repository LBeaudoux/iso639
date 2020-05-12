import csv
import json
import logging

from pkg_resources import resource_filename

__all__ = ["Lang"]

TABLE_PATH = resource_filename(__package__, "iso-639-3.tab")
MAPPING_PATH = resource_filename(__package__, "iso-639-3.json")

logger = logging.getLogger(__name__)


def _load_iso639_mapping():
    """Load the ISO-639 mapping from its JSON file.
    """
    with open(MAPPING_PATH) as f:
        mapping = json.load(f)

    if not mapping:
        table = _load_iso639_table()
        mapping = _map_iso639_table(table)
        _save_iso639_mapping(mapping)

    return mapping


def _load_iso639_table():
    """Load the iso639 table from its tab file.
    """
    with open(TABLE_PATH) as f:
        rows = csv.reader(f, delimiter="\t")
        return rows[1:]


def _map_iso639_table(table):
    """Turn the ISO-639 table into a dict for mapping iso639 values faster.
    """
    mapping = {k: {} for k in ("pt1", "pt3", "name")}
    for row in table:
        # ISO 639 part 1 codes
        if row[3]:
            mapping["pt1"][row[3]] = {"pt3": row[0], "name": row[6]}
        # ISO 639 part 3 codes
        if row[0]:
            mapping["pt3"][row[0]] = {"pt1": row[3], "name": row[6]}
        # ISO 639 names
        if row[6]:
            mapping["name"][row[6]] = {"pt1": row[3], "pt3": row[0]}

    return mapping


def _save_iso639_mapping(mapping):
    """Save the ISO-639 mapping into a JSON file.
    """
    with open(MAPPING_PATH, "w") as f:
        json.dump(mapping, f)


class Lang:
    """Handle the code and the name of a given language by loading an 
    ISO 639-3 to ISO 639 name language mapping.
    data url on the official site of the ISO 639-3 Registration Authority:
    https://iso639-3.sil.org/sites/iso639-3/files/downloads/iso-639-3.tab    
    """

    _data = _load_iso639_mapping()

    def __init__(self, language=None):

        if not language:
            self.pt3 = ""
        elif len(language) == 3 and language.lower() == language:
            self.pt3 = language
        elif len(language) == 2 and language.lower() == language:
            self.pt1 = language
        else:
            self.name = language

    def __repr__(self):
        return f"pt3 : {self.pt3}, pt1 : {self.pt1}, name : {self.name}"

    @property
    def pt3(self):
        """Get the code of this language.
        """
        return self._pt3

    @pt3.setter
    def pt3(self, lang_pt3):
        """Set the code of this language and then change the name too.
        """
        try:
            self._pt3 = lang_pt3
            self._pt1 = Lang._data["pt3"][lang_pt3]["pt1"]
            self._name = Lang._data["pt3"][lang_pt3]["name"]
        except KeyError:
            logger.error(f"{lang_pt3} is not an ISO 639-3 language code.")
            self._pt3 = ""
            self._pt1 = ""
            self._name = ""

    @property
    def pt1(self):
        """Get the part1 code of this language.
        """
        return self._pt1

    @pt1.setter
    def pt1(self, lang_pt1):
        """Set the part1 of this language and then change the code and name too.
        """
        try:
            self._pt3 = Lang._data["pt1"][lang_pt1]["pt3"]
            self._pt1 = lang_pt1
            self._name = Lang._data["pt1"][lang_pt1]["name"]
        except KeyError:
            logger.error(f"{lang_pt1} is not an ISO 639-1 language code.")
            self._pt3 = ""
            self._pt1 = ""
            self._name = ""

    @property
    def name(self):
        """Get the name of this language.
        """
        return self._name

    @name.setter
    def name(self, lang_name):
        """Set the name of this language and then the code and the pt1 too.
        """
        try:
            self._pt3 = Lang._data["name"][lang_name]["pt3"]
            self._pt1 = Lang._data["name"][lang_name]["pt1"]
            self._name = lang_name
        except KeyError:
            logger.error(f"{lang_name} is not an ISO 639 language name.")
            self._pt3 = ""
            self._pt1 = ""
            self._name = ""
