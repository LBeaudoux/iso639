import pytest

from iso639 import Lang, iter_langs
from iso639.exceptions import DeprecatedLanguageValue, InvalidLanguageValue


def test_top_example():
    assert repr(Lang("French")) == (
        "Lang(name='French', pt1='fr', pt2b='fre', pt2t='fra', pt3='fra', "
        "pt5='')"
    )


def test_example_language():
    lg = Lang("deu")
    assert lg.name == "German"
    assert lg.pt1 == "de"
    assert lg.pt2b == "ger"
    assert lg.pt2t == "deu"
    assert lg.pt3 == "deu"


def test_example_group_of_languages():
    lg = Lang("cel")
    assert lg.name == "Celtic languages"
    assert lg.pt2b == "cel"
    assert lg.pt2t == "cel"
    assert lg.pt5 == "cel"


def test_example_any_id_or_ref_name():
    assert Lang("German") == Lang("de") == Lang("deu") == Lang("ger")


def test_example_iso6393_inverted_name():
    s = (
        "Lang(name='Mandarin Chinese', "
        "pt1='', pt2b='', pt2t='', pt3='cmn', pt5='')"
    )
    assert repr(Lang("Chinese, Mandarin")) == s


def test_example_iso6393_printed_name():
    s = (
        "Lang(name='Uighur', "
        "pt1='ug', pt2b='uig', pt2t='uig', pt3='uig', pt5='')"
    )
    assert repr(Lang("Uyghur")) == s


def test_example_iso6392_english_name():
    s = (
        "Lang(name='Catalan', "
        "pt1='ca', pt2b='cat', pt2t='cat', pt3='cat', pt5='')"
    )
    assert repr(Lang("Valencian")) == s


def test_example_case_sensitive():
    s = (
        "Lang(name='Akan', "
        "pt1='ak', pt2b='aka', pt2t='aka', pt3='aka', pt5='')"
    )
    assert repr(Lang("ak")) == s
    s = "Lang(name='Ak', pt1='', pt2b='', pt2t='', pt3='akq', pt5='')"
    assert repr(Lang("Ak")) == s


def test_example_asdict():
    assert Lang("fra").asdict() == {
        "name": "French",
        "pt1": "fr",
        "pt2b": "fre",
        "pt2t": "fra",
        "pt3": "fra",
        "pt5": "",
    }


def test_example_sorted_list():
    a = [lg.name for lg in sorted([Lang("deu"), Lang("rus"), Lang("eng")])]
    assert a == ["English", "German", "Russian"]


def test_example_dict_keys():
    d = {Lang("de"): "foo", Lang("fr"): "bar"}
    s = (
        "{Lang(name='German', "
        "pt1='de', pt2b='ger', pt2t='deu', pt3='deu', pt5=''): 'foo', "
        "Lang(name='French', pt1='fr', "
        "pt2b='fre', pt2t='fra', pt3='fra', pt5=''): 'bar'}"
    )
    assert repr(d) == s


def test_example_iter_langs_list():
    a = [lg.name for lg in iter_langs()]
    assert a[:3] == ["'Are'are", "'Auhelawa", "A'ou"]
    assert a[-3:] == ["ǂHua", "ǂUngkue", "ǃXóõ"]


def test_example_type():
    lg = Lang("Latin")
    assert lg.type() == "Historical"


def test_example_scope():
    lg = Lang("Arabic")
    assert lg.scope() == "Macrolanguage"


def test_example_macro():
    lg = Lang("Wu Chinese")
    s = (
        "Lang(name='Chinese', "
        "pt1='zh', pt2b='chi', pt2t='zho', pt3='zho', pt5='')"
    )
    assert repr(lg.macro()) == s


def test_example_individuals():
    lg = Lang("Persian")
    s = (
        "[Lang(name='Iranian Persian', "
        "pt1='', pt2b='', pt2t='', pt3='pes', pt5=''), "
        "Lang(name='Dari', "
        "pt1='', pt2b='', pt2t='', pt3='prs', pt5='')]"
    )
    assert repr(lg.individuals()) == s


def test_example_other_names():
    lg = Lang("ast")
    assert lg.name == "Asturian"
    assert lg.other_names() == ["Asturleonese", "Bable", "Leonese"]


def test_example_invalid_value():
    with pytest.raises(InvalidLanguageValue) as exc_info:
        Lang("foobar")
    s = "'foobar' is not a valid Lang argument."
    assert exc_info.value.msg == s


def test_example_deprecated_value():
    with pytest.raises(DeprecatedLanguageValue) as exc_info:
        Lang("gsc")
    assert exc_info.value.name == "Gascon"
    lg = Lang(exc_info.value.change_to)
    assert lg.name == "Occitan (post 1500)"
