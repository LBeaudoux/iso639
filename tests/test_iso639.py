import pytest

from iso639 import Lang, iter_langs
from iso639.exceptions import InvalidLanguageValue


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
        Lang("fra", "French", "fr", "fre", "fra", "fra") == Lang("French")

    def test_wrong_multiple_args(self):
        with pytest.raises(InvalidLanguageValue):
            Lang("fra", "fr")

    def test_one_kwarg(self):
        assert Lang(pt1="fr") == Lang("fr")

    def test_one_wrong_kwarg(self):
        with pytest.raises(InvalidLanguageValue):
            Lang(name="fr")

    def test_mutliple_kwargs(self):
        Lang(
            name="French", pt1="fr", pt2b="fre", pt2t="fra", pt3="fra"
        ) == Lang("French")

    def test_mutliple_wrong_kwargs(self):
        with pytest.raises(InvalidLanguageValue):
            Lang(name="French", pt1="en")

    def test_kwarg_wrong_key(self):
        with pytest.raises(TypeError):
            Lang(foobar="fr")

    def test_kwarg_wrong_value(self):
        with pytest.raises(InvalidLanguageValue):
            Lang(name_or_identifier="foobar")

    def test_no_arg_no_kwarg(self):
        with pytest.raises(InvalidLanguageValue):
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


def test_iter_langs():
    lg1 = next(iter_langs())
    lgs = [lg for lg in iter_langs()]
    assert all(isinstance(lg, Lang) for lg in lgs)
    assert lg1 == lgs[0]
    assert len(set(lgs)) == len(lgs)
