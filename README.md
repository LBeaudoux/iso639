
# iso639-lang

![PyPI](https://img.shields.io/pypi/v/iso639-lang)
![Supported Python versions](https://img.shields.io/pypi/pyversions/iso639-lang.svg)
![PyPI - Downloads](https://img.shields.io/pypi/dm/iso639-lang)
  
`iso639-lang` handles the ISO 639 code for individual languages and language groups.

```python
>>> from iso639 import Lang
>>> Lang("French")
Lang(name='French', pt1='fr', pt2b='fre', pt2t='fra', pt3='fra', pt5='')
```

## Installation

```console
$ pip install iso639-lang
```
`iso639-lang` supports Python 3.9+.  
  
## Usage

Begin by importing the `Lang` class.
```python
>>> from iso639 import Lang
```

Let's try with the identifier of an individual language.
```python
>>> lg = Lang("deu")
>>> lg.name # 639-3 reference name
'German'
>>> lg.pt1 # 639-1 identifier
'de'
>>> lg.pt2b # 639-2/B bibliographic identifier
'ger'
>>> lg.pt2t # 639-2/T terminological identifier
'deu'
>>> lg.pt3 # 639-3 identifier
'deu'
```

And now with the identifier of a group of languages.
```python
>>> lg = Lang("cel")
>>> lg.name # 639-5 English name
'Celtic languages'
>>> lg.pt2b # 639-2/B bibliographic identifier
'cel'
>>> lg.pt2t # 639-2/T terminological identifier
'cel'
>>> lg.pt5 # 639-5 identifier
'cel'
```

`Lang` is instantiable with any ISO 639 identifier or reference name.
```python
>>> Lang("German") == Lang("de") == Lang("deu") == Lang("ger")
True
```

`Lang` also recognizes all non-reference English names associated with a language identifier in ISO 639.
```python
>>> Lang("Chinese, Mandarin") # 639-3 inverted name
Lang(name='Mandarin Chinese', pt1='', pt2b='', pt2t='', pt3='cmn', pt5='')
>>> Lang("Uyghur") # other 639-3 printed name
Lang(name='Uighur', pt1='ug', pt2b='uig', pt2t='uig', pt3='uig', pt5='')
>>> Lang("Valencian") # other 639-2 English name
Lang(name='Catalan', pt1='ca', pt2b='cat', pt2t='cat', pt3='cat', pt5='')
```

Please note that `Lang` is case-sensitive.
```python
>>> Lang("ak")
Lang(name='Akan', pt1='ak', pt2b='aka', pt2t='aka', pt3='aka', pt5='')
>>> Lang("Ak")
Lang(name='Ak', pt1='', pt2b='', pt2t='', pt3='akq', pt5='')
```

### Other Language Names

In addition to their reference name, some language identifiers may be associated with other names. You can list them using the `other_names` method.
```python
>>> lg = Lang("ast")
>>> lg.name
'Asturian'
>>> lg.other_names()
['Asturleonese', 'Bable', 'Leonese']
```

### Language Type

The type of a language is accessible thanks to the `type` method.
```python
>>> lg = Lang("Latin")
>>> lg.type()
'Historical'
```

### Macrolanguage & Individual Languages

You can easily determine whether a language is a macrolanguage or an individual language.
```python
>>> lg = Lang("Arabic")
>>> lg.scope()
'Macrolanguage'
```

Use the `macro` method to get the macrolanguage of an individual language.
```python
>>> lg = Lang("Wu Chinese")
>>> lg.macro()
Lang(name='Chinese', pt1='zh', pt2b='chi', pt2t='zho', pt3='zho', pt5='')
```

Conversely, you can also list all the individual languages that share a common macrolanguage.
```python
>>> lg = Lang("Persian")
>>> lg.individuals()
[Lang(name='Iranian Persian', pt1='', pt2b='', pt2t='', pt3='pes', pt5=''), 
Lang(name='Dari', pt1='', pt2b='', pt2t='', pt3='prs', pt5='')]
```

### Exceptions

When an invalid language value is passed to `Lang`, an `InvalidLanguageValue` exception is raised.
```python
>>> from iso639.exceptions import InvalidLanguageValue
>>> try:
...     Lang("foobar")
... except InvalidLanguageValue as e:
...     e.msg
... 
"'foobar' is not a valid Lang argument."
```

When a deprecated language value is passed to `Lang`, a `DeprecatedLanguageValue` exception is raised.
```python
>>> from iso639.exceptions import DeprecatedLanguageValue
>>> try:
...     Lang("gsc")
... except DeprecatedLanguageValue as e:
...     lg = Lang(e.change_to)
...     f"{e.name} replaced by {lg.name}."
...
'Gascon replaced by Occitan (post 1500).'
```

Note that you can use the `is_language` language checker if you don't want to handle exceptions.

### Checker

The `is_language` function checks if a language value exists according to ISO 639.

```python
>>> from iso639 import is_language
>>> is_language("fr")
True
>>> is_language("French")
True
```

You can restrict the check to certain identifiers or names by passing an additional argument.
```python
>>> is_language("fr", "pt3") # only 639-3
False
>>> is_language("fre", ("pt2b", "pt2t")) # only 639-2/B or 639-2/T
True
```

### Iterator

`iter_langs()` iterates through all possible `Lang` instances, ordered alphabetically by name.

```python
>>> from iso639 import iter_langs
>>> [lg.name for lg in iter_langs()]
["'Are'are", "'Auhelawa", "A'ou", ... , 'ǂHua', 'ǂUngkue', 'ǃXóõ']
```


## Speed

`iso639-lang` loads its mappings into memory to process calls much faster than Python libraries that rely on an embedded database.


## Sources

As of July 19, 2025, `iso639-lang` is based on the latest tables provided by the ISO 639 registration authorities. Please open a new issue if you find that this library uses out-of-date data files.
 
| Set                                                                            | Description                                                                                                                  | Registration Authority | Last Modified                                                             |
|--------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------|------------------------|---------------------------------------------------------------------------|
| [Set 1](https://iso639-3.sil.org/sites/iso639-3/files/downloads/iso-639-3.tab) | _two-letter language identifiers for major, mostly national individual languages_                                            | Infoterm               | [2009-09-01](https://www.loc.gov/standards/iso639-2/php/code_changes.php) |
| [Set 2](https://www.loc.gov/standards/iso639-2/ISO-639-2_utf-8.txt)            | _three-letter language identifiers for a larger number of widely known individual languages and a number of language groups_ | Library of Congress    | [2017-12-21](https://www.loc.gov/standards/iso639-2/php/code_changes.php) |
| [Set 3](https://iso639-3.sil.org/sites/iso639-3/files/downloads/iso-639-3.tab) | _three-letter language identifiers covering all individual languages, including living, extinct and ancient languages_       | SIL International      | [2025-07-15](https://iso639-3.sil.org/code_tables/download_tables)        |
| [Set 5](http://id.loc.gov/vocabulary/iso639-5.tsv)                             | _three-letter language identifiers covering a larger set of language groups, living and extinct_                             | Library of Congress    | [2013-02-11](https://www.loc.gov/standards/iso639-5/changes.php)          |

To learn more about how the source tables are processed by the `iso639-lang` library, read the [`generate.py`](https://github.com/LBeaudoux/iso639/blob/master/generate.py) script.

## Contributing

We welcome contributions from the community to help improve this Python library. If you're interested in contributing, please follow the guidelines [here](https://github.com/LBeaudoux/iso639/blob/master/CONTRIBUTING.md).
