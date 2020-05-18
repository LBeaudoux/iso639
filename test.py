import unittest

from iso639 import Lang
from iso639.exceptions import InvalidLanguageValue


class TestLang(unittest.TestCase):
    """Test the Lang class.
    """

    def test_pt1(self):
        lg = Lang("fr")
        self.assertEqual(lg.pt1, "fr")
        self.assertEqual(lg.pt3, "fra")
        self.assertEqual(lg.name, "French")

    def test_upper_pt1(self):
        self.assertRaises(InvalidLanguageValue, Lang, "FR")

    def test_capitalized_pt1(self):
        self.assertRaises(InvalidLanguageValue, Lang, "Fr")        

    def test_pt3_with_pt1(self):
        lg = Lang("eng")
        self.assertEqual(lg.pt1, "en")
        self.assertEqual(lg.pt3, "eng")
        self.assertEqual(lg.name, "English")

    def test_pt3_without_pt1(self):
        lg = Lang("cmn")
        self.assertEqual(lg.pt1, "")
        self.assertEqual(lg.pt3, "cmn")
        self.assertEqual(lg.name, "Mandarin Chinese")

    def test_upper_pt3(self):
        self.assertRaises(InvalidLanguageValue, Lang, "ENG")

    def test_capitalized_pt3(self):
        self.assertRaises(InvalidLanguageValue, Lang, "Eng")           

    def test_name(self):
        lg = Lang("German")
        self.assertEqual(lg.pt1, "de")
        self.assertEqual(lg.pt3, "deu")
        self.assertEqual(lg.name, "German")

    def test_lower_name(self):
        self.assertRaises(InvalidLanguageValue, Lang, "german")

    def test_upper_name(self):
        self.assertRaises(InvalidLanguageValue, Lang, "GERMAN")        


if __name__ == "__main__":
    unittest.main()
