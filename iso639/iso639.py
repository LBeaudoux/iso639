from operator import itemgetter

from . import mapping
from .exceptions import DeprecatedLanguageValue, InvalidLanguageValue


class Lang(tuple):
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
    _data = mapping.ISO639Mapping().load()
    _scope = mapping.ScopeMapping().load()
    _type = mapping.TypeMapping().load()
    _macro = mapping.MacroMapping().load()
    _deprecated = mapping.DeprecatedMapping().load()

    __slots__ = ()  # set immutability of Lang

    def __new__(cls, *args, **kwargs):
        # validate positional argument
        if len(args) == 1:
            args_values = cls._validate_arg(args[0])
            if not args_values:
                raise InvalidLanguageValue(*args, **kwargs)
        else:
            args_values = tuple()

        # validate keyword arguments
        if kwargs:
            kwargs_values = cls._validate_kwargs(kwargs)
            if not kwargs_values:
                raise InvalidLanguageValue(*args, **kwargs)
        else:
            kwargs_values = tuple()

        # check compatiblity between positional and keyword arguments
        if args_values == kwargs_values and args_values:
            language_values = args_values
        elif args_values and not kwargs_values:
            language_values = args_values
        elif kwargs_values and not args_values:
            language_values = kwargs_values
        else:
            raise InvalidLanguageValue(*args, **kwargs)

        # instantiate as a tuple of ISO 639 language values
        return tuple.__new__(cls, language_values)

    def __repr__(self):
        chunks = ["=".join((tg, repr(getattr(self, tg)))) for tg in self._tags]

        return "Lang({})".format(", ".join(chunks))

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return isinstance(other, Lang) and hash(other) == hash(self)

    def __lt__(self, other):
        return other.name and self.name < other.name

    def __getnewargs__(self):
        unpickling_args = (self.name,)

        return unpickling_args

    @property
    def name(self):
        """Gets the ISO 639 name of this language"""
        return tuple.__getitem__(self, 0)

    @property
    def pt1(self):
        """Gets the ISO 639-1 code of this language"""
        return tuple.__getitem__(self, 1)

    @property
    def pt2b(self):
        """Gets the ISO 639-2B code of this language"""
        return tuple.__getitem__(self, 2)

    @property
    def pt2t(self):
        """Gets the ISO 639-2T code of this language"""
        return tuple.__getitem__(self, 3)

    @property
    def pt3(self):
        """Gets the ISO 639-3 code of this language"""
        return tuple.__getitem__(self, 4)

    @property
    def pt5(self):
        """Gets the ISO 639-5 code of this language"""
        return tuple.__getitem__(self, 5)

    def scope(self):
        """Gets the ISO 639-3 scope of this language

        Returns
        -------
        str
            the ISO 639-3 scope of this language among 'Individual',
            'Macrolanguage' and 'Special'.
            None is returned by not ISO 639-3 languages.
        """
        return self._get_scope(self.pt3)

    def type(self):
        """Gets the ISO 639-3 type of this language

        Returns
        -------
        str
            the ISO 639-3 type of this language among 'Ancient',
            'Constructed', 'Extinct', 'Historical', 'Living' and
            'Special'.
            None is returned by not ISO 639-3 languages.
        """
        return self._get_type(self.pt3)

    def macro(self):
        """Get the macrolanguage of this individual language

        Returns
        -------
        iso639.Lang
            the macrolanguage of this individual language, if there is one
        """
        macro_pt3 = self._get_macro(self.pt3)
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
        for lg in self._get_individuals(self.pt3):
            try:
                lang = Lang(lg)
            except InvalidLanguageValue:
                pass
            except DeprecatedLanguageValue as e:
                if e.change_to:
                    individuals.append(Lang(e.change_to))
            else:
                individuals.append(lang)

        return individuals

    @classmethod
    def _validate_arg(cls, arg):
        if isinstance(arg, Lang):
            return tuple(getattr(arg, tag) for tag in cls._tags)
        elif isinstance(arg, str):
            if len(arg) == 3 and arg.lower() == arg:
                cls._assert_not_deprecated(arg)
                for tg in ("pt3", "pt2b", "pt2t", "pt5"):
                    values = cls._get_language_values(tg, arg)
                    if values:
                        return values
            elif len(arg) == 2 and arg.lower() == arg:
                return cls._get_language_values("pt1", arg)
            else:
                return cls._get_language_values("name", arg)
        else:
            return tuple()

    @classmethod
    def _validate_kwargs(cls, kwargs):
        params = set()
        if all(isinstance(ka, str) for ka in kwargs.values()):
            cls._assert_not_deprecated(kwargs.get("pt3"))
            for tg, lg in kwargs.items():
                if lg:
                    params.add(cls._get_language_values(tg, lg))
        else:
            params.add(tuple())

        return params.pop() if len(params) == 1 else tuple()

    @classmethod
    def _assert_not_deprecated(cls, lang_value):
        try:
            d = cls._deprecated[lang_value]
        except KeyError:
            pass
        else:
            raise DeprecatedLanguageValue(id=lang_value, **d)

    @classmethod
    def _get_language_values(cls, tag, language_value):
        try:
            language_dict = cls._data[tag][language_value]
        except KeyError:
            language_tuple = tuple()
        else:
            language_dict[tag] = language_value
            language_tuple = itemgetter(*cls._tags)(language_dict)

        return language_tuple

    @classmethod
    def _get_scope(cls, pt3_value):
        abr = cls._scope.get(pt3_value, "")

        return cls._abrs.get(abr) if abr else None

    @classmethod
    def _get_type(cls, pt3_value):
        abr = cls._type.get(pt3_value, "")

        return cls._abrs.get(abr) if abr else None

    @classmethod
    def _get_macro(cls, pt3_value):
        return cls._macro["individual"].get(pt3_value, "")

    @classmethod
    def _get_individuals(cls, pt3_value):
        return cls._macro["macro"].get(pt3_value, [])
