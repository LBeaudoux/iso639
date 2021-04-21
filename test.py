import unittest

from iso639 import Lang
from iso639.exceptions import InvalidLanguageValue


class TestLang(unittest.TestCase):
    """Test the Lang class."""

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

    def test_lower_name(self):
        with self.assertRaises(InvalidLanguageValue):
            Lang("german")

    def test_upper_name(self):
        with self.assertRaises(InvalidLanguageValue):
            Lang("GERMAN")

    def test_equal_languages(self):
        lg1 = Lang("eng")
        lg2 = Lang("eng")
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

    def test_multiple_arg(self):
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

    def test_multiple_kwarg(self):
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

    def test_kwarg_wrong_second_value(self):
        with self.assertRaises(InvalidLanguageValue):
            Lang(pt1="fr", pt3="deu")

    def test_kwarg_wrong_key(self):
        with self.assertRaises(InvalidLanguageValue):
            Lang(foobar="fr")

    def test_kwarg_wrong_second_key(self):
        with self.assertRaises(InvalidLanguageValue):
            Lang(pt1="fr", foobar="fra")

    def test_no_param(self):
        with self.assertRaises(InvalidLanguageValue):
            Lang()

    def test_arg_and_kwarg(self):
        with self.assertRaises(InvalidLanguageValue):
            Lang("fra", pt1="fr")

    def test_attribute_setter(self):
        lg = Lang("spa")
        for k, v in [
            ("pt1", "de"),
            ("pt2b", "fre"),
            ("pt2t", "deu"),
            ("pt3", "cmn"),
            ("name", "Italian"),
        ]:
            lg[k] = v
            self.assertEqual(getattr(lg, k), v)
            self.assertEqual(lg, Lang(v))

    def test_macro(self):
        lg = Lang("cmn")
        self.assertEqual(lg.macro().pt3, "zho")

    def test_individuals(self):
        lg = Lang("fas")
        ind_lgs = {x.pt3 for x in lg.individuals()}
        self.assertIn("pes", ind_lgs)


if __name__ == "__main__":
    unittest.main()
