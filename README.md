
# iso639-lang

![PyPI](https://img.shields.io/pypi/v/iso639-lang)
![Supported Python versions](https://img.shields.io/pypi/pyversions/iso639-lang.svg)
![PyPI - Downloads](https://img.shields.io/pypi/dm/iso639-lang)
  
**iso639-lang** is a simple library to handle the ISO 639 series of international standards for language codes.

```python
>>> from iso639 import Lang
>>> Lang("fr")
Lang(name='French', pt1='fr', pt2b='fre', pt2t='fra', pt3='fra', pt5='')
```

iso639-lang allows you to switch from one language code to another easily. 
There’s no need to manually download or parse data files, just use the `Lang` class!

ISO 639-1, ISO 639-2, ISO 639-3 and ISO 639-5 parts are all supported.

## Installing iso639-lang and Supported Versions

iso639-lang is available on PyPI:

```console
$ pip install iso639-lang
```
iso639-lang supports Python 3.7+.  
  
## Usage

Handling language codes with iso639-lang is very simple.

Begin by importing the `Lang` class:
```python
>>> from iso639 import Lang
```

`Lang` is instantiable with any ISO 639 language code or name. For example, let’s try to get the ISO 639 codes for French:
```python
>>> lg = Lang("French")
>>> lg.name
'French'
>>> lg.pt1
'fr'
>>> lg.pt2b
'fre'
>>> lg.pt2t
'fra'
>>> lg.pt3
'fra'
>>> lg.pt5
''
```

You can use the `asdict` method to return ISO 639 language values as a Python dictionary.
```python
>>> lg.asdict()
{'name': 'French', 'pt1': 'fr', 'pt2b': 'fre', 'pt2t': 'fra', 'pt3': 'fra', 'pt5': ''}
```

### In data structures
Lists of `Lang` instances are sortable by name. 
```python
>>> langs = [Lang("deu"), Lang("eng"), Lang("rus"), Lang("eng")]
>>> [lg.name for lg in sorted(langs)]
['English', 'English', 'German', 'Russian']
```
As `Lang` is hashable, `Lang` instances can be added to a set or used as dictionary keys.
```python
>>> [lg.pt3 for lg in set(langs)]
['eng', 'rus', 'deu']
```

### Iterator

`iter_langs()` iterates through all possible `Lang` instances, ordered alphabetically by name.

```python
>>> from iso639 import iter_langs
>>> [lg.name for lg in iter_langs()]
["'Are'are", "'Auhelawa", "A'ou", ... , 'ǂHua', 'ǂUngkue', 'ǃXóõ']
```

### Language Types

The type of a language is accessible thanks to the `type` method.
```python
>>> lg = Lang("Latin")
>>> lg.type()
'Ancient'
```

### Macrolanguages

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
"'foobar' not supported by ISO 639"
```

When an deprecated language value is passed to `Lang`, a `DeprecatedLanguageValue` exception is raised.
```python
>>> from iso639.exceptions import DeprecatedLanguageValue
>>> try:
...     Lang("gsc")
... except DeprecatedLanguageValue as e:
...     lg = Lang(e.change_to)
...     f"{e.name} replaced by {lg.name}"
...
'Gascon replaced by Occitan (post 1500)'
```

## Sources of data used by iso639-lang

As of November 12, 2023, iso639-lang is based on the latest official code tables provided by the ISO 639 registration authorities.
 
 
| Standard  | Name                                                                                       | Registration Authority |
| --------- | ------------------------------------------------------------------------------------------ | ---------------------- |
| [ISO 639-1](https://iso639-3.sil.org/sites/iso639-3/files/downloads/iso-639-3.tab) | *Part 1: Alpha-2 code*                                                                       | Infoterm               |
| [ISO 639-2](https://www.loc.gov/standards/iso639-2/ISO-639-2_utf-8.txt) | *Part 2: Alpha-3 code*                                                                       | Library of Congress    |
| [ISO 639-3](https://iso639-3.sil.org/sites/iso639-3/files/downloads/iso-639-3.tab) | *Part 3: Alpha-3 code for comprehensive coverage of languages*                               | SIL International      |
| ISO 639-4 | *Part 4: Implementation guidelines and general principles for language coding* (not a list)  | ISO/TC 37/SC 2         |
| [ISO 639-5](http://id.loc.gov/vocabulary/iso639-5.tsv) | *Part 5: Alpha-3 code for language families and groups*                                      | Library of Congress    |
