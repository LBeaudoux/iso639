import pytest

from iso639 import Lang, iter_langs
from iso639.exceptions import DeprecatedLanguageValue, InvalidLanguageValue

from .utils import (
    get_iso6391_deprecated_ids_rows,
    get_iso6391_deprecated_names_rows,
    get_iso6392_deprecated_ids_rows,
    get_iso6392_deprecated_names_rows,
    get_iso6392_rows,
    get_iso6393_deprecated_ids_rows,
    get_iso6393_deprecated_names_rows,
    get_iso6393_macrolanguages_rows,
    get_iso6393_names_rows,
    get_iso6393_rows,
    get_iso6395_rows,
)


class TestLang:

    def test_upper_pt1(self):
        with pytest.raises(InvalidLanguageValue):
            Lang("FR")

    def test_capitalized_pt1(self):
        with pytest.raises(InvalidLanguageValue):
            Lang("Fr")

    def test_upper_pt3(self):
        with pytest.raises(InvalidLanguageValue):
            Lang("ENG")

    def test_capitalized_pt3(self):
        with pytest.raises(InvalidLanguageValue):
            Lang("Eng")

    def test_lower_name(self):
        with pytest.raises(InvalidLanguageValue):
            Lang("german")

    def test_upper_name(self):
        with pytest.raises(InvalidLanguageValue):
            Lang("GERMAN")

    def test_not_equal_languages(self):
        lg1 = Lang("fra")
        lg2 = Lang("eng")
        assert lg1 != lg2

    def test_not_equal_languages_string(self):
        lg1 = Lang("fra")
        lg2 = "fra"
        assert lg1 != lg2

    def test_not_equal_languages_None(self):
        lg1 = Lang("fra")
        lg2 = None
        assert lg1 != lg2

    def test_multiple_args(self):
        with pytest.raises(TypeError):
            Lang("fra", "fr")

    def test_mutliple_kwargs(self):
        with pytest.raises(TypeError):
            Lang(name_or_identifier="fr", pt3="fra")

    def test_kwarg_wrong_key(self):
        with pytest.raises(TypeError):
            Lang(foobar="fr")

    def test_kwarg_wrong_value(self):
        with pytest.raises(InvalidLanguageValue):
            Lang(name_or_identifier="foobar")

    def test_no_arg_no_kwarg(self):
        with pytest.raises(TypeError):
            Lang()

    def test_none_arg(self):
        with pytest.raises(InvalidLanguageValue):
            Lang(None)

    def test_empty_string_arg(self):
        with pytest.raises(InvalidLanguageValue):
            Lang("")

    def test_repr(self):
        lg = Lang("alu")
        s = (
            """Lang(name="'Are'are", pt1='', pt2b='', """
            """pt2t='', pt3='alu', pt5='')"""
        )
        assert s == repr(lg)

    def test_immutable(self):
        lg = Lang("fra")
        with pytest.raises(AttributeError):
            lg.pt1 = "en"

    def test_hashable_set_element(self):
        lg = Lang("fra")
        s = set()
        s.add(lg)
        assert lg in s

    def test_hashable_dict_key(self):
        lg = Lang("fra")
        d = {}
        d.update({lg: "foobar"})
        assert d[lg] == "foobar"

    @pytest.mark.parametrize(
        "Part2b, Part2t, Part1, English_Name, French_Name",
        get_iso6392_rows(),
    )
    def test_iso6392_rows(
        self, Part2b, Part2t, Part1, English_Name, French_Name
    ):

        lg = Lang(Part2b)
        pt2t = Part2t if Part2t else Part2b  # Part2B is default Part2T
        assert lg.pt1 == Part1
        assert lg.pt2b == Part2b
        assert lg.pt2t == pt2t
        assert lg == Lang(lg)
        assert not Part1 or lg == Lang(Part1)
        assert lg == Lang(pt2t)

        for english_name in English_Name.split("; "):
            d = {"pt1": Part1, "pt2b": Part2b, "pt2t": pt2t}
            assert lg == Lang(english_name)
            assert d.items() <= lg.asdict().items()

    @pytest.mark.parametrize(
        "Id, Part2b, Part2t, Part1, Scope, Language_Type, Ref_Name, Comment",
        get_iso6393_rows(),
    )
    def test_iso6393_rows(
        self,
        Id,
        Part2b,
        Part2t,
        Part1,
        Scope,
        Language_Type,
        Ref_Name,
        Comment,
    ):
        lg = Lang(Id)
        assert lg.name == Ref_Name
        assert lg.pt1 == Part1
        assert lg.pt2b == Part2b
        assert lg.pt2t == Part2t
        assert lg.pt3 == Id
        assert lg.pt5 == ""
        assert lg == Lang(lg)
        assert lg == Lang(Ref_Name)
        assert not Part1 or lg == Lang(Part1)
        assert not Part2b or lg == Lang(Part2b)
        assert not Part2t or lg == Lang(Part2t)
        abbreviations = {
            "A": "Ancient",
            "C": "Constructed",
            "E": "Extinct",
            "H": "Historical",
            "I": "Individual",
            "L": "Living",
            "M": "Macrolanguage",
            "S": "Special",
        }
        assert lg.scope() == abbreviations[Scope]
        assert lg.type() == abbreviations[Language_Type]
        d = {"name": Ref_Name, "pt1": Part1, "pt2b": Part2b, "pt2t": Part2t}
        assert d.items() <= lg.asdict().items()

    @pytest.mark.parametrize(
        "Id, Print_Name, Inverted_Name",
        get_iso6393_names_rows(),
    )
    def test_iso6393_names_rows(self, Id, Print_Name, Inverted_Name):
        lg = Lang(Id)
        assert lg.pt3 == Id
        assert lg == Lang(Print_Name)
        assert lg == Lang(Inverted_Name)

        assert lg.name == Print_Name or lg.other_names().count(Print_Name) == 1
        assert (
            lg.name == Inverted_Name
            or lg.other_names().count(Inverted_Name) == 1
        )
        assert lg.other_names() == sorted(lg.other_names())
        assert len(lg.other_names()) == len(set(lg.other_names()))

    @pytest.mark.parametrize(
        "M_Id, I_Id, I_Status",
        get_iso6393_macrolanguages_rows(),
    )
    def test_iso6393_macrolanguages_rows(self, M_Id, I_Id, I_Status):
        macro = Lang(M_Id)
        indiv = Lang(I_Id)

        assert indiv.macro() == macro
        assert macro.individuals().count(indiv) == 1
        assert macro.macro() is None
        assert indiv.individuals() == []
        assert macro.individuals() == sorted(
            macro.individuals(), key=lambda x: x.pt3
        )
        assert len(macro.individuals()) == len(set(macro.individuals()))

    @pytest.mark.parametrize(
        "URI, code, Label_English, Label_French",
        get_iso6395_rows(),
    )
    def test_iso6395_rows(self, URI, code, Label_English, Label_French):
        lg = Lang(code)
        assert lg.name == Label_English
        assert lg.pt5 == code
        assert lg == Lang(lg)
        kwargs = {"name": Label_English, "pt5": code}
        assert kwargs.items() <= lg.asdict().items()

    @pytest.mark.parametrize(
        "Id, Change_To, English_Name, French_Name, Date_Added_Or_Changed, "
        "Category_Of_Change, Notes",
        get_iso6391_deprecated_ids_rows(),
    )
    def test_iso6391_deprecated_ids(
        self,
        Id,
        Change_To,
        English_Name,
        French_Name,
        Date_Added_Or_Changed,
        Category_Of_Change,
        Notes,
    ):

        with pytest.raises(DeprecatedLanguageValue) as exc_info:
            Lang(Id)

        assert exc_info.value.id == Id
        assert exc_info.value.name == English_Name
        assert exc_info.value.reason == Category_Of_Change
        assert exc_info.value.change_to == Change_To
        assert exc_info.value.ret_remedy == Notes
        assert exc_info.value.effective == Date_Added_Or_Changed

        if exc_info.value.change_to:
            lg = Lang(exc_info.value.change_to)
            assert lg.pt1 == Change_To

    @pytest.mark.parametrize(
        "Id, Change_To, English_Name, French_Name, Date_Added_Or_Changed, "
        "Category_Of_Change, Notes",
        get_iso6391_deprecated_names_rows(),
    )
    def test_iso6391_deprecated_names(
        self,
        Id,
        Change_To,
        English_Name,
        French_Name,
        Date_Added_Or_Changed,
        Category_Of_Change,
        Notes,
    ):

        with pytest.raises(DeprecatedLanguageValue) as exc_info:
            Lang(English_Name)

        assert exc_info.value.id == Id
        assert exc_info.value.name == English_Name
        assert exc_info.value.reason == Category_Of_Change
        assert exc_info.value.change_to == Change_To
        assert exc_info.value.ret_remedy == Notes
        assert exc_info.value.effective == Date_Added_Or_Changed

        if exc_info.value.change_to:
            lg = Lang(exc_info.value.change_to)
            assert lg.pt1 == Change_To

    @pytest.mark.parametrize(
        "Id, Change_To, English_Name, French_Name, Date_Added_Or_Changed, "
        "Category_Of_Change, Notes",
        get_iso6392_deprecated_ids_rows(),
    )
    def test_iso6392_deprecated_ids(
        self,
        Id,
        Change_To,
        English_Name,
        French_Name,
        Date_Added_Or_Changed,
        Category_Of_Change,
        Notes,
    ):

        with pytest.raises(DeprecatedLanguageValue) as exc_info:
            Lang(Id)

        assert exc_info.value.id == Id
        assert exc_info.value.name == English_Name
        assert exc_info.value.reason == Category_Of_Change
        assert exc_info.value.change_to == Change_To
        assert exc_info.value.ret_remedy == Notes
        assert exc_info.value.effective == Date_Added_Or_Changed

        if exc_info.value.change_to:
            lg = Lang(exc_info.value.change_to)
            assert lg.pt2b == Change_To

    @pytest.mark.parametrize(
        "Id, Change_To, English_Name, French_Name, Date_Added_Or_Changed, "
        "Category_Of_Change, Notes",
        get_iso6392_deprecated_names_rows(),
    )
    def test_iso6392_deprecated_names(
        self,
        Id,
        Change_To,
        English_Name,
        French_Name,
        Date_Added_Or_Changed,
        Category_Of_Change,
        Notes,
    ):

        with pytest.raises(DeprecatedLanguageValue) as exc_info:
            Lang(English_Name)

        assert exc_info.value.id == Id
        assert English_Name in exc_info.value.name
        assert exc_info.value.reason == Category_Of_Change
        assert exc_info.value.change_to == Change_To
        assert exc_info.value.ret_remedy == Notes
        assert exc_info.value.effective == Date_Added_Or_Changed

        if exc_info.value.change_to:
            lg = Lang(exc_info.value.change_to)
            assert lg.pt2b == Change_To

    @pytest.mark.parametrize(
        "Id, Ref_Name, Ret_Reason, Change_To, Ret_Remedy, Effective",
        get_iso6393_deprecated_ids_rows(),
    )
    def test_iso6393_deprecated_ids(
        self,
        Id,
        Ref_Name,
        Ret_Reason,
        Change_To,
        Ret_Remedy,
        Effective,
    ):
        with pytest.raises(DeprecatedLanguageValue) as exc_info:
            Lang(Id)

        assert exc_info.value.id == Id
        assert exc_info.value.name == Ref_Name
        assert exc_info.value.reason == Ret_Reason
        assert exc_info.value.change_to == Change_To
        assert exc_info.value.ret_remedy == Ret_Remedy
        assert exc_info.value.effective == Effective

        if exc_info.value.change_to:
            lg = Lang(exc_info.value.change_to)
            assert lg.pt3 == Change_To

    @pytest.mark.parametrize(
        "Id, Ref_Name, Ret_Reason, Change_To, Ret_Remedy, Effective",
        get_iso6393_deprecated_names_rows(),
    )
    def test_iso6393_deprecated_names(
        self,
        Id,
        Ref_Name,
        Ret_Reason,
        Change_To,
        Ret_Remedy,
        Effective,
    ):
        with pytest.raises(DeprecatedLanguageValue) as exc_info:
            Lang(Ref_Name)

        assert exc_info.value.id == Id
        assert exc_info.value.name == Ref_Name
        assert exc_info.value.reason == Ret_Reason
        assert exc_info.value.change_to == Change_To
        assert exc_info.value.ret_remedy == Ret_Remedy
        assert exc_info.value.effective == Effective

        if exc_info.value.change_to:
            lg = Lang(exc_info.value.change_to)
            assert lg.pt3 == Change_To


def test_iter_langs():
    lg1 = next(iter_langs())
    lgs = [lg for lg in iter_langs()]
    assert all(isinstance(lg, Lang) for lg in lgs)
    assert lg1 == lgs[0]
    assert len(set(lgs)) == len(lgs)
