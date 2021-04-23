from .exceptions import InvalidLanguageValue, DeprecatedLanguageValue
from .mapping import DeprecatedMapping, ISO639Mapping, MacroMapping

TAGS = ("name", "pt1", "pt2b", "pt2t", "pt3", "pt5")


class Lang:
    """Lang handles the ISO 639 series of international standards
    for language codes

    Instantiable with any ISO 639 language code or name as argument
    (case sensitive)

    ...

    Attributes
    ----------
    name : str
        ISO 639-3 reference language name if there is one, ISO 639-2 or
        ISO 639-5 English name otherwise
    pt1 : str
        two-letter ISO 639-1 code, if there is one
    pt2b : str
        three-letter ISO 639-2 code for bibliographic applications,
        if there is one
    pt2t : str
        three-letter ISO 639-2 code for terminology applications,
        if there is one
    pt3 : str
        three-letter ISO 639-3 code, if there is one
    pt5 : str
        three-letter ISO 639-5 code, if there is one
    """

    _data = ISO639Mapping().load()
    _macro = MacroMapping().load()
    _deprecated = DeprecatedMapping().load()

    def __init__(self, *args, **kwargs):

        params = {}
        if not kwargs and len(args) == 1:
            lang = args[0]
            if isinstance(lang, Lang):
                params = {k[1:]: v for k, v in lang.__dict__.items()}
            elif len(lang) == 3 and lang.lower() == lang:
                self._assert_not_deprecated(lang)
                for tag in ("pt3", "pt2b", "pt2t", "pt5"):
                    params = self._get_params(tag, lang)
                    if params:
                        break
            elif len(lang) == 2 and lang.lower() == lang:
                params = self._get_params("pt1", lang)
            else:
                params = self._get_params("name", lang)
        elif not args and kwargs:
            self._assert_not_deprecated(kwargs.get("pt3"))
            a = [self._get_params(tg, lg) for tg, lg in kwargs.items()]
            params = {} if a.count(a[0]) != len(a) else a[0]

        self._set_attributes(params, *args, **kwargs)

    def __repr__(self):

        msg = ", ".join((f"{tag}='{getattr(self, tag)}'" for tag in TAGS))

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
    def pt1(self):
        """Gets the ISO 639-1 code of this language"""
        return self._pt1

    @pt1.setter
    def pt1(self, lang_pt1):
        """Sets this language to this ISO 639-1 code"""
        params = self._get_params("pt1", lang_pt1)
        self._set_attributes(params, lang_pt1)

    @property
    def pt2b(self):
        """Gets the ISO 639-2B code of this language"""
        return self._pt2b

    @pt2b.setter
    def pt2b(self, lang_pt2b):
        """Sets this language to this ISO 639-2B code"""
        params = self._get_params("pt2b", lang_pt2b)
        self._set_attributes(params, lang_pt2b)

    @property
    def pt2t(self):
        """Gets the ISO 639-2T code of this language"""
        return self._pt2t

    @pt2t.setter
    def pt2t(self, lang_pt2t):
        """Sets this language to this ISO 639-2T code"""
        params = self._get_params("pt2t", lang_pt2t)
        self._set_attributes(params, lang_pt2t)

    @property
    def pt3(self):
        """Gets the ISO 639-3 code of this language"""
        return self._pt3

    @pt3.setter
    def pt3(self, lang_pt3):
        """Sets this language to this ISO 639-3 code"""
        params = self._get_params("pt3", lang_pt3)
        self._set_attributes(params, lang_pt3)

    @property
    def pt5(self):
        """Gets the ISO 639-5 code of this language"""
        return self._pt5

    @pt5.setter
    def pt5(self, lang_pt5):
        """Sets this language to this ISO 639-5 code"""
        params = self._get_params("pt5", lang_pt5)
        self._set_attributes(params, lang_pt5)

    @property
    def name(self):
        """Gets the ISO 639 name of this language"""
        return self._name

    @name.setter
    def name(self, lang_name):
        """Sets this language to this ISO 639 name"""
        params = self._get_params("name", lang_name)
        self._set_attributes(params, lang_name)

    def macro(self):
        """Get the macrolanguage of this individual language

        Returns
        -------
        iso639.Lang
            the macrolanguage of this individual language, if there is one
        """
        macro_pt3 = self._get_macro(self._pt3)
        if macro_pt3:
            try:
                macro = Lang(macro_pt3)
            except InvalidLanguageValue:
                pass
            else:
                return macro

        return

    def individuals(self):
        """Get all individual languages of this macrolanguage

        Returns
        -------
        list of Lang
            the Lang instances of the individual languages of this
            macrolanguage, if it is one
        """
        individuals = []
        for lg in self._get_individuals(self._pt3):
            try:
                lang = Lang(lg)
            except InvalidLanguageValue:
                pass
            else:
                individuals.append(lang)

        return individuals

    @classmethod
    def _assert_not_deprecated(cls, lang_value):
        """Raise an error when this language value is a deprecated
        ISO 639-3 code
        """
        try:
            d = cls._deprecated[lang_value]
        except KeyError:
            pass
        else:
            raise DeprecatedLanguageValue(id=lang_value, **d)

    @classmethod
    def _get_params(cls, key_lang_tag=None, new_lang_value=None):
        """Get all ISO-639 parameters for this language tag and value

        Return an empty dict if the language parameters are not valid
        """
        d = cls._data.get(key_lang_tag, {}).get(new_lang_value, {})
        if d:
            d[key_lang_tag] = new_lang_value

        return d

    @classmethod
    def _get_macro(cls, pt3):
        """Get the macrolanguage of this ISO639-3 language code"""
        return cls._macro["individual"].get(pt3, "")

    @classmethod
    def _get_individuals(cls, pt3):
        """Get the individual languages linked to this macrolanguage code"""
        return cls._macro["macro"].get(pt3, [])

    def _set_attributes(self, lang_params, *args, **kwargs):
        """Set attributes values to these ISO-639 language parameters

        Raise an error when no language parameter is passed
        """
        if not lang_params:
            raise InvalidLanguageValue(*args, **kwargs)

        for t in TAGS:
            setattr(self, f"_{t}", lang_params.get(t, ""))
