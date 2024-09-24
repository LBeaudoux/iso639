from operator import itemgetter
from typing import Dict, Iterator, List, Optional, Union

from .datafile import load_file
from .exceptions import DeprecatedLanguageValue, InvalidLanguageValue


class Lang(tuple):
    """ISO 639 reference name and identifiers of a language or group of
    languages.

    Can be instantiated with any ISO 639 identifier or name as an argument.
    Case sensitive.

    ...

    Attributes
    ----------
    name : str
        ISO 639-3 reference name for languages, ISO 639-5 English name for
        groups of languages.
    pt1 : str
        two-letter ISO 639-1 identifier, if there is one.
    pt2b : str
        three-letter ISO 639-2/B identifier for bibliographic applications, if
        there is one
    pt2t : str
        three-letter ISO 639-2/T identifier for terminology applications,
        if there is one
    pt3 : str
        three-letter ISO 639-3 identifier, if there is one
    pt5 : str
        three-letter ISO 639-5 identifier, if there is one

    Examples
    --------
    >>> lg = Lang("eng")
    >>> lg
    Lang(name='English', pt1='en', pt2b='eng', pt2t='eng', pt3='eng', pt5='')
    >>> lg.name
    'English'
    """

    _tags = ("name", "pt1", "pt2b", "pt2t", "pt3", "pt5")
    _abrs = {
        "A": "Ancient",
        "C": "Constructed",
        "E": "Extinct",
        "H": "Historical",
        "I": "Individual",
        "L": "Living",
        "M": "Macrolanguage",
        "S": "Special",
    }

    _data = load_file("mapping_data")
    _scope = load_file("mapping_scope")
    _type = load_file("mapping_type")
    _deprecated = load_file("mapping_deprecated")
    _macro = load_file("mapping_macro")
    _ref_name = load_file("mapping_ref_name")
    _other_names = load_file("mapping_other_names")

    __slots__ = ()  # set immutability of Lang

    def __new__(cls, name_or_identifier: Union[str, "Lang"]):
        lang_tuple = cls._validate_arg(name_or_identifier)
        if lang_tuple == tuple():  # not valid argument
            cls._assert_not_deprecated(name_or_identifier)
            raise InvalidLanguageValue(name_or_identifier=name_or_identifier)

        # instantiate as a tuple of ISO 639 language values
        return tuple.__new__(cls, lang_tuple)

    def __repr__(self):
        chunks = ["=".join((tg, repr(getattr(self, tg)))) for tg in self._tags]

        return "Lang({})".format(", ".join(chunks))

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return type(other) is type(self) and hash(other) == hash(self)

    def __lt__(self, other):
        return (
            type(other) is type(self) and other.name and self.name < other.name
        )

    def __getnewargs__(self):
        unpickling_args = (self.name,)

        return unpickling_args

    @property
    def name(self) -> str:
        """The ISO 639 reference name of the language or group of languages."""
        return tuple.__getitem__(self, 0)

    @property
    def pt1(self) -> str:
        """The ISO 639-1 identifier of the language."""
        return tuple.__getitem__(self, 1)

    @property
    def pt2b(self) -> str:
        """The ISO 639-2/B identifier of the language or group of languages."""
        return tuple.__getitem__(self, 2)

    @property
    def pt2t(self) -> str:
        """The ISO 639-2/T identifier of the language or group of languages."""
        return tuple.__getitem__(self, 3)

    @property
    def pt3(self) -> str:
        """The ISO 639-3 identifier of the language."""
        return tuple.__getitem__(self, 4)

    @property
    def pt5(self) -> str:
        """The ISO 639-5 identifier of the group of languages."""
        return tuple.__getitem__(self, 5)

    def asdict(self) -> Dict[str, str]:
        """Get the attributes of the `Lang` as a Python dictionary.

        Returns
        -------
        Dict[str, str]
            A dictionary containing the values of the 'name', 'pt1', 'pt2b',
            'pt2t', 'pt3' and 'pt5' attibutes.
        """

        return {tg: getattr(self, tg) for tg in self._tags}

    def scope(self) -> Optional[str]:
        """Get the scope of the language according to ISO 639-3.

        Returns
        -------
        str
            The scope of the language among 'Individual','Macrolanguage' and
            'Special'. Returns None for groups of languages.
        """
        return self._get_scope(self.pt3)

    def type(self) -> Optional[str]:
        """Get the type of the language according to ISO 639-3.

        Returns
        -------
        str
            The ISO 639-3 type of this language among 'Ancient',
            'Constructed', 'Extinct', 'Historical', 'Living' and'Special'.
            Returns None for groups of languages.
        """
        return self._get_type(self.pt3)

    def macro(self) -> Optional["Lang"]:
        """Get the macrolanguage of an individual language.

        Returns
        -------
        iso639.Lang
            The macrolanguage of the individual language, if there is one.
        """
        macro_pt3 = self._get_macro(self.pt3)
        return Lang(macro_pt3) if macro_pt3 else macro_pt3

    def individuals(self) -> List["Lang"]:
        """Get all individual languages of a macrolanguage.

        Returns
        -------
        list of Lang
            The `Lang` instances of the individual languages of a
            macrolanguage, sorted by name.
        """
        return [Lang(ind) for ind in self._get_individuals(self.pt3)]

    def other_names(self) -> List[str]:
        """Get all the names of this language that are not its reference name.

        Returns
        -------
        list of str
            The possible other ISO 639-3 printed names or ISO 639-3 inverted
            names or ISO 639-2 English names of the language, in alphabetical
            order.
        """
        return self._get_other_names(self.name)

    @classmethod
    def _validate_arg(cls, arg_value):
        if isinstance(arg_value, Lang):
            return tuple(map(lambda x: getattr(arg_value, x), cls._tags))
        elif isinstance(arg_value, str):
            if len(arg_value) == 3 and arg_value.lower() == arg_value:
                for tg in ("pt3", "pt2b", "pt2t", "pt5"):
                    lang_tuple = cls._get_language_tuple(tg, arg_value)
                    if lang_tuple:
                        return lang_tuple
            elif len(arg_value) == 2 and arg_value.lower() == arg_value:
                return cls._get_language_tuple("pt1", arg_value)
            else:
                return cls._get_language_tuple("name", arg_value)

        return tuple()

    @classmethod
    def _assert_not_deprecated(cls, arg_value):
        for key in ("id", "name"):
            try:
                d = cls._deprecated[key][arg_value]
            except KeyError:
                pass
            else:
                d[key] = arg_value
                raise DeprecatedLanguageValue(**d)

    @classmethod
    def _get_language_tuple(cls, tag, arg_value):
        if tag == "name":
            ref_value = cls._ref_name.get(arg_value, arg_value)
        else:
            ref_value = arg_value

        try:
            lang_dict = cls._data[tag][ref_value]
        except KeyError:
            lang_tuple = tuple()
        else:
            lang_dict[tag] = ref_value
            lang_tuple = itemgetter(*cls._tags)(lang_dict)

        return lang_tuple

    @classmethod
    def _get_scope(cls, pt3_value):
        abr = cls._scope.get(pt3_value)

        return cls._abrs.get(abr)

    @classmethod
    def _get_type(cls, pt3_value):
        abr = cls._type.get(pt3_value)

        return cls._abrs.get(abr)

    @classmethod
    def _get_macro(cls, pt3_value):
        return cls._macro["individual"].get(pt3_value)

    @classmethod
    def _get_individuals(cls, pt3_value):
        return cls._macro["macro"].get(pt3_value, [])

    @classmethod
    def _get_other_names(cls, ref_name_value):
        return cls._other_names.get(ref_name_value, [])


def iter_langs() -> Iterator[Lang]:
    """Iterate through all languages that are in ISO 639.

    Does not yield languages that are depracted according to ISO 639.

    Yields
    -------
    Lang
        `Lang` instances ordered alphabetically by reference name.
    """
    sorted_lang_names = load_file("list_langs")

    return (Lang(lang_name) for lang_name in sorted_lang_names)
