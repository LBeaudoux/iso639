import json

from pkg_resources import resource_filename

FILENAMES = {
    "pt3": "data/iso-639-3.tab",
    "pt2": "data/ISO-639-2_utf-8.txt",
    "pt5": "data/iso639-5.tsv",
    "retirements": "data/iso-639-3_Retirements.tab",
    "macros": "data/iso-639-3-macrolanguages.tab",
    "mapping_data": "data/iso-639.json",
    "mapping_scope": "data/iso-639_scope.json",
    "mapping_type": "data/iso-639_type.json",
    "mapping_deprecated": "data/iso-639_deprecated.json",
    "mapping_macro": "data/iso-639_macro.json",
}


def get_file(file_alias: str) -> str:
    """Get the path of a local data file"""
    return resource_filename(__package__, FILENAMES[file_alias])


def load_mapping(file_alias):
    """Load a mapping JSON file"""
    with open(get_file(file_alias), encoding="utf-8") as f:
        return json.load(f)
