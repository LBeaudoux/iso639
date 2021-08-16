import json
from collections import namedtuple

from pkg_resources import resource_filename

FILENAMES = {
    "core": "data/iso-639-3.tab",
    "pt2": "data/ISO-639-2_utf-8.txt",
    "pt5": "data/iso639-5.tsv",
    "macro": "data/iso-639-3-macrolanguages.tab",
    "deprecated": "data/iso-639-3_Retirements.tab",
    "mapping": "data/iso-639.json",
    "mapping_macro": "data/iso-639_macro.json",
    "mapping_deprecated": "data/iso-639_deprecated.json",
}
TAGS = ("pt1", "pt2b", "pt2t", "pt3", "pt5", "name")


class ISO639Mapping:
    """A mapping used to query the ISO 639 values efficiently"""

    _fps = {
        k: resource_filename(__package__, FILENAMES[k])
        for k in ("core", "pt2", "pt5", "mapping")
    }

    def __init__(self):

        self._data = {}

    def load(self):
        """Load data from local JSON file"""
        try:
            with open(self._fps["mapping"], encoding="utf-8") as f:
                self._data = json.load(f)
        except FileNotFoundError:
            self.build()
            self.save()
        else:
            # remap if the mapping is incomplete
            if any(k not in self._data.keys() for k in TAGS):
                self.build()
                self.save()

        return self._data

    def save(self):
        """Save data into local JSON file"""
        with open(self._fps["mapping"], "w", encoding="utf-8") as f:
            json.dump(self._data, f)

    def build(self):
        """Build the JSON file from the official ISO 639 code tables
        stored locally
        """
        mapping = self._build_core_mapping()
        mapping = self._complete_part2(mapping)
        mapping = self._add_part5(mapping)

        self._data = self._sort_alphabetically(mapping)

    @classmethod
    def _build_core_mapping(cls):
        """Builds the core ISO-639 mapping from the ISO 639-3 tab file"""
        Iso6393 = namedtuple(
            "Iso6393",
            [
                "Id",
                "Part2B",
                "Part2T",
                "Part1",
                "Scope",
                "Language_Type",
                "Ref_Name",
            ],
        )
        mapping = {}
        with open(cls._fps["core"], encoding="utf-8") as f:
            next(f)
            for line in f:
                row = line.rstrip().split("\t")
                iso6393 = Iso6393(*row[:7])

                dict_iso6393 = {
                    "pt1": iso6393.Part1,
                    "pt2b": iso6393.Part2B,
                    "pt2t": iso6393.Part2T,
                    "pt3": iso6393.Id,
                    "pt5": "",
                    "name": iso6393.Ref_Name,
                }
                for tag in TAGS:
                    if dict_iso6393[tag]:
                        mapping.setdefault(tag, {})[dict_iso6393[tag]] = {
                            k: v for k, v in dict_iso6393.items() if k != tag
                        }

        return mapping

    @classmethod
    def _complete_part2(cls, mapping):
        """Complete mapping with pt2 codes not covered by pt3"""
        Iso6392 = namedtuple(
            "Iso6392",
            [
                "alpha3_bibliographic",
                "alpha3_terminologic",
                "alpha2",
                "English_name",
                "French_name",
            ],
        )
        with open(cls._fps["pt2"], encoding="utf-8-sig") as f:
            for line in f:
                row = line.rstrip().split("|")
                iso6392 = Iso6392(*row)

                params = {
                    "pt1": iso6392.alpha2,
                    "pt2b": iso6392.alpha3_bibliographic,
                    "pt2t": iso6392.alpha3_terminologic,
                    "pt3": "",
                    "pt5": "",
                    "name": iso6392.English_name,
                }
                if len(params["pt2b"]) == 3:
                    for tag in TAGS:
                        if params[tag] and params[tag] not in mapping[tag]:
                            mapping.setdefault(tag, {})[params[tag]] = {
                                k: v for k, v in params.items() if k != tag
                            }
        return mapping

    @classmethod
    def _add_part5(cls, mapping):
        """Add ISO 639-2 pt5 codes to mapping"""
        Iso6395 = namedtuple(
            "Iso6395", ["URI", "code", "Label_English", "Label_French"]
        )
        with open(cls._fps["pt5"], encoding="utf-8") as f:
            next(f)
            for line in f:
                row = line.rstrip().split("\t")
                iso6395 = Iso6395(*row)

                params = {
                    "pt1": "",
                    "pt2b": "",
                    "pt2t": "",
                    "pt3": "",
                    "pt5": iso6395.code,
                    "name": iso6395.Label_English,
                }
                if len(params["pt5"]) == 3:
                    for tag in TAGS:
                        if params[tag] and params[tag] not in mapping.get(
                            tag, {}
                        ):
                            mapping.setdefault(tag, {})[params[tag]] = {
                                k: v for k, v in params.items() if k != tag
                            }
                # map pt5 and pt2b
                if params["pt5"] in mapping["pt2b"]:
                    mapping["pt2b"][params["pt5"]]["pt5"] = params["pt5"]
                    mapping["pt5"][params["pt5"]]["pt2b"] = params["pt5"]

        return mapping

    @staticmethod
    def _sort_alphabetically(mapping):
        """Sort language codes and names alphabetically in the mapping"""
        sorted_data = {}
        for tag, d1 in mapping.items():
            sorted_data[tag] = {lg: d2 for lg, d2 in sorted(d1.items())}

        mapping = {k: v for k, v in sorted(sorted_data.items())}

        return mapping


class MacroMapping:
    """A mapping used to query the ISO 639 macrolanguages efficiently"""

    _fps = {
        k: resource_filename(__package__, FILENAMES[k])
        for k in ("macro", "mapping_macro")
    }

    def __init__(self):

        self._data = {}

    def load(self):
        """Load data from local JSON file"""
        try:
            with open(self._fps["mapping_macro"], encoding="utf-8") as f:
                self._data = json.load(f)
        except FileNotFoundError:
            mapping = self._build()
            self._data = self._sort_alphabetically(mapping)
            self.save()

        return self._data

    def save(self):
        """Save data into local JSON file"""
        with open(self._fps["mapping_macro"], "w", encoding="utf-8") as f:
            json.dump(self._data, f)

    @classmethod
    def _build(cls):

        MacroLanguage = namedtuple("Macro", ["M_Id", "I_Id", "I_Status"])
        mapping = {k: {} for k in ("macro", "individual")}
        with open(cls._fps["macro"], encoding="utf-8") as f:
            next(f)
            for line in f:
                row = line.rstrip().split("\t")
                macro = MacroLanguage(*row)

                mapping["macro"].setdefault(macro.M_Id, []).append(macro.I_Id)
                mapping["individual"][macro.I_Id] = macro.M_Id

        return mapping

    @staticmethod
    def _sort_alphabetically(mapping):

        mapping["individual"] = {
            k: v for k, v in sorted(mapping["individual"].items())
        }
        return mapping


class DeprecatedMapping:
    """A mapping used to query the deprecated ISO 639-3 efficiently"""

    _fps = {
        k: resource_filename(__package__, FILENAMES[k])
        for k in ("deprecated", "mapping_deprecated")
    }

    def __init__(self):

        self._data = {}

    def load(self):
        """Load data from local JSON file"""
        try:
            with open(self._fps["mapping_deprecated"], encoding="utf-8") as f:
                self._data = json.load(f)
        except FileNotFoundError:
            mapping = self._build()
            self._data = self._sort_alphabetically(mapping)
            self.save()

        return self._data

    def save(self):
        """Save data into local JSON file"""
        with open(self._fps["mapping_deprecated"], "w", encoding="utf-8") as f:
            json.dump(self._data, f)

    @classmethod
    def _build(cls):

        Retirement = namedtuple(
            "Retirement",
            [
                "Id",
                "Ref_Name",
                "Ret_Reason",
                "Change_To",
                "Ret_Remedy",
                "Effective",
            ],
        )

        with open(cls._fps["deprecated"], encoding="utf-8") as f:
            retirements = [
                Retirement(*line.rstrip().split("\t")) for line in f
            ]

        # make sure that deprecations are ordered chronologically
        sorted_retirements = sorted(retirements[1:], key=lambda x: x.Effective)

        mapping = {}
        for ret in sorted_retirements:
            # avoid infinite loops to self
            if ret.Change_To == ret.Id:
                continue
            # when a deprecation routes to an already deprecated
            # lang, the older one is canceled
            if ret.Change_To in mapping:
                del mapping[ret.Change_To]

            mapping[ret.Id] = {
                "ref_name": ret.Ref_Name,
                "ret_reason": ret.Ret_Reason,
                "change_to": ret.Change_To,
                "ret_remedy": ret.Ret_Remedy,
                "effective": ret.Effective,
            }

        return mapping

    @staticmethod
    def _sort_alphabetically(mapping):

        return {k: mapping[k] for k in sorted(mapping.keys())}
