from .exceptions import InvalidLanguageValue
from .mapping import load_iso639_mapping


class Lang:
    """Handler for the ISO 639 language representation standard
    The ISO 639 mapping data comes from the official site of the
    ISO 639-3 Registration Authority:
    https://iso639-3.sil.org/sites/iso639-3/files/downloads/iso-639-3.tab
    """

    _data = load_iso639_mapping()

    def __init__(self, language):
        """
        Parameters
        ----------
        language : str
            A language code (ISO 639-1, ISO 639-2B, ISO 639-2T, ISO 639-3)
            or an ISO 639 language name. Case sensitive
        """

        self._pt1 = ""
        self._pt2b = ""
        self._pt2t = ""
        self._pt3 = ""
        self._name = ""

        if isinstance(language, Lang):
            self._pt1 = language._pt1
            self._pt2b = language._pt2b
            self._pt2t = language._pt2t
            self._pt3 = language._pt3
            self._name = language._name
        elif len(language) == 3 and language.lower() == language:
            try:
                self.pt3 = language
                # note that when it exists, the ISO 639-2T of a language
                # is always equal to its ISO 639-3
            except InvalidLanguageValue:
                self.pt2b = language
        elif len(language) == 2 and language.lower() == language:
            self.pt1 = language
        else:
            self.name = language

    def __repr__(self):

        return (
            f"pt3 : {self.pt3}, pt1 : {self.pt1}, pt2b : {self.pt2b}, "
            f"pt2t : {self.pt2t}, name : {self.name}"
        )

    def __eq__(self, other):

        return (
            isinstance(other, Lang)
            and self.pt1 == other.pt1
            and self.pt2b == other.pt2b
            and self.pt2t == other.pt2t
            and self.pt3 == other.pt3
            and self.name == other.name
        )

    @property
    def pt3(self):
        """Gets the ISO 639-3 code of this language"""
        return self._pt3

    @pt3.setter
    def pt3(self, lang_pt3):
        """Sets this language to this ISO 639-3 code"""
        if lang_pt3 not in Lang._data["pt3"]:
            raise InvalidLanguageValue(lang_pt3)
        else:
            self._pt3 = lang_pt3
            self._pt1 = Lang._data["pt3"][lang_pt3]["pt1"]
            self._pt2b = Lang._data["pt3"][lang_pt3]["pt2B"]
            self._pt2t = Lang._data["pt3"][lang_pt3]["pt2T"]
            self._name = Lang._data["pt3"][lang_pt3]["name"]

    @property
    def pt1(self):
        """Gets the ISO 639-1 code of this language"""
        return self._pt1

    @pt1.setter
    def pt1(self, lang_pt1):
        """Sets this language to this ISO 639-1 code"""
        if lang_pt1 not in Lang._data["pt1"]:
            raise InvalidLanguageValue(lang_pt1)
        else:
            self._pt3 = Lang._data["pt1"][lang_pt1]["pt3"]
            self._pt1 = lang_pt1
            self._pt2b = Lang._data["pt1"][lang_pt1]["pt2B"]
            self._pt2t = Lang._data["pt1"][lang_pt1]["pt2T"]
            self._name = Lang._data["pt1"][lang_pt1]["name"]

    @property
    def pt2b(self):
        """Gets the ISO 639-2B code of this language"""
        return self._pt2b

    @pt2b.setter
    def pt2b(self, lang_pt2b):
        """Sets this language to this ISO 639-2B code"""
        if lang_pt2b not in Lang._data["pt2B"]:
            raise InvalidLanguageValue(lang_pt2b)
        else:
            self._pt3 = Lang._data["pt2B"][lang_pt2b]["pt3"]
            self._pt1 = Lang._data["pt2B"][lang_pt2b]["pt1"]
            self._pt2b = lang_pt2b
            self._pt2t = Lang._data["pt2B"][lang_pt2b]["pt2T"]
            self._name = Lang._data["pt2B"][lang_pt2b]["name"]

    @property
    def pt2t(self):
        """Gets the ISO 639-2T code of this language"""
        return self._pt2t

    @pt2t.setter
    def pt2t(self, lang_pt2t):
        """Sets this language to this ISO 639-2T code"""
        if lang_pt2t not in Lang._data["pt2T"]:
            raise InvalidLanguageValue(lang_pt2t)
        else:
            self._pt3 = Lang._data["pt2T"][lang_pt2t]["pt3"]
            self._pt1 = Lang._data["pt2T"][lang_pt2t]["pt1"]
            self._pt2b = Lang._data["pt2T"][lang_pt2t]["pt2B"]
            self._pt2t = lang_pt2t
            self._name = Lang._data["pt2T"][lang_pt2t]["name"]

    @property
    def name(self):
        """Gets the ISO 639 name of this language"""
        return self._name

    @name.setter
    def name(self, lang_name):
        """Sets this language to this ISO 639 name"""
        if lang_name not in Lang._data["name"]:
            raise InvalidLanguageValue(lang_name)
        else:
            self._pt3 = Lang._data["name"][lang_name]["pt3"]
            self._pt1 = Lang._data["name"][lang_name]["pt1"]
            self._pt2b = Lang._data["name"][lang_name]["pt2B"]
            self._pt2t = Lang._data["name"][lang_name]["pt2T"]
            self._name = lang_name
