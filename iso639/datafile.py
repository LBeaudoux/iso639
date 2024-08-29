import json
from typing import Dict, List, Optional, Union

try:
    from importlib.resources import files
except ImportError:
    # Compatibility for Python <3.9
    from importlib_resources import files


FILENAMES = {
    "pt3": "data/iso-639-3.tab",
    "pt2": "data/ISO-639-2_utf-8.txt",
    "pt5": "data/iso639-5.tsv",
    "retirements": "data/iso-639-3_Retirements.tab",
    "macros": "data/iso-639-3-macrolanguages.tab",
    "names": "data/iso-639-3_Name_Index.tab",
    "mapping_data": "data/iso-639.json",
    "mapping_scope": "data/iso-639_scope.json",
    "mapping_type": "data/iso-639_type.json",
    "mapping_deprecated": "data/iso-639_deprecated.json",
    "mapping_macro": "data/iso-639_macro.json",
    "mapping_ref_name": "data/iso-639_ref_name.json",
    "mapping_other_names": "data/iso-639_other_names.json",
    "list_langs": "data/iso-639_langs.json",
}


def get_file(file_alias: str):
    """Get the path of a local data file"""
    return files(__package__).joinpath(FILENAMES[file_alias])


def load_file(file_alias: str) -> Optional[Union[Dict, List]]:
    """Load local JSON file"""
    file_path = get_file(file_alias)
    try:
        with file_path.open(encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return None
