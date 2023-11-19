import json
import pickle

try:
    from importlib.resources import files
    from importlib.abc import Traversable
except ImportError:
    # Compatibility for Python <3.9
    from importlib_resources import files
    from importlib_resources.abc import Traversable


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
    "list_langs": "data/iso-639_langs.pkl",
}


def get_file(file_alias: str) -> Traversable:
    """Get the path of a local data file"""
    return files(__package__).joinpath(FILENAMES[file_alias])


def load_mapping(file_alias: str) -> dict:
    """Load an ISO 639 mapping JSON file"""
    file_path = get_file(file_alias)
    try:
        with file_path.open(encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def load_langs() -> list:
    """Load the pickled list of ISO 639 Langs"""
    file_path = get_file("list_langs")
    try:
        with file_path.open("rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return []
