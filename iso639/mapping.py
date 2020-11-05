import csv
import json

from pkg_resources import resource_filename

TABLE_PATH = resource_filename(__package__, "iso-639-3.tab")
MAPPING_PATH = resource_filename(__package__, "iso-639-3.json")


def load_iso639_mapping():
    """Loads the ISO-639 mapping from its JSON file"""
    try:
        with open(MAPPING_PATH, encoding="utf-8") as f:
            mapping = json.load(f)
    except FileNotFoundError:
        mapping = _build_iso639_mapping()
        with open(MAPPING_PATH, "w", encoding="utf-8") as f:
            json.dump(mapping, f)
    else:
        # remap if the mapping is incomplete
        if any(
            k not in mapping.keys()
            for k in ("pt1", "pt2B", "pt2T", "pt3", "name")
        ):
            mapping = _build_iso639_mapping()
            with open(MAPPING_PATH, "w", encoding="utf-8") as f:
                json.dump(mapping, f)

    return mapping


def _build_iso639_mapping():
    """Builds the ISO-639 mapping from its tab file"""
    mapping = {k: {} for k in ("pt1", "pt2B", "pt2T", "pt3", "name")}
    with open(TABLE_PATH, encoding="utf-8") as f:
        reader = csv.reader(f, delimiter="\t")
        next(reader)
        for row in reader:
            # ISO 639-1 codes (2 characters)
            if row[3]:
                mapping["pt1"][row[3]] = {
                    "pt2B": row[1],
                    "pt2T": row[2],
                    "pt3": row[0],
                    "name": row[6],
                }
            # ISO 639-2B codes (3 characters)
            if row[1]:
                mapping["pt2B"][row[1]] = {
                    "pt1": row[3],
                    "pt2T": row[2],
                    "pt3": row[0],
                    "name": row[6],
                }
            # ISO 639-2T codes (3 characters)
            if row[2]:
                mapping["pt2T"][row[2]] = {
                    "pt1": row[3],
                    "pt2B": row[1],
                    "pt3": row[0],
                    "name": row[6],
                }
            # ISO 639-3 codes (3 characters)
            if row[0]:
                mapping["pt3"][row[0]] = {
                    "pt1": row[3],
                    "pt2B": row[1],
                    "pt2T": row[2],
                    "name": row[6],
                }
            # ISO 639 names (capitalized string)
            if row[6]:
                mapping["name"][row[6]] = {
                    "pt1": row[3],
                    "pt2B": row[1],
                    "pt2T": row[2],
                    "pt3": row[0],
                }

    return mapping
