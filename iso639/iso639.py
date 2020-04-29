import csv
import json

from pkg_resources import resource_filename


TABLE_PATH =  resource_filename(__package__, 'iso-639-3.tab')
MAPPING_PATH =  resource_filename(__package__, 'iso-639-3.json')


def _load_iso639_mapping():
    """Load the ISO-639 mapping from its JSON file.
    """
    with open(MAPPING_PATH) as f:
        mapping = json.load(f)
    
    if not mapping:
        table = _load_iso639_table()
        mapping = _map_iso639_table(table)
        _save_iso639_mapping(mapping)
    
    return mapping

def _load_iso639_table():
    """Load the iso639 table from its tab file.
    """
    with open(TABLE_PATH) as f:
        rows = csv.reader(f, delimiter='\t')        
        return rows[1:]

def _map_iso639_table(table):
    """Turn the ISO-639 table into a dict for mapping iso639 values faster.
    """
    mapping = {k : {} for k in ("pt1", "pt3", "name")}
    for row in table:
        # ISO 639 part 1 codes
        if row[3]:
            mapping["pt1"][row[3]] = {"pt3": row[0], "name": row[6]}
        # ISO 639 part 3 codes
        if row[0]:
            mapping["pt3"][row[0]] = {"pt1": row[3], "name": row[6]}
        # ISO 639 names
        if row[6]:
            mapping["name"][row[6]] = {"pt1": row[3], "pt3": row[0]}
    
    return mapping

def _save_iso639_mapping(mapping_data):
    """Save the ISO-639 mapping into a JSON file.
    """
    with open(MAPPING_PATH, 'w') as f:
        json.dump(mapping_data, f)    



class Lang:
    """Handle the code and the name of a given language by loading an 
    ISO 639-3 to ISO 639 name language mapping.
    data url on the official site of the ISO 639-3 Registration Authority:
    https://iso639-3.sil.org/sites/iso639-3/files/downloads/iso-639-3.tab    
    """
    _data = _load_iso639_mapping()

    def __init__(self, language=None):
        if not language:
            self.pt3 = ""
        elif len(language) == 3:
            self.pt3 = language
        elif len(language) == 2:
            self.pt1 = language
        else:
            self.name = language

    def __repr__(self):
        return f"pt3 : {self.pt3}, pt1 : {self.pt1}, name : {self.name}"
    
    def _fetch_part1(self, lang_key):
        """Fetch the part1 code that corespond to this key.
        """
        try:
            if len(lang_key) == 3:
                pt1 = Lang._data["pt3"][lang_key]["pt1"]
            elif len(lang_key) > 3:
                pt1 = Lang._data["name"][lang_key]["pt1"]
            else:
                pt1 = lang_key if lang_key in self._data["pt1"] else ""
        except KeyError:
            print(f"{lang_key} is not an ISO-639 value.")
            pt1 = ""
        
        return pt1

    def _fetch_part3(self, lang_key):
        """Fetch the part 3 code that corespond to this language key.
        """
        try:
            if len(lang_key) == 2:
                pt3 = self._data["pt1"][lang_key]["pt3"]
            elif len(lang_key) > 3:
                pt3 = self._data["name"][lang_key]["pt3"]
            else:
                pt3 = lang_key if lang_key in self._data["pt3"] else ""
        except KeyError:
            print(f"{lang_key} is not an ISO-639 value.")
            pt3 = ""
        
        return pt3

    def _fetch_name(self, lang_key):
        """Fetch the name that corespond to this language key.
        """
        try:
            if len(lang_key) == 3:
                name = self._data["pt3"][lang_key]["name"]
            elif len(lang_key) == 2:
                name = self._data["pt1"][lang_key]["name"]
            else:
                name = lang_key if lang_key in self._data["name"] else ""
        except KeyError:
            print(f"{lang_key} is not an ISO-639 value.")
            name = ""

        return name                                  
    
    @property
    def pt3(self):
        """Get the code of this language.
        """
        return self._pt3

    @pt3.setter
    def pt3(self, lang_pt3):
        """Set the code of this language and then change the name too.
        """
        self._pt3 = lang_pt3.lower()
        self._name = self._fetch_name(lang_pt3)
        self._pt1 = self._fetch_part1(lang_pt3)

    @property
    def pt1(self):
        """Get the part1 code of this language.
        """
        return self._pt1

    @pt1.setter
    def pt1(self, lang_pt1):
        """Set the part1 of this language and then change the code and name too.
        """
        self._pt1 = lang_pt1.lower()
        self._name = self._fetch_name(lang_pt1)        
        self._pt3 = self._fetch_part3(lang_pt1)        

    @property
    def name(self):
        """Get the name of this language.
        """
        return self._name

    @name.setter
    def name(self, lang_name):
        """Set the name of this language and then the code and the pt1 too.
        """
        self._name = lang_name.capitalize()
        self._pt3 = self._fetch_part3(lang_name)
        self._pt1 = self._fetch_part1(lang_name)