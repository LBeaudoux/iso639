import unittest

from iso639 import Lang, iter_langs
from iso639.exceptions import DeprecatedLanguageValue, InvalidLanguageValue


class TestLang(unittest.TestCase):
    """Test the Lang class."""

    lang_vals = {tg: set(d.keys()) for tg, d in Lang._data.items()}
    lang_vals["changed_to"] = {
        d["change_to"] for d in Lang._deprecated.values() if d["change_to"]
    }
    lang_vals["deprecated"] = set(Lang._deprecated.keys())
    lang_vals["macro"] = set(Lang._macro["macro"].keys())
    lang_vals["individual"] = set(Lang._macro["individual"].keys())

    def test_pt1(self):
        lg = Lang("fr")
        self.assertEqual(lg.pt1, "fr")
        self.assertEqual(lg.pt2b, "fre")
        self.assertEqual(lg.pt2t, "fra")
        self.assertEqual(lg.pt3, "fra")
        self.assertEqual(lg.pt5, "")
        self.assertEqual(lg.name, "French")

    def test_upper_pt1(self):
        with self.assertRaises(InvalidLanguageValue):
            Lang("FR")

    def test_capitalized_pt1(self):
        with self.assertRaises(InvalidLanguageValue):
            Lang("Fr")

    def test_pt2b(self):
        lg = Lang("fre")
        self.assertEqual(lg.pt1, "fr")
        self.assertEqual(lg.pt2b, "fre")
        self.assertEqual(lg.pt2t, "fra")
        self.assertEqual(lg.pt3, "fra")
        self.assertEqual(lg.pt5, "")
        self.assertEqual(lg.name, "French")

    def test_pt2t(self):
        lg = Lang("deu")
        self.assertEqual(lg.pt1, "de")
        self.assertEqual(lg.pt2b, "ger")
        self.assertEqual(lg.pt2t, "deu")
        self.assertEqual(lg.pt3, "deu")
        self.assertEqual(lg.pt5, "")
        self.assertEqual(lg.name, "German")

    def test_pt5(self):
        lg = Lang("ber")
        self.assertEqual(lg.pt1, "")
        self.assertEqual(lg.pt2b, "ber")
        self.assertEqual(lg.pt2t, "")
        self.assertEqual(lg.pt3, "")
        self.assertEqual(lg.pt5, "ber")
        self.assertEqual(lg.name, "Berber languages")

    def test_pt3_with_other_pts(self):
        lg = Lang("eng")
        self.assertEqual(lg.pt1, "en")
        self.assertEqual(lg.pt2b, "eng")
        self.assertEqual(lg.pt2t, "eng")
        self.assertEqual(lg.pt3, "eng")
        self.assertEqual(lg.pt5, "")
        self.assertEqual(lg.name, "English")

    def test_pt3_without_other_pts(self):
        lg = Lang("cmn")
        self.assertEqual(lg.pt1, "")
        self.assertEqual(lg.pt2b, "")
        self.assertEqual(lg.pt2t, "")
        self.assertEqual(lg.pt3, "cmn")
        self.assertEqual(lg.pt5, "")
        self.assertEqual(lg.name, "Mandarin Chinese")

    def test_upper_pt3(self):
        with self.assertRaises(InvalidLanguageValue):
            Lang("ENG")

    def test_capitalized_pt3(self):
        with self.assertRaises(InvalidLanguageValue):
            Lang("Eng")

    def test_name(self):
        lg = Lang("German")
        self.assertEqual(lg.pt1, "de")
        self.assertEqual(lg.pt2b, "ger")
        self.assertEqual(lg.pt2t, "deu")
        self.assertEqual(lg.pt3, "deu")
        self.assertEqual(lg.pt5, "")
        self.assertEqual(lg.name, "German")

    def test_other_name(self):
        # pt3 printed name
        self.assertEqual(Lang("uig"), Lang("Uyghur"))
        self.assertEqual(Lang("Uighur"), Lang("Uyghur"))
        # pt3 inverted name
        self.assertEqual(Lang("cmn"), Lang("Chinese, Mandarin"))
        self.assertEqual(Lang("Mandarin Chinese"), Lang("Chinese, Mandarin"))
        # pt2b English name
        self.assertEqual(Lang("ast"), Lang("Bable"))
        self.assertEqual(Lang("Asturian"), Lang("Bable"))

    def test_lower_name(self):
        with self.assertRaises(InvalidLanguageValue):
            Lang("german")

    def test_upper_name(self):
        with self.assertRaises(InvalidLanguageValue):
            Lang("GERMAN")

    def test_asdict(self):
        lg = Lang("fra")
        self.assertEqual(
            lg.asdict(),
            {
                "name": "French",
                "pt1": "fr",
                "pt2b": "fre",
                "pt2t": "fra",
                "pt3": "fra",
                "pt5": "",
            },
        )

    def test_equal_languages(self):
        lg1 = Lang("eng")
        lg2 = Lang("en")
        self.assertEqual(lg1, lg2)

    def test_not_equal_languages(self):
        lg1 = Lang("fra")
        lg2 = Lang("eng")
        self.assertNotEqual(lg1, lg2)

    def test_not_equal_languages_string(self):
        lg1 = Lang("fra")
        lg2 = "fra"
        self.assertNotEqual(lg1, lg2)

    def test_not_equal_languages_None(self):
        lg1 = Lang("fra")
        lg2 = None
        self.assertNotEqual(lg1, lg2)

    def test_lang_of_lang(self):
        lg1 = Lang("fra")
        lg2 = Lang(lg1)
        self.assertEqual(lg1, lg2)

    def test_multiple_args(self):
        with self.assertRaises(InvalidLanguageValue):
            Lang("fra", "fr")

    def test_kwarg(self):
        lg = Lang(pt1="fr")
        self.assertEqual(lg.pt1, "fr")
        self.assertEqual(lg.pt2b, "fre")
        self.assertEqual(lg.pt2t, "fra")
        self.assertEqual(lg.pt3, "fra")
        self.assertEqual(lg.pt5, "")
        self.assertEqual(lg.name, "French")

    def test_multiple_kwargs(self):
        lg = Lang(pt1="fr", name="French")
        self.assertEqual(lg.pt1, "fr")
        self.assertEqual(lg.pt2b, "fre")
        self.assertEqual(lg.pt2t, "fra")
        self.assertEqual(lg.pt3, "fra")
        self.assertEqual(lg.pt5, "")
        self.assertEqual(lg.name, "French")

    def test_kwarg_wrong_value(self):
        with self.assertRaises(InvalidLanguageValue):
            Lang(pt1="fra")

    def test_kwargs_wrong_second_value(self):
        with self.assertRaises(InvalidLanguageValue):
            Lang(pt1="fr", pt3="deu")

    def test_kwargs_right_empty_second_value(self):
        Lang(pt1="fr", pt5="")

    def test_kwarg_wrong_key(self):
        with self.assertRaises(InvalidLanguageValue):
            Lang(foobar="fr")

    def test_kwarg_wrong_second_key(self):
        with self.assertRaises(InvalidLanguageValue):
            Lang(pt1="fr", foobar="fra")

    def test_no_arg_no_kwarg(self):
        with self.assertRaises(InvalidLanguageValue):
            Lang()

    def test_none_arg(self):
        with self.assertRaises(InvalidLanguageValue):
            Lang(None)

    def test_none_kwarg(self):
        for tag in Lang._tags:
            kwargs = {tag: ""}
            with self.assertRaises(InvalidLanguageValue):
                Lang(**kwargs)

    def test_empty_string_arg(self):
        with self.assertRaises(InvalidLanguageValue):
            Lang("")

    def test_empty_string_kwarg(self):
        for tag in Lang._tags:
            kwargs = {tag: ""}
            with self.assertRaises(InvalidLanguageValue):
                Lang(**kwargs)

    def test_arg_and_kwarg(self):
        lg = Lang("fra", pt1="fr")
        self.assertEqual(lg.pt1, "fr")
        self.assertEqual(lg.pt2b, "fre")
        self.assertEqual(lg.pt2t, "fra")
        self.assertEqual(lg.pt3, "fra")
        self.assertEqual(lg.pt5, "")
        self.assertEqual(lg.name, "French")

    def test_arg_and_kwarg_nok(self):
        with self.assertRaises(InvalidLanguageValue):
            Lang("fra", pt1="deu")

    def test_repr(self):
        lg = Lang("alu")
        s = (
            """Lang(name="'Are'are", pt1='', pt2b='', """
            """pt2t='', pt3='alu', pt5='')"""
        )
        self.assertEqual(s, repr(lg))

    def test_immutable(self):
        lg = Lang("fra")
        with self.assertRaises(AttributeError):
            lg.pt1 = "en"

    def test_hashable_set_element(self):
        lg = Lang("fra")
        s = set()
        s.add(lg)
        self.assertIn(lg, s)

    def test_hashable_dict_key(self):
        lg = Lang("fra")
        d = {}
        d.update({lg: "foobar"})
        self.assertEqual(d[lg], "foobar")

    def test_scope(self):
        self.assertEqual(Lang("fra").scope(), "Individual")
        self.assertEqual(Lang("zh").scope(), "Macrolanguage")
        self.assertEqual(Lang("und").scope(), "Special")
        self.assertIsNone(Lang("ber").scope())

    def test_type(self):
        self.assertEqual(Lang("epo").type(), "Constructed")
        self.assertEqual(Lang("djf").type(), "Extinct")
        self.assertEqual(Lang("lat").type(), "Historical")
        self.assertEqual(Lang("fra").type(), "Living")
        self.assertEqual(Lang("und").type(), "Special")
        self.assertIsNone(Lang("ber").type())

    def test_macro(self):
        lg = Lang("cmn")
        self.assertEqual(lg.macro().pt3, "zho")

    def test_individuals(self):
        individuals_pt3 = [x.pt3 for x in Lang("ara").individuals()]
        self.assertIn("apc", individuals_pt3)
        self.assertEqual(len(individuals_pt3), len(set(individuals_pt3)))

    def test_other_names(self):
        # pt3 printed name
        lg = Lang("Uighur")
        self.assertAlmostEqual(lg.other_names(), ["Uyghur"])
        # pt3 inverted name
        lg = Lang("cmn")
        self.assertAlmostEqual(lg.other_names(), ["Chinese, Mandarin"])
        # pt2b English names
        lg = Lang("ast")
        self.assertAlmostEqual(
            lg.other_names(), ["Asturleonese", "Bable", "Leonese"]
        )
        # no other name
        lg = Lang("fra")
        self.assertAlmostEqual(lg.other_names(), [])

    def test_deprecated_arg(self):
        for pt3 in self.lang_vals["deprecated"]:
            with self.assertRaises(DeprecatedLanguageValue):
                Lang(pt3)

    def test_deprecated_kwarg(self):
        for pt3 in self.lang_vals["deprecated"]:
            with self.assertRaises(DeprecatedLanguageValue):
                Lang(pt3=pt3)

    def test_deprecated_with_change_to(self):
        for pt in ("name", "pt1", "pt2b", "pt2t", "pt3", "pt5"):
            for lv in self.lang_vals[pt]:
                try:
                    Lang(lv)
                except DeprecatedLanguageValue as e:
                    if e.change_to:
                        Lang(e.change_to)

    def test_no_macro_of_macro(self):
        for lvs in self.lang_vals.values():
            for lv in lvs:
                try:
                    macro = Lang(lv).macro()
                except DeprecatedLanguageValue:
                    continue
                else:
                    if macro is not None:
                        self.assertIsNone(macro.macro())

    def test_no_individual_of_individual(self):
        for lvs in self.lang_vals.values():
            for lv in lvs:
                try:
                    individuals = Lang(lv).individuals()
                except DeprecatedLanguageValue:
                    continue
                else:
                    for ind in individuals:
                        self.assertEqual(ind.individuals(), [])

    def test_iter_langs(self):
        lg1 = next(iter_langs()).name
        lgs = [lg.name for lg in iter_langs()]
        self.assertEqual(lg1, lgs[0])
        self.assertEqual(len(set(lgs)), len(lgs))


if __name__ == "__main__":
    unittest.main()
