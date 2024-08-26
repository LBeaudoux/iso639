import json
import pickle
import sqlite3
from collections import defaultdict, namedtuple
from typing import Generator

from iso639.datafile import get_file
from iso639.iso639 import Lang

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


def read_iso6392(datafile: str) -> Generator[Iso6392, None, None]:
    """Read ISO 639-2 data from its source file"""
    with open(datafile, encoding="utf-8-sig") as f:
        for line in f:
            row = line.rstrip().split("|")
            yield Iso6392(*row)


def load_iso6392(datafile: str, db: sqlite3.Connection):
    """Load ISO 639-2 data into a database table"""
    with db:
        db.execute("DROP TABLE IF EXISTS iso6392")
        db.execute(
            """
            CREATE TABLE iso6392 (
                pt2b CHAR(3) PRIMARY KEY,
                name TEXT NOT NULL,
                pt2t CHAR(3) NULL,
                pt1 CHAR(2) NULL
            )
            """
        )
        for iso6392 in read_iso6392(datafile):
            db.execute(
                "INSERT INTO iso6392 VALUES (?, ?, ?, ?)",
                (
                    iso6392.alpha3_bibliographic,
                    iso6392.English_name,
                    iso6392.alpha3_terminologic,
                    iso6392.alpha2,
                ),
            )


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


def read_iso6393(datafile: str) -> Generator[Iso6393, None, None]:
    """Read ISO 639-3 data from its source file"""
    with open(datafile, encoding="utf-8") as f:
        next(f)
        for line in f:
            row = line.rstrip().split("\t")
            yield Iso6393(*row[:7])


def load_iso6393(datafile: str, db: sqlite3.Connection):
    """Load ISO 639-3 data into a database table"""
    with db:
        db.execute(
            """
            CREATE TEMPORARY TABLE iso6393 (
                pt3 CHAR(3) PRIMARY KEY,
                name TEXT NOT NULL,
                pt1 CHAR(2) NULL,  
                pt2b CHAR(3) NULL,
                pt2t CHAR(3) NULL,
                scope CHAR(1) NOT NULL,
                type CHAR(1) NOT NULL
            )
            """
        )
        for iso6393 in read_iso6393(datafile):
            db.execute(
                "INSERT INTO iso6393 VALUES (?, ?, ?, ?, ?, ?, ?)",
                (
                    iso6393.Id,
                    iso6393.Ref_Name,
                    iso6393.Part1,
                    iso6393.Part2B,
                    iso6393.Part2T,
                    iso6393.Scope,
                    iso6393.Language_Type,
                ),
            )


Iso6395 = namedtuple(
    "Iso6395", ["URI", "code", "Label_English", "Label_French"]
)


def read_iso6395(datafile: str) -> Generator[Iso6395, None, None]:
    """Read ISO 639-5 data from its source file"""
    with open(datafile, encoding="utf-8") as f:
        next(f)
        for line in f:
            row = line.rstrip().split("\t")
            yield Iso6395(*row)


def load_iso6395(datafile: str, db: sqlite3.Connection):
    """Load ISO 639-5 data into a database table"""
    with db:
        db.execute(
            """
            CREATE TEMPORARY TABLE iso6395 (
                pt5 CHAR(3) PRIMARY KEY,
                name TEXT NOT NULL
            )
            """
        )
        for iso6395 in read_iso6395(datafile):
            db.execute(
                "INSERT INTO iso6395 (pt5, name) VALUES (?, ?)",
                (iso6395.code, iso6395.Label_English),
            )


def build_iso639(db: sqlite3.Connection):
    """Merge ISO 639-1, ISO 639-2, ISO 639-3 and ISO 639-5
    data into a single table
    """
    with db:
        db.execute("DROP TABLE IF EXISTS iso639")
        db.execute(
            """
            CREATE TABLE iso639 (
                name TEXT PRIMARY KEY,
                pt1 CHAR(2) NULL,  
                pt2b CHAR(3) NULL,
                pt2t CHAR(3) NULL,
                pt3 CHAR(3) NULL,
                pt5 CHAR(3) NULL,
                scope CHAR(1) NULL,
                type CHAR(1) NULL
            )
            """
        )
        db.execute(
            """
            INSERT INTO iso639 
            SELECT 
                iso6393.name, 
                iso6393.pt1, 
                iso6393.pt2b, 
                iso6393.pt2t, 
                iso6393.pt3, 
                '',
                iso6393.scope, 
                iso6393.type
            FROM iso6393 
            """
        )
        db.execute(
            """
            INSERT INTO iso639 
            SELECT 
                iso6395.name, 
                IFNULL(iso6392.pt1, ''), 
                IFNULL(iso6392.pt2b, ''), 
                IFNULL(iso6392.pt2t, ''), 
                '',
                iso6395.pt5,
                '',
                ''
            FROM iso6395
            LEFT JOIN iso6392
            ON iso6395.pt5 = iso6392.pt2b
            """
        )
        for pt in ("name", "pt1", "pt2b", "pt2t", "pt3", "pt5"):
            db.execute(
                "CREATE INDEX idx_iso639_{0} ON iso639 ({0})".format(pt)
            )


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


def read_retirement(datafile: str) -> Generator[Retirement, None, None]:
    """Read ISO 639-3 retirement data from its source file"""
    with open(datafile, encoding="utf-8") as f:
        next(f)
        for line in f:
            row = line.rstrip().split("\t")
            yield Retirement(*row)


def load_retirements(datafile: str, db: sqlite3.Connection):
    """Load retirements into a database table"""
    with db:
        db.execute(
            """
            CREATE TEMPORARY TABLE temp_retirements (
                pt3 CHAR(3) PRIMARY KEY,
                name VARCHAR(150) NOT NULL,
                reason CHAR(1) NOT NULL,
                change_to CHAR(3) NULL,
                ret_remedy VARCHAR(300) NULL,
                effective DATE NOT NULL
            )
            """
        )
        for ret in read_retirement(datafile):
            db.execute(
                "INSERT INTO temp_retirements VALUES (?, ?, ?, ?, ?, ?)",
                (
                    ret.Id,
                    ret.Ref_Name,
                    ret.Ret_Reason,
                    ret.Change_To,
                    ret.Ret_Remedy,
                    ret.Effective,
                ),
            )


def filter_retirements(db: sqlite3.Connection):
    """Discard infinite retirement loops"""
    with db:
        db.execute("DROP TABLE IF EXISTS retirements")
        db.execute(
            """
            CREATE TABLE retirements (
                pt3 CHAR(3) PRIMARY KEY,
                name VARCHAR(150) NOT NULL,
                reason CHAR(1) NOT NULL,
                change_to CHAR(3) NULL,
                ret_remedy VARCHAR(300) NULL,
                effective DATE NOT NULL
            )
            """
        )
        db.execute(
            """ 
            INSERT INTO retirements
            SELECT 
                rt1.pt3,
                rt1.name,
                rt1.reason,
                rt1.change_to,
                rt1.ret_remedy,
                rt1.effective
            FROM temp_retirements as rt1
            LEFT JOIN temp_retirements as rt2
            ON rt1.change_to = rt2.pt3
            WHERE rt2.change_to IS NULL
                OR (
                    rt1.pt3 != rt1.change_to  
                    AND rt1.effective > rt2.effective
                )
            """
        )
        db.execute(
            """
            CREATE INDEX idx_retirements_effective
            ON retirements (effective)
            """
        )


MacroLanguage = namedtuple("Macro", ["M_Id", "I_Id", "I_Status"])


def read_macro(datafile: str) -> Generator[MacroLanguage, None, None]:
    """Read ISO 639-3 macrolanguage data from its source file"""
    with open(datafile, encoding="utf-8") as f:
        next(f)
        for line in f:
            row = line.rstrip().split("\t")
            yield MacroLanguage(*row)


def load_macros(datafile: str, db: sqlite3.Connection):
    """Load ISO 639-3 macrolanguage data into a database table"""
    with db:
        db.execute("DROP TABLE IF EXISTS macros")
        db.execute(
            """
            CREATE TEMPORARY TABLE temp_macros (
                macro CHAR(3) NOT NULL,
                individual CHAR(3) NOT NULL,
                individual_status CHAR(1) NOT NULL
            )
            """
        )
        for macro in read_macro(datafile):
            db.execute(
                "INSERT INTO temp_macros VALUES (?, ?, ?)",
                (macro.M_Id, macro.I_Id, macro.I_Status),
            )
        db.execute(
            """
            CREATE TABLE macros (
                macro CHAR(3) NOT NULL,
                individual CHAR(3) NOT NULL
            )
            """
        )
        # route deprecated individual languages
        db.execute(
            """ 
            INSERT INTO macros
            SELECT DISTINCT
                CASE 
                    WHEN r1.change_to IS NULL OR r1.change_to = '' 
                        THEN m.macro
                    ELSE r1.change_to
                END AS macro,
                CASE 
                    WHEN r2.change_to IS NULL OR r2.change_to = '' 
                        THEN m.individual
                    ELSE r2.change_to
                END AS individual
            FROM temp_macros AS m
            LEFT JOIN retirements r1
                ON m.macro = r1.pt3
            LEFT JOIN retirements r2
                ON m.individual = r2.pt3
            """
        )
        db.execute(
            """
            CREATE INDEX idx_macros_macro_individual 
            ON macros (macro, individual)
            """
        )
        db.execute(
            """
            CREATE INDEX idx_macro_individual 
            ON macros (individual)
            """
        )


Name = namedtuple("Name", ["Id", "Print_Name", "Inverted_Name"])


def read_name(datafile: str) -> Generator[Name, None, None]:
    """Read ISO 639-3 name data from its source file"""
    with open(datafile, encoding="utf-8") as f:
        next(f)
        for line in f:
            row = line.rstrip().split("\t")
            yield Name(*row)


def load_names(datafile: str, db: sqlite3.Connection):
    """Load ISO 639-3 name data into a database table"""
    with db:
        db.execute("DROP TABLE IF EXISTS names")
        db.execute(
            """
            CREATE TABLE names (
                pt3 CHAR(3) NOT NULL,
                print_name TEXT NOT NULL,
                inverted_name TEXT NOT NULL
            )
            """
        )
        for name in read_name(datafile):
            db.execute(
                "INSERT INTO names VALUES (?, ?, ?)",
                (name.Id, name.Print_Name, name.Inverted_Name),
            )


def serialize_iso639(db: sqlite3.Connection, datafile: str):
    with db:
        mapping = {}
        for tag in ("name", "pt1", "pt2b", "pt2t", "pt3", "pt5"):
            sql = """
                  SELECT name, pt1, pt2b, pt2t, pt3, pt5 
                  FROM iso639
                  WHERE {0} != ''
                  ORDER BY {0}
                  """.format(
                tag
            )
            for row in db.execute(sql):
                dict_row = dict(row)
                dict_row.pop(tag)
                mapping.setdefault(tag, {})[row[tag]] = dict_row

    with open(datafile, "w", encoding="utf-8") as f:
        json.dump(mapping, f)


def serialize_scope(db: sqlite3.Connection, datafile: str):
    with db:
        sql = "SELECT pt3, scope FROM iso639 WHERE pt3 != '' ORDER BY pt3"
        mapping = {row[0]: row[1] for row in db.execute(sql)}
    with open(datafile, "w", encoding="utf-8") as f:
        json.dump(mapping, f)


def serialize_type(db: sqlite3.Connection, datafile: str):
    with db:
        sql = "SELECT pt3, type FROM iso639 WHERE pt3 != '' ORDER BY pt3"
        mapping = {row[0]: row[1] for row in db.execute(sql)}
    with open(datafile, "w", encoding="utf-8") as f:
        json.dump(mapping, f)


def serialize_deprecated(db: sqlite3.Connection, datafile: str):
    with db:
        mapping = {}
        sql = "SELECT * FROM retirements ORDER BY pt3, effective"
        for row in db.execute(sql):
            dict_row = dict(row)
            dict_row.pop("pt3")
            mapping[row["pt3"]] = dict_row
    with open(datafile, "w", encoding="utf-8") as f:
        json.dump(mapping, f)


def serialize_macro(db: sqlite3.Connection, datafile: str):
    with db:
        mapping = {}
        sql = "SELECT macro, individual FROM macros"
        for macro, individual in db.execute(sql):
            mapping.setdefault("macro", {}).setdefault(macro, []).append(
                individual
            )
            mapping.setdefault("individual", {})[individual] = macro
    with open(datafile, "w", encoding="utf-8") as f:
        json.dump(mapping, f)


def serialize_ref_name(db: sqlite3.Connection, datafile: str):
    with db:
        sql = """
                SELECT 
                    names.print_name AS other_name,
                    iso639.name AS ref_name
                FROM names
                INNER JOIN iso639 ON names.pt3 = iso639.pt3
                    WHERE other_name != ref_name
                UNION
                SELECT 
                    names.inverted_name AS other_name,
                    iso639.name AS ref_name
                FROM names
                INNER JOIN iso639 ON names.pt3 = iso639.pt3
                    WHERE other_name != ref_name
                UNION
                SELECT 
                    iso6392.name AS other_name,
                    iso639.name AS ref_name
                FROM iso6392
                INNER JOIN iso639 ON iso6392.pt2B = iso639.pt2B
                    WHERE other_name != ref_name
                ORDER BY ref_name
                """
        ref_names = defaultdict(set)
        for joined_names, ref_name in db.execute(sql):
            for other_name in joined_names.split("; "):
                if other_name != ref_name:
                    ref_names[other_name].add(ref_name)

    mapping = {
        other_name: v.pop()
        for other_name, v in sorted(ref_names.items())
        if len(v) == 1
    }
    assert len(ref_names) == len(mapping)

    with open(datafile, "w", encoding="utf-8") as f:
        json.dump(mapping, f)


def serialize_other_names(db: sqlite3.Connection, datafile: str):
    with db:
        sql = """
                WITH other_names AS (
                    SELECT 
                        iso639.name AS ref_name,
                        names.print_name AS other_name
                    FROM names
                    INNER JOIN iso639 ON names.pt3 = iso639.pt3
                        WHERE other_name != ref_name
                    UNION
                    SELECT 
                        iso639.name AS ref_name,
                        names.inverted_name AS other_name
                    FROM names
                    INNER JOIN iso639 ON names.pt3 = iso639.pt3
                        WHERE other_name != ref_name
                    UNION
                    SELECT 
                        iso639.name AS ref_name,
                        iso6392.name AS other_name
                    FROM iso6392
                    INNER JOIN iso639 ON iso6392.pt2B = iso639.pt2B
                        WHERE other_name != ref_name
                )
                SELECT ref_name, group_concat(other_name, "; ")
                FROM other_names
                GROUP BY ref_name
                ORDER BY ref_name ASC
                """
        other_names = defaultdict(set)
        for ref_name, joined_names in db.execute(sql):
            for other_name in joined_names.split("; "):
                if other_name != ref_name:
                    other_names[ref_name].add(other_name)

    mapping = {
        ref_name: sorted(list(other_names))
        for ref_name, other_names in other_names.items()
    }

    with open(datafile, "w", encoding="utf-8") as f:
        json.dump(mapping, f)


def serialize_langs(db: sqlite3.Connection, datafile: str):
    Lang._reset()
    with db:
        sql = """
                SELECT iso639.name
                FROM iso639
                LEFT JOIN retirements
                    ON iso639.pt3 = retirements.pt3
                WHERE retirements.pt3 IS NULL
                ORDER BY iso639.name
                """
        all_langs = []
        for (name,) in db.execute(sql):
            all_langs.append(Lang(name))

    with open(datafile, "wb") as f:
        pickle.dump(all_langs, f)


if __name__ == "__main__":

    con = sqlite3.connect(":memory:")
    con.row_factory = sqlite3.Row

    # load source files and transform tables
    pt3_path = get_file("pt3")
    load_iso6393(pt3_path, con)
    pt5_path = get_file("pt5")
    load_iso6395(pt5_path, con)
    pt2_path = get_file("pt2")
    load_iso6392(pt2_path, con)
    build_iso639(con)
    retirements_path = get_file("retirements")
    load_retirements(retirements_path, con)
    filter_retirements(con)
    macros_path = get_file("macros")
    load_macros(macros_path, con)
    names_path = get_file("names")
    load_names(names_path, con)

    # export mapping results as JSON files
    mapping_data_path = get_file("mapping_data")
    serialize_iso639(con, mapping_data_path)
    mapping_scope_path = get_file("mapping_scope")
    serialize_scope(con, mapping_scope_path)
    mapping_type_path = get_file("mapping_type")
    serialize_type(con, mapping_type_path)
    mapping_deprecated_path = get_file("mapping_deprecated")
    serialize_deprecated(con, mapping_deprecated_path)
    mapping_macro_path = get_file("mapping_macro")
    serialize_macro(con, mapping_macro_path)
    mapping_ref_name_path = get_file("mapping_ref_name")
    serialize_ref_name(con, mapping_ref_name_path)
    mapping_other_names_path = get_file("mapping_other_names")
    serialize_other_names(con, mapping_other_names_path)

    # pickle the list of all possible Lang instances
    langs_path = get_file("list_langs")
    serialize_langs(con, langs_path)

    con.close()
