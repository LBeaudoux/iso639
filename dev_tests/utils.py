import csv
import re

DOWNLOAD_DIR = "dev_iso639/downloads/"


def get_iso6392_rows():
    with open(DOWNLOAD_DIR + "ISO-639-2_utf-8.txt", encoding="utf-8-sig") as f:
        # qaa–qtz is a range reserved for local use in ISO 639-2
        rows = [r for r in csv.reader(f, delimiter="|") if "-" not in r[0]]
    return rows


def get_iso6393_rows():
    rows = []
    with open(DOWNLOAD_DIR + "iso-639-3.tab", encoding="utf-8") as f:
        next(f)
        for r in csv.reader(f, delimiter="\t"):
            if r[-1] == "Code element for 639-1 has been deprecated":
                r[3] = ""
            rows.append(r)
    return rows


def get_iso6393_names_rows():
    with open(
        DOWNLOAD_DIR + "iso-639-3_Name_Index.tab", encoding="utf-8"
    ) as f:
        next(f)
        rows = [r for r in csv.reader(f, delimiter="\t")]
    return rows


def get_iso6393_retirements_rows():
    with open(
        DOWNLOAD_DIR + "iso-639-3_Retirements.tab", encoding="utf-8"
    ) as f:
        next(f)
        rows = [r for r in csv.reader(f, delimiter="\t")]
    return rows


def get_iso6393_macrolanguages_rows():
    with open(
        DOWNLOAD_DIR + "iso-639-3-macrolanguages.tab", encoding="utf-8"
    ) as f:
        next(f)
        # only rows with 'A'ctive individual languages are useful
        rows = [r for r in csv.reader(f, delimiter="\t") if r[2] == "A"]
    return rows


def get_iso6395_rows():
    with open(DOWNLOAD_DIR + "iso639-5.tsv", encoding="utf-8") as f:
        next(f)
        rows = [r for r in csv.reader(f, delimiter="\t")]
    return rows


def get_valid_iso639_alpha3_ids():
    valid_ids = set()

    with open(DOWNLOAD_DIR + "iso-639-3.tab", encoding="utf-8") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            valid_ids.add(r["Id"])

    with open(DOWNLOAD_DIR + "iso639-5.tsv", encoding="utf-8") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            valid_ids.add(r["code"])

    with open(DOWNLOAD_DIR + "ISO-639-2_utf-8.txt", encoding="utf-8-sig") as f:
        for r in csv.reader(f, delimiter="|"):
            valid_ids.add(r[0])
            valid_ids.add(r[1])

    return valid_ids


def get_valid_iso639_names():
    valid_names = set()

    with open(DOWNLOAD_DIR + "iso-639-3.tab", encoding="utf-8") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            valid_names.add(r["Ref_Name"])

    with open(DOWNLOAD_DIR + "iso639-5.tsv", encoding="utf-8") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            valid_names.add(r["Label (English)"])

    with open(DOWNLOAD_DIR + "ISO-639-2_utf-8.txt", encoding="utf-8-sig") as f:
        for r in csv.reader(f, delimiter="|"):
            for name in r[3].split("; "):
                valid_names.add(name)

    with open(
        DOWNLOAD_DIR + "iso-639-3_Name_Index.tab", encoding="utf-8"
    ) as f:
        for _, print_name, inverted_neme in csv.reader(f, delimiter="\t"):
            valid_names.add(print_name)
            valid_names.add(inverted_neme)

    return valid_names


def get_iso6391_deprecated_ids_rows():
    rows = []
    with open(
        DOWNLOAD_DIR + "ISO-639-2_code_changes.tsv", encoding="utf-8"
    ) as f:
        next(f)
        for r in csv.reader(f, delimiter="\t"):
            m = re.search(r"^([a-z]{2})?\s?\[\-([a-z]{2})\]$", r[0])
            if m and r[6]:
                dep = m.group(2)
                change_to = m.group(1) if m.group(1) else ""
                name = r[2].split("; ")[0]
                rows.append([dep, change_to, name] + r[3:])
    return rows


def get_iso6391_deprecated_names_rows():
    valid_names = get_valid_iso639_names()
    rows = []
    with open(
        DOWNLOAD_DIR + "ISO-639-2_code_changes.tsv", encoding="utf-8"
    ) as f:
        next(f)
        for r in csv.reader(f, delimiter="\t"):
            m = re.search(r"^([a-z]{2})?\s?\[\-([a-z]{2})\]$", r[0])
            if m and r[6]:
                dep = m.group(2)
                change_to = m.group(1) if m.group(1) else ""
                name = r[2].split("; ")[0]
                if name not in valid_names:
                    rows.append([dep, change_to, name] + r[3:])
    return rows


def get_iso6392_deprecated_ids_rows():
    rows = []
    with open(
        DOWNLOAD_DIR + "ISO-639-2_code_changes.tsv", encoding="utf-8"
    ) as f:
        next(f)
        for r in csv.reader(f, delimiter="\t"):
            m = re.search(r"^([a-z]{3})?\s?\[\-([a-z]{3})\]$", r[1])
            if m and r[6] and r[4] < "2007-02-01":
                dep = m.group(2)
                change_to = m.group(1) if m.group(1) else ""
                name = r[2].split("; ")[0]
                rows.append([dep, change_to, name] + r[3:])
    return rows


def get_iso6392_deprecated_names_rows():
    valid_names = get_valid_iso639_names()
    rows = []
    with open(
        DOWNLOAD_DIR + "ISO-639-2_code_changes.tsv", encoding="utf-8"
    ) as f:
        next(f)
        for r in csv.reader(f, delimiter="\t"):
            m = re.search(r"^([a-z]{3})?\s?\[\-([a-z]{3})\]$", r[1])
            if m and r[6] and r[4] < "2007-02-01":
                dep = m.group(2)
                change_to = m.group(1) if m.group(1) else ""
                name = r[2].split("; ")[0]
                if name not in valid_names:
                    rows.append([dep, change_to, name] + r[3:])
    return rows


def get_iso6393_deprecated_ids_rows():
    valid_ids = get_valid_iso639_alpha3_ids()
    with open(
        DOWNLOAD_DIR + "iso-639-3_Retirements.tab", encoding="utf-8"
    ) as f:
        next(f)
        rows = [
            r
            for r in csv.reader(f, delimiter="\t")
            if r[0] not in valid_ids and r[-1] >= "2007-02-01"
        ]

    return rows


def get_iso6393_deprecated_names_rows():
    valid_names = get_valid_iso639_names()
    with open(
        DOWNLOAD_DIR + "iso-639-3_Retirements.tab", encoding="utf-8"
    ) as f:
        next(f)
        rows = [
            r
            for r in csv.reader(f, delimiter="\t")
            if r[1] not in valid_names and r[-1] >= "2007-02-01"
        ]

    return rows
