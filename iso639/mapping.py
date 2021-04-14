import json

from pkg_resources import resource_filename

CORE_TABLE_PATH = resource_filename(__package__, "iso-639-3.tab")
PART2_TABLE_PATH = resource_filename(__package__, "ISO-639-2_utf-8.txt")
PART5_TABLE_PATH = resource_filename(__package__, "iso639-5.tsv")
MAPPING_PATH = resource_filename(__package__, "iso-639.json")

TAGS = ("pt1", "pt2b", "pt2t", "pt3", "pt5", "name")


class ISO639Mapping:
    """A mapping used to query the ISO 639 values efficiently"""

    def __init__(self):

        self._data = {}

    def load(self):
        """Load data from local JSON file"""
        try:
            with open(MAPPING_PATH, encoding="utf-8") as f:
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
        with open(MAPPING_PATH, "w", encoding="utf-8") as f:
            json.dump(self._data, f)

    def build(self):
        """Build the JSON file from the official ISO 639 code tables
        stored locally
        """
        self._data = self._build_core_mapping()
        self._complete_part2()
        self._add_part5()
        self._sort_alphabetically()

    @staticmethod
    def _build_core_mapping():
        """Builds the core ISO-639 mapping from the ISO 639-3 tab file"""
        mapping = {}
        with open(CORE_TABLE_PATH, encoding="utf-8") as f:
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

    def _complete_part2(self):
        """Complete mapping with pt2 codes not covered by pt3"""
        with open(PART2_TABLE_PATH, encoding="utf-8-sig") as f:
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
                        if params[tag] and params[tag] not in self._data[tag]:
                            self._data.setdefault(tag, {})[params[tag]] = {
                                k: v for k, v in params.items() if k != tag
                            }

    def _add_part5(self):
        """Add ISO 639-2 pt5 codes to mapping"""
        with open(PART5_TABLE_PATH, encoding="utf-8") as f:
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
                        if params[tag] and params[tag] not in self._data.get(
                            tag, {}
                        ):
                            self._data.setdefault(tag, {})[params[tag]] = {
                                k: v for k, v in params.items() if k != tag
                            }
                # map pt5 and pt2b
                if params["pt5"] in self._data["pt2b"]:
                    self._data["pt2b"][params["pt5"]]["pt5"] = params["pt5"]
                    self._data["pt5"][params["pt5"]]["pt2b"] = params["pt5"]

    def _sort_alphabetically(self):
        """Sort language codes and names alphabetically in the mapping"""
        sorted_data = {}
        for tag, d1 in self._data.items():
            sorted_data[tag] = {lg: d2 for lg, d2 in sorted(d1.items())}

        self._data = {k: v for k, v in sorted(sorted_data.items())}
