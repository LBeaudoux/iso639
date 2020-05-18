import csv
import json

from pkg_resources import resource_filename

TABLE_PATH = resource_filename(__package__, "iso-639-3.tab")
MAPPING_PATH = resource_filename(__package__, "iso-639-3.json")


def load_iso639_mapping():
    """Load the ISO-639 mapping from its JSON file.
    """
    try:
        with open(MAPPING_PATH) as f:
            mapping = json.load(f)
    except FileNotFoundError:
        table = _load_iso639_table()
        mapping = _map_iso639_table(table)
        _save_iso639_mapping(mapping)
    finally:
        return mapping


def _load_iso639_table():
    """Load the iso639 table from its tab file.
    """
    with open(TABLE_PATH) as f:
        reader = csv.reader(f, delimiter="\t")
        next(reader)

        return [row for row in reader]


def _map_iso639_table(table):
    """Turn the ISO-639 table into a dict for mapping iso639 values faster.
    """
    mapping = {k: {} for k in ("pt1", "pt3", "name")}
    for row in table:
        # ISO 639 part 1 codes (2 characters)
        if row[3]:
            mapping["pt1"][row[3]] = {"pt3": row[0], "name": row[6]}
        # ISO 639 part 3 codes (3 characters)
        if row[0]:
            mapping["pt3"][row[0]] = {"pt1": row[3], "name": row[6]}
        # ISO 639 names (capitalized string)
        if row[6]:
            mapping["name"][row[6]] = {"pt1": row[3], "pt3": row[0]}

    return mapping


def _save_iso639_mapping(mapping):
    """Save the ISO-639 mapping into a JSON file.
    """
    with open(MAPPING_PATH, "w") as f:
        json.dump(mapping, f)
