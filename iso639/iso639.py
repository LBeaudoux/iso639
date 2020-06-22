from .exceptions import InvalidLanguageValue
from .mapping import load_iso639_mapping


class Lang:
    """Handle the ISO 639 codes and name of a given language.
    The ISO 639 language mapping data comes from the official site of the 
    ISO 639-3 Registration Authority:
    https://iso639-3.sil.org/sites/iso639-3/files/downloads/iso-639-3.tab    
    """

    _data = load_iso639_mapping()

    def __init__(self, language):

        self._pt1 = ""
        self._pt3 = ""
        self._name = ""

        if len(language) == 3 and language.lower() == language:
            self.pt3 = language
        elif len(language) == 2 and language.lower() == language:
            self.pt1 = language
        else:
            self.name = language

    def __repr__(self):

        return f"pt3 : {self.pt3}, pt1 : {self.pt1}, name : {self.name}"

    def __eq__(self, other):

        return (
            self._pt1 == other.pt1
            and self._pt3 == other.pt3
            and self.name == other.name
        )

    @property
    def pt3(self):
        """Get the code of this language.
        """
        return self._pt3

    @pt3.setter
    def pt3(self, lang_pt3):
        """Set the code of this language and then change the name too.
        """
        if lang_pt3 not in Lang._data["pt3"]:
            raise InvalidLanguageValue(lang_pt3)
        else:
            self._pt3 = lang_pt3
            self._pt1 = Lang._data["pt3"][lang_pt3]["pt1"]
            self._name = Lang._data["pt3"][lang_pt3]["name"]

    @property
    def pt1(self):
        """Get the part1 code of this language.
        """
        return self._pt1

    @pt1.setter
    def pt1(self, lang_pt1):
        """Set the part1 of this language and then change the code and name too.
        """
        if lang_pt1 not in Lang._data["pt1"]:
            raise InvalidLanguageValue(lang_pt1)
        else:
            self._pt3 = Lang._data["pt1"][lang_pt1]["pt3"]
            self._pt1 = lang_pt1
            self._name = Lang._data["pt1"][lang_pt1]["name"]

    @property
    def name(self):
        """Get the name of this language.
        """
        return self._name

    @name.setter
    def name(self, lang_name):
        """Set the name of this language and then the code and the pt1 too.
        """
        if lang_name not in Lang._data["name"]:
            raise InvalidLanguageValue(lang_name)
        else:
            self._pt3 = Lang._data["name"][lang_name]["pt3"]
            self._pt1 = Lang._data["name"][lang_name]["pt1"]
            self._name = lang_name
