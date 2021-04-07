from .exceptions import InvalidLanguageValue
from .mapping import load_iso639_mapping


TAGS = ("name", "pt1", "pt2b", "pt2t", "pt3")


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
        for t in TAGS:
            setattr(self, f"_{t}", "")

        if isinstance(language, Lang):
            for t in TAGS:
                self[t] = language[t]
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

        msg = ", ".join((f"{tag}='{self[tag]}'" for tag in TAGS))

        return f"Lang({msg})"

    def __eq__(self, other):

        return isinstance(other, Lang) and all(
            self[t] == other[t] for t in TAGS
        )

    def __getitem__(self, lang_tag):

        return getattr(self, lang_tag)

    def __setitem__(self, lang_tag, new_lang_value):

        setattr(self, lang_tag, new_lang_value)

    @property
    def pt3(self):
        """Gets the ISO 639-3 code of this language"""
        return self._pt3

    @pt3.setter
    def pt3(self, lang_pt3):
        """Sets this language to this ISO 639-3 code"""
        self._set_attributes("pt3", lang_pt3)

    @property
    def pt1(self):
        """Gets the ISO 639-1 code of this language"""
        return self._pt1

    @pt1.setter
    def pt1(self, lang_pt1):
        """Sets this language to this ISO 639-1 code"""
        self._set_attributes("pt1", lang_pt1)

    @property
    def pt2b(self):
        """Gets the ISO 639-2B code of this language"""
        return self._pt2b

    @pt2b.setter
    def pt2b(self, lang_pt2b):
        """Sets this language to this ISO 639-2B code"""
        self._set_attributes("pt2b", lang_pt2b)

    @property
    def pt2t(self):
        """Gets the ISO 639-2T code of this language"""
        return self._pt2t

    @pt2t.setter
    def pt2t(self, lang_pt2t):
        """Sets this language to this ISO 639-2T code"""
        self._set_attributes("pt2t", lang_pt2t)

    @property
    def name(self):
        """Gets the ISO 639 name of this language"""
        return self._name

    @name.setter
    def name(self, lang_name):
        """Sets this language to this ISO 639 name"""
        self._set_attributes("name", lang_name)

    def _set_attributes(self, key_lang_tag, new_lang_value):

        try:
            d = Lang._data[key_lang_tag][new_lang_value]
        except KeyError:
            raise InvalidLanguageValue(new_lang_value)
        else:
            for t in TAGS:
                if t == key_lang_tag:
                    v = new_lang_value
                else:
                    v = d[t]
                setattr(self, f"_{t}", v)
