import logging

from .database import Database
from .utils import download, get_data, scrape, serialize

logger = logging.getLogger(__name__)


def download_source_data_files() -> None:
    """Download all source data files from the websites of the
    ISO 639 registration authorities.
    """
    for file_name in (
        "ISO-639-2_utf-8.txt",
        "iso-639-3.tab",
        "iso-639-3_Retirements.tab",
        "iso-639-3-macrolanguages.tab",
        "iso-639-3_Name_Index.tab",
        "iso639-5.tsv",
    ):
        download(file_name)
    for file_name in ("ISO-639-2_code_changes.tsv", "iso639-5_changes.tsv"):
        scrape(file_name)


def generate_library_embedded_data_files() -> None:
    """Generate the mappings and lists that are embedded into the `iso639-lang`
    library from the local ISO 639 source data files.
    """
    with Database(":memory:") as db:
        # source data files are loaded into the database
        iso6392 = get_data("ISO-639-2_utf-8.txt")
        db.load_iso6392(iso6392)

        iso6392_changes = get_data("ISO-639-2_code_changes.tsv")
        db.load_iso6392_changes(iso6392_changes)

        iso6393 = get_data("iso-639-3.tab")
        db.load_iso6393(iso6393)

        iso6393_names = get_data("iso-639-3_Name_Index.tab")
        db.load_iso6393_names(iso6393_names)

        iso6393_macrolanguages = get_data("iso-639-3-macrolanguages.tab")
        db.load_iso6393_macrolanguages(iso6393_macrolanguages)

        iso6393_retirements = get_data("iso-639-3_Retirements.tab")
        db.load_iso6393_retirements(iso6393_retirements)

        iso6395 = get_data("iso639-5.tsv")
        db.load_iso6395(iso6395)

        iso6395_changes = get_data("iso639-5_changes.tsv")
        db.load_iso6395_changes(iso6395_changes)

        # export generated data files to the iso639-lang library
        mapping_core = db.get_mapping_core()
        serialize(mapping_core, "iso-639.json")

        mapping_depreated = db.get_mapping_deprecated()
        serialize(mapping_depreated, "iso-639_deprecated.json")

        mapping_macro = db.get_mapping_macro()
        serialize(mapping_macro, "iso-639_macro.json")

        mapping_ref_name = db.get_mapping_ref_name()
        serialize(mapping_ref_name, "iso-639_ref_name.json")

        mapping_other_names = db.get_mapping_other_names()
        serialize(mapping_other_names, "iso-639_other_names.json")

        mapping_scope = db.get_mapping_scope()
        serialize(mapping_scope, "iso-639_scope.json")

        mapping_type = db.get_mapping_type()
        serialize(mapping_type, "iso-639_type.json")

        list_langs = db.get_list_langs()
        serialize(list_langs, "iso-639_langs.json")
