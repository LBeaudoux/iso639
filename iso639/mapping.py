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
    "mapping_scope": "data/iso-639_scope.json",
    "mapping_type": "data/iso-639_type.json",
    "mapping_macro": "data/iso-639_macro.json",
    "mapping_deprecated": "data/iso-639_deprecated.json",
}
TAGS = ("pt1", "pt2b", "pt2t", "pt3", "pt5", "name")


def get_file_path(file_alias):
    """Get the path of a local data file"""
    return resource_filename(__package__, FILENAMES[file_alias])


def read_core():
    """Generates core ISO 639 data from its source file"""
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
    with open(get_file_path("core"), encoding="utf-8") as f:
        next(f)
        for line in f:
            row = line.rstrip().split("\t")
            yield Iso6393(*row[:7])


def read_pt2():
    """Generates ISO 639-2 data from its source file"""
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
    with open(get_file_path("pt2"), encoding="utf-8-sig") as f:
        for line in f:
            row = line.rstrip().split("|")
            yield Iso6392(*row)


def read_pt5():
    """Generates ISO 639-5 data from its source file"""
    Iso6395 = namedtuple(
        "Iso6395", ["URI", "code", "Label_English", "Label_French"]
    )
    with open(get_file_path("pt5"), encoding="utf-8") as f:
        next(f)
        for line in f:
            row = line.rstrip().split("\t")
            yield Iso6395(*row)


def read_macro():
    """Generates ISO 639 macrolanguage data from its source file"""
    MacroLanguage = namedtuple("Macro", ["M_Id", "I_Id", "I_Status"])
    with open(get_file_path("macro"), encoding="utf-8") as f:
        next(f)
        for line in f:
            row = line.rstrip().split("\t")
            yield MacroLanguage(*row)


def read_deprecated():
    """Generates ISO 639-3 deprecated language data from its source
    file
    """
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
    with open(get_file_path("deprecated"), encoding="utf-8") as f:
        next(f)
        for line in f:
            row = line.rstrip().split("\t")
            yield Retirement(*row)


class Mapping(object):
    """A base class for handling data mappings stored locally as
    JSON files
    """

    _file_path = ""

    def __init__(self):
        self._data = {}

    def load(self):
        try:
            with open(self._file_path, encoding="utf-8") as f:
                self._data = json.load(f)
        except FileNotFoundError:
            self._data = self.build()
            with open(self._file_path, "w", encoding="utf-8") as f:
                json.dump(self._data, f)

        return self._data

    def build(self):
        mapping = self._build()
        mapping = self._sort_alphabetically(mapping)

        return mapping

    @staticmethod
    def _sort_alphabetically(mapping):
        return {k: mapping[k] for k in sorted(mapping.keys())}


class ISO639Mapping(Mapping):
    """A mapping used to efficiently query the ISO 639 values
    in-memory
    """

    _file_path = get_file_path("mapping")

    def build(self):
        """Build the JSON file from the official ISO 639 code tables
        stored locally
        """
        mapping = self._build_core_mapping()
        mapping = self._complete_part2(mapping)
        mapping = self._add_part5(mapping)
        mapping = self._sort_alphabetically(mapping)

        return mapping

    @staticmethod
    def _build_core_mapping():
        # the ISO 639-3 code table is used to build the core of
        # the mapping
        mapping = {}
        for iso6393 in read_core():
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

    @staticmethod
    def _complete_part2(mapping):
        # complete core mapping with ISO 639-2 codes not covered by
        # ISO 639-3
        for iso6392 in read_pt2():
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

    @staticmethod
    def _add_part5(mapping):
        # complete core mapping with ISO 639-5 codes
        for iso6395 in read_pt5():
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
                    if params[tag] and params[tag] not in mapping.get(tag, {}):
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
        sorted_data = {}
        for tag, d1 in mapping.items():
            sorted_data[tag] = {lg: d2 for lg, d2 in sorted(d1.items())}

        mapping = {k: v for k, v in sorted(sorted_data.items())}

        return mapping


class ScopeMapping(Mapping):
    """A mapping used to efficiently query the ISO 639-3
    languages' scopes in-memory
    """

    _file_path = get_file_path("mapping_scope")

    @staticmethod
    def _build():
        return {iso6393.Id: iso6393.Scope for iso6393 in read_core()}


class TypeMapping(Mapping):
    """A mapping used to efficiently query the ISO 639-3
    languages' types in-memory
    """

    _file_path = get_file_path("mapping_type")

    @staticmethod
    def _build():
        return {iso6393.Id: iso6393.Language_Type for iso6393 in read_core()}


class MacroMapping(Mapping):
    """A mapping used to efficiently query the ISO 639-3
    macrolanguages values in-memory
    """

    _file_path = get_file_path("mapping_macro")

    def build(self):
        """Build the mapping for the ISO 639-3 macrolanguages"""
        mapping = self._build()
        mapping = self._sort_alphabetically(mapping)

        return mapping

    @staticmethod
    def _build():
        mapping = {}
        for macro in read_macro():
            mapping.setdefault("macro", {}).setdefault(macro.M_Id, []).append(
                macro.I_Id
            )
            mapping.setdefault("individual", {})[macro.I_Id] = macro.M_Id

        return mapping

    @staticmethod
    def _sort_alphabetically(mapping):
        mapping["individual"] = {
            k: v for k, v in sorted(mapping["individual"].items())
        }
        return mapping


class DeprecatedMapping(Mapping):
    """A mapping used to efficiently query the ISO 639-3
    deprecated languages in-memory
    """

    _file_path = get_file_path("mapping_deprecated")

    def build(self):
        mapping = self._build()
        mapping = self._sort_alphabetically(mapping)

        return mapping

    @staticmethod
    def _build():
        retirements = [ret for ret in read_deprecated()]
        # make sure that deprecations are ordered chronologically
        sorted_retirements = sorted(retirements, key=lambda x: x.Effective)

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
