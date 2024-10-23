import sqlite3
from collections import defaultdict
from typing import Any, Dict, List

import pandas as pd


class Database:
    """An SQLite database to manage ISO 63 data."""

    def __init__(self, database: str):
        self._db = database

    def __enter__(self):
        self._con = sqlite3.connect(self._db)
        self._con.row_factory = sqlite3.Row  # return result rows as dicts
        return self

    def __exit__(self, exception_type, exception_val, trace):
        self._con.close()

    def load_iso6392(self, data: pd.DataFrame) -> None:
        with self._con:
            self._con.execute("DROP TABLE IF EXISTS ISO_639_2")
            self._con.execute(
                """
                CREATE TABLE ISO_639_2 (
                    Part2b CHAR(3) PRIMARY KEY,
                    Part2t CHAR(3) NULL,
                    Part1 CHAR(2) NULL,
                    English_Name TEXT NOT NULL,
                    French_Name TEXT NOT NULL
                )
                """
            )
            data.to_sql("ISO_639_2", self._con, if_exists="append")

    def load_iso6392_changes(self, data: pd.DataFrame) -> None:
        with self._con:
            self._con.execute("DROP TABLE IF EXISTS ISO_639_2_Changes")
            self._con.execute(
                """
                CREATE TABLE ISO_639_2_Changes (
                    Part1 TEXT,
                    Part2 TEXT,
                    English_Name TEXT NOT NULL,
                    French_Name TEXT NOT NULL,
                    Date_Added_Or_Changed DATE,
                    Category_Of_Change CHAR(3),
                    Notes TEXT
                )
                """
            )
            data.to_sql("ISO_639_2_Changes", self._con, if_exists="append")

    def load_iso6393(self, data: pd.DataFrame) -> None:
        with self._con:
            self._con.execute("DROP TABLE IF EXISTS ISO_639_3")
            self._con.execute(
                """
                    CREATE TABLE ISO_639_3 (
                        Id CHAR(3) PRIMARY KEY,
                        Part2B CHAR(3) NULL,
                        Part2T CHAR(3) NULL,
                        Part1 CHAR(2) NULL,
                        Scope CHAR(1) NOT NULL,
                        Type CHAR(1) NOT NULL,
                        Ref_Name VARCHAR(150) NOT NULL,
                        Comment VARCHAR(150) NULL
                    )
                    """
            )
            data.to_sql("ISO_639_3", self._con, if_exists="append")

    def load_iso6393_names(self, data: pd.DataFrame) -> None:
        with self._con:
            self._con.execute("DROP TABLE IF EXISTS ISO_639_3_Names")
            self._con.execute(
                """
                CREATE TABLE ISO_639_3_Names (
                    Id CHAR(3) NOT NULL,
                    Print_Name VARCHAR(75) NOT NULL,
                    Inverted_Name VARCHAR(75) NOT NULL
                )
                """
            )
            data.to_sql("ISO_639_3_Names", self._con, if_exists="append")

    def load_iso6393_macrolanguages(self, data: pd.DataFrame) -> None:
        with self._con:
            self._con.execute("DROP TABLE IF EXISTS ISO_639_3_Macrolanguages")
            self._con.execute(
                """
                    CREATE TABLE ISO_639_3_Macrolanguages (
                        M_Id CHAR(3) NOT NULL,
                        I_Id CHAR(3) NOT NULL,
                        I_Status CHAR(1) NOT NULL
                    )
                    """
            )
            data.to_sql(
                "ISO_639_3_Macrolanguages", self._con, if_exists="append"
            )

    def load_iso6393_retirements(self, data: pd.DataFrame) -> None:
        with self._con:
            self._con.execute("DROP TABLE IF EXISTS ISO_639_3_Retirements")
            self._con.execute(
                """
                    CREATE TABLE ISO_639_3_Retirements (
                        Id CHAR(3) PRIMARY KEY,
                        Ref_Name VARCHAR(150) NOT NULL,
                        Ret_Reason CHAR(1) NOT NULL,
                        Change_To CHAR(3) NULL,
                        Ret_Remedy VARCHAR(300) NULL,
                        Effective DATE NOT NULL
                    )
                    """
            )
            data.to_sql("ISO_639_3_Retirements", self._con, if_exists="append")

    def load_iso6395(self, data: pd.DataFrame) -> None:
        with self._con:
            self._con.execute("DROP TABLE IF EXISTS ISO_639_5")
            self._con.execute(
                """
                    CREATE TABLE ISO_639_5 (
                        Uri TEXT NOT NULL,
                        Code CHAR(3) PRIMARY KEY,
                        Label_English TEXT NOT NULL,
                        Label_French TEXT NOT NULL
                    )
                    """
            )
            data.to_sql("ISO_639_5", self._con, if_exists="append")

    def load_iso6395_changes(self, data: pd.DataFrame) -> None:
        with self._con:
            self._con.execute("DROP TABLE IF EXISTS ISO_639_5_Changes")
            self._con.execute(
                """
                CREATE TABLE ISO_639_5_Changes (
                    Date DATE,
                    Code TEXT,
                    Reason TEXT
                )
                """
            )
            data.to_sql("ISO_639_5_Changes", self._con, if_exists="append")

    def get_mapping_core(self) -> Dict[str, Dict[str, Dict[str, str]]]:
        mapping: Dict[str, Dict[str, Dict[str, str]]] = {}
        with self._con:
            for tag in ("name", "pt1", "pt2b", "pt2t", "pt3", "pt5"):
                sql = """
                    WITH ISO_639 AS (
                        SELECT
                            ISO_639_3.Ref_Name AS name, 
                            CASE 
                                WHEN Dep.Part1 NOT NULL THEN Dep.Change_To
                                ELSE IFNULL(ISO_639_3.Part1, "")
                            END AS pt1, 
                            IFNULL(ISO_639_3.Part2b, "") AS pt2b, 
                            IFNULL(ISO_639_3.Part2t, "") AS pt2t, 
                            ISO_639_3.Id AS pt3, 
                            "" AS pt5
                        FROM ISO_639_3
                        LEFT JOIN (
                            SELECT
                              SUBSTR(Part1, INSTR(Part1, '-') + 1, 2) Part1,
                              SUBSTR(Part1, 1, INSTR(Part1, ' ') - 1) Change_To
                            FROM ISO_639_2_Changes
                            WHERE Part1 like "%[%" AND Notes NOT NULL 
                        ) Dep ON ISO_639_3.Part1 = Dep.Part1
                        UNION
                        SELECT 
                            ISO_639_5.Label_English AS name, 
                            IFNULL(ISO_639_2.Part1, "") AS pt1, 
                            IFNULL(ISO_639_2.Part2b, "") AS pt2b, 
                            IFNULL(
                                ISO_639_2.Part2t, 
                                IFNULL(ISO_639_2.Part2b, "")
                            ) AS pt2t, 
                            "" AS pt3, 
                            ISO_639_5.Code AS pt5
                        FROM ISO_639_5
                        LEFT JOIN ISO_639_2
                            ON ISO_639_5.Code = ISO_639_2.Part2b
                        UNION
                        SELECT 
                            substr(
                                ISO_639_2.English_Name, 
                                1, 
                                instr(ISO_639_2.English_Name, ';') - 1
                            ) AS name,
                            IFNULL(ISO_639_2.Part1, "") AS pt1,
                            ISO_639_2.Part2b AS pt2b, 
                            IFNULL(
                                ISO_639_2.Part2t, 
                                IFNULL(ISO_639_2.Part2b, "")
                            ) AS pt2t, 
                            "" AS pt3,
                            "" AS pt5
                        FROM ISO_639_2
                        LEFT JOIN ISO_639_3 
                            ON ISO_639_2.Part2b = ISO_639_3.Part2B
                        LEFT JOIN ISO_639_5 
                            ON ISO_639_2.Part2b = ISO_639_5.Code
                        WHERE ISO_639_3.Part2B IS NULL 
                            AND ISO_639_5.Code IS NULL
                            AND NOT ISO_639_2.Part2b like "%-%"
                        ORDER BY name
                    )
                    SELECT name, pt1, pt2b, pt2t, pt3, pt5 
                    FROM ISO_639
                    WHERE {0} != ""
                    ORDER BY {0}
                    """.format(
                    tag
                )
                for row in self._con.execute(sql):
                    dict_row = dict(row)
                    dict_row.pop(tag)
                    mapping.setdefault(tag, {})[row[tag]] = dict_row
        return mapping

    def get_mapping_deprecated(self) -> Dict[str, Dict[str, Dict[str, str]]]:
        mapping: Dict[str, Dict[str, Dict[str, str]]] = {}
        with self._con:
            for tag in ("id", "name"):
                sql = """
                    SELECT
                        SUBSTR(Part2, INSTR(Part2, '-') + 1, 3) AS id,
                        CASE INSTR(English_Name, ';')
                            WHEN 0 THEN English_Name
                            ELSE SUBSTR(
                                English_Name, 
                                0, 
                                INSTR(English_Name, ';')
                            )
                        END AS name,
                        Category_Of_Change AS reason,
                        SUBSTR(Part2, 1, INSTR(Part2, ' ') - 1) AS change_to,
                        Notes AS ret_remedy,
                        Date_Added_Or_Changed AS effective
                    FROM ISO_639_2_Changes
                    WHERE 
                        Part2 like "%[%" 
                        AND Notes NOT NULL 
                        AND Date_Added_Or_Changed < "2007-02-01"
                    UNION
                    SELECT
                        SUBSTR(Part1, INSTR(Part1, '-') + 1, 2) AS id,
                        CASE INSTR(English_Name, ';')
                            WHEN 0 THEN English_Name
                            ELSE SUBSTR(
                                English_Name, 
                                0, 
                                INSTR(English_Name, ';')
                            )
                        END AS name,
                        Category_Of_Change AS reason,
                        SUBSTR(Part1, 1, INSTR(Part1, '[') - 1) AS change_to,
                        Notes AS ret_remedy,
                        Date_Added_Or_Changed AS effective
                    FROM ISO_639_2_Changes
                    WHERE Part1 like "%[%"
                        AND Notes NOT NULL 
                    """
                for row in self._con.execute(sql):
                    dict_row = dict(row)
                    dict_row.pop(tag)
                    mapping.setdefault(tag, {})[row[tag]] = dict_row

            for tag in ("id", "name"):
                sql = """
                    SELECT
                        rt.Id AS id,
                        rt.Ref_Name AS name,
                        rt.Ret_Reason AS reason,
                        IFNULL(rt.Change_To, "") AS change_to,
                        IFNULL(rt.Ret_Remedy, "") AS ret_remedy,
                        rt.Effective AS effective
                    FROM ISO_639_3_Retirements rt
                    WHERE Effective >= "2007-02-01"
                    """
                for row in self._con.execute(sql):
                    dict_row = dict(row)
                    dict_row.pop(tag)
                    mapping.setdefault(tag, {})[row[tag]] = dict_row

        mapping["id"] = dict(sorted(mapping["id"].items()))
        mapping["name"] = dict(sorted(mapping["name"].items()))

        return mapping

    def get_mapping_macro(self) -> Dict[str, Dict[str, Any]]:
        mapping: Dict[str, Dict[str, Any]] = {}
        with self._con:
            sql = """
                SELECT
                    M_Id AS macro,
                    I_Id AS individual
                FROM ISO_639_3_Macrolanguages
                WHERE I_Status = "A"
                ORDER BY macro ASC, individual ASC
                """
            for macro, individual in self._con.execute(sql):
                mapping.setdefault("macro", {}).setdefault(macro, []).append(
                    individual
                )
            sql = """
                SELECT
                    I_Id AS individual,
                    M_Id AS macro
                FROM ISO_639_3_Macrolanguages
                WHERE I_Status = "A"
                ORDER BY individual ASC, macro ASC
                """
            for individual, macro in self._con.execute(sql):
                mapping.setdefault("individual", {})[individual] = macro
        return mapping

    def get_mapping_ref_name(self) -> Dict[str, str]:
        with self._con:
            sql = """ 
                WITH ref_names AS (
                    SELECT
                        ISO_639_3.Part2b AS id,
                        ISO_639_3.Ref_Name AS ref_name
                    FROM ISO_639_3
                    WHERE ISO_639_3.Part2b NOTNULL
                    UNION
                    SELECT
                        ISO_639_3.Id AS id,
                        ISO_639_3.Ref_Name AS ref_name
                    FROM ISO_639_3
                    UNION
                    SELECT 
                        ISO_639_2.Part2b AS id, 
                        ISO_639_5.Label_English AS ref_name
                    FROM ISO_639_5
                    INNER JOIN ISO_639_2
                        ON ISO_639_5.Code = ISO_639_2.Part2b
                    UNION
                    SELECT 
                        ISO_639_2.Part2b AS id,
                        substr(
                            ISO_639_2.English_Name, 
                            1, 
                            instr(ISO_639_2.English_Name, ';') - 1
                        ) AS ref_name
                    FROM ISO_639_2
                    LEFT JOIN ISO_639_3 
                        ON ISO_639_2.Part2b = ISO_639_3.Part2B
                    LEFT JOIN ISO_639_5 
                        ON ISO_639_2.Part2b = ISO_639_5.Code
                    WHERE ISO_639_3.Part2B IS NULL 
                        AND ISO_639_5.Code IS NULL
                        AND NOT ISO_639_2.Part2b like "%-%"
                )
                SELECT 
                    ISO_639_3_Names.Print_Name AS other_name,
                    ref_names.ref_name
                FROM ISO_639_3_Names
                INNER JOIN ref_names ON ISO_639_3_Names.Id = ref_names.id
                    WHERE other_name != ref_name
                UNION
                SELECT 
                    ISO_639_3_Names.Inverted_Name AS other_name,
                    ref_names.ref_name
                FROM ISO_639_3_Names
                INNER JOIN ref_names ON ISO_639_3_Names.Id = ref_names.id
                    WHERE other_name != ref_name
                UNION
                SELECT 
                    ISO_639_2.English_Name AS other_name,
                    ref_names.ref_name
                FROM ISO_639_2
                INNER JOIN ref_names ON ISO_639_2.Part2b = ref_names.id
                    WHERE other_name != ref_name
                ORDER BY other_name
                """
            mapping = {}
            for joined_names, ref_name in self._con.execute(sql):
                for other_name in joined_names.split("; "):
                    if other_name != ref_name:
                        mapping[other_name] = ref_name

        return dict(sorted(mapping.items()))

    def get_mapping_other_names(self) -> Dict[str, List[str]]:
        with self._con:
            sql = """
                WITH ref_names AS (
                    SELECT
                        ISO_639_3.Part2b AS id,
                        ISO_639_3.Ref_Name AS ref_name
                    FROM ISO_639_3
                    WHERE ISO_639_3.Part2b NOTNULL
                    UNION
                    SELECT
                        ISO_639_3.Id AS id,
                        ISO_639_3.Ref_Name AS ref_name
                    FROM ISO_639_3
                    UNION
                    SELECT 
                        ISO_639_2.Part2b AS id, 
                        ISO_639_5.Label_English AS ref_name
                    FROM ISO_639_5
                    INNER JOIN ISO_639_2
                        ON ISO_639_5.Code = ISO_639_2.Part2b
                    UNION
                    SELECT 
                        ISO_639_2.Part2b AS id,
                        substr(
                            ISO_639_2.English_Name, 
                            1, 
                            instr(ISO_639_2.English_Name, ';') - 1
                        ) AS ref_name
                    FROM ISO_639_2
                    LEFT JOIN ISO_639_3 
                        ON ISO_639_2.Part2b = ISO_639_3.Part2B
                    LEFT JOIN ISO_639_5 
                        ON ISO_639_2.Part2b = ISO_639_5.Code
                    WHERE ISO_639_3.Part2B IS NULL 
                        AND ISO_639_5.Code IS NULL
                        AND NOT ISO_639_2.Part2b like "%-%"
                )
                SELECT ref_name, group_concat(other_name, "; ")
                FROM (
                    SELECT 
                        ref_names.ref_name,
                        ISO_639_3_Names.Print_Name AS other_name
                    FROM ISO_639_3_Names
                    INNER JOIN ref_names ON ISO_639_3_Names.Id = ref_names.id
                        WHERE other_name != ref_name
                    UNION
                    SELECT 
                        ref_names.ref_name,
                        ISO_639_3_Names.Inverted_Name AS other_name
                    FROM ISO_639_3_Names
                    INNER JOIN ref_names ON ISO_639_3_Names.Id = ref_names.id
                        WHERE other_name != ref_name
                    UNION
                    SELECT 
                        ref_names.ref_name,
                        ISO_639_2.English_Name AS other_name
                    FROM ISO_639_2
                    INNER JOIN ref_names ON ISO_639_2.Part2b = ref_names.id
                        WHERE other_name != ref_name
                    ORDER BY ref_name, other_name
                )
                GROUP BY ref_name
                ORDER BY ref_name
                """
            other_names = defaultdict(set)
            for ref_name, joined_names in self._con.execute(sql):
                for other_name in joined_names.split("; "):
                    if other_name != ref_name:
                        other_names[ref_name].add(other_name)

        return {
            ref_name: sorted(list(other_names))
            for ref_name, other_names in other_names.items()
        }

    def get_mapping_scope(self) -> Dict[str, str]:
        with self._con:
            sql = """
                SELECT 
                    Id As pt3, 
                    Scope AS scope 
                FROM ISO_639_3 
                ORDER BY pt3
                """
            mapping = {
                row["pt3"]: row["scope"] for row in self._con.execute(sql)
            }
        return mapping

    def get_mapping_type(self) -> Dict[str, str]:
        with self._con:
            sql = """
                SELECT 
                    Id As pt3, 
                    Type AS type 
                FROM ISO_639_3 
                ORDER BY pt3
                """
            mapping = {
                row["pt3"]: row["type"] for row in self._con.execute(sql)
            }
        return mapping

    def get_list_langs(self) -> List[str]:
        with self._con:
            sql = """
                SELECT
                    ISO_639_3.Ref_Name AS name
                FROM ISO_639_3
                UNION
                SELECT 
                    ISO_639_5.Label_English AS name
                FROM ISO_639_5
                UNION
                SELECT 
                    substr(
                        ISO_639_2.English_Name, 
                        1, 
                        instr(ISO_639_2.English_Name, ';') - 1
                    ) AS name
                FROM ISO_639_2
                LEFT JOIN ISO_639_3 
                    ON ISO_639_2.Part2b = ISO_639_3.Part2B
                LEFT JOIN ISO_639_5 
                    ON ISO_639_2.Part2b = ISO_639_5.Code
                WHERE ISO_639_3.Part2B IS NULL 
                    AND ISO_639_5.Code IS NULL
                    AND NOT ISO_639_2.Part2b like "%-%"
                ORDER BY name
                """
            language_names = [row["name"] for row in self._con.execute(sql)]
        return language_names
