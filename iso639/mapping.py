import json

from pkg_resources import resource_filename

FILENAMES = {
    "core": "iso-639-3.tab",
    "pt2": "ISO-639-2_utf-8.txt",
    "pt5": "iso639-5.tsv",
    "macro": "iso-639-3-macrolanguages.tab",
    "mapping": "iso-639.json",
    "mapping_macro": "iso-639_macro.json",
    "deprecated": "iso-639-3_Retirements.tab",
    "mapping_deprecated": "iso-639_deprecated.json",
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
        mapping = {}
        with open(cls._fps["core"], encoding="utf-8") as f:
            next(f)
            for line in f:
                row = line.rstrip().split("\t")
                params = {
                    "pt1": row[3],
                    "pt2b": row[1],
                    "pt2t": row[2],
                    "pt3": row[0],
                    "pt5": "",
                    "name": row[6],
                }
                for tag in TAGS:
                    if params[tag]:
                        mapping.setdefault(tag, {})[params[tag]] = {
                            k: v for k, v in params.items() if k != tag
                        }

        return mapping

    @classmethod
    def _complete_part2(cls, mapping):
        """Complete mapping with pt2 codes not covered by pt3"""
        with open(cls._fps["pt2"], encoding="utf-8-sig") as f:
            for line in f:
                row = line.rstrip().split("|")
                params = {
                    "pt1": row[2],
                    "pt2b": row[0],
                    "pt2t": row[1],
                    "pt3": "",
                    "pt5": "",
                    "name": row[3],
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
        with open(cls._fps["pt5"], encoding="utf-8") as f:
            next(f)
            for line in f:
                row = line.rstrip().split("\t")
                params = {
                    "pt1": "",
                    "pt2b": "",
                    "pt2t": "",
                    "pt3": "",
                    "pt5": row[1],
                    "name": row[2],
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

        mapping = {k: {} for k in ("macro", "individual")}
        with open(cls._fps["macro"], encoding="utf-8") as f:
            next(f)
            for line in f:
                row = line.rstrip().split("\t")
                mapping["macro"].setdefault(row[0], []).append(row[1])
                mapping["individual"][row[1]] = row[0]

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

        mapping = {}
        with open(cls._fps["deprecated"], encoding="utf-8") as f:
            next(f)
            for line in f:
                row = line.rstrip().split("\t")
                mapping[row[0]] = {
                    k: row[i + 1]
                    for i, k in enumerate(
                        [
                            "ref_name",
                            "ret_reason",
                            "change_to",
                            "ret_remedy",
                            "effective",
                        ]
                    )
                }

        return mapping

    @staticmethod
    def _sort_alphabetically(mapping):

        return {k: mapping[k] for k in sorted(mapping.keys())}
