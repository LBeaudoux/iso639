
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
`iso639-lang` supports Python 3.7+.  
  
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
>>> lg.pt2b # 639-2 bibliographic identifier
'ger'
>>> lg.pt2t # 639-2 terminological identifier
'deu'
>>> lg.pt3 # 639-3 identifier
'deu'
```

And now with the identifier of a group of languages.
```python
>>> lg = Lang("cel")
>>> lg.name # 639-5 English name
'Celtic languages'
>>> lg.pt2b # 639-2 bibliographic identifier
'cel'
>>> lg.pt5 # 639-5 identifier
'cel'
```

`Lang` is instantiable with any ISO 639 identifier or name.
```python
>>> Lang("German") == Lang("de") == Lang("deu") == Lang("ger")
True
```

Please note that `Lang` is case-sensitive.
```python
>>> Lang("ak")
Lang(name='Akan', pt1='ak', pt2b='aka', pt2t='aka', pt3='aka', pt5='')
>>> Lang("Ak")
Lang(name='Ak', pt1='', pt2b='', pt2t='', pt3='akq', pt5='')
```

`Lang` recognizes all English names that can be associated with a language identifier according to ISO 639.
```python
>>> Lang("Chinese, Mandarin") # ISO 639-3 inverted name
Lang(name='Mandarin Chinese', pt1='', pt2b='', pt2t='', pt3='cmn', pt5='')
>>> Lang("Uyghur") # other ISO 639-3 printed name
Lang(name='Uighur', pt1='ug', pt2b='uig', pt2t='uig', pt3='uig', pt5='')
>>> Lang("Valencian") # other ISO 639-2 English name
Lang(name='Catalan', pt1='ca', pt2b='cat', pt2t='cat', pt3='cat', pt5='')
```

You can use the `asdict` method to return ISO 639 values as a Python dictionary.
```python
>>> Lang("fra").asdict()
{'name': 'French', 'pt1': 'fr', 'pt2b': 'fre', 'pt2t': 'fra', 'pt3': 'fra', 'pt5': ''}
```

### In data structures

Lists of `Lang` instances are sortable by name. 
```python
>>> [lg.name for lg in sorted([Lang("deu"), Lang("rus"), Lang("eng")])]
['English', 'German', 'Russian']
```
As `Lang` is hashable, `Lang` instances can be added to a set or used as dictionary keys.
```python
>>> {Lang("de"): "foo", Lang("fr"):  "bar"}
{Lang(name='German', pt1='de', pt2b='ger', pt2t='deu', pt3='deu', pt5=''): 'foo', Lang(name='French', pt1='fr', pt2b='fre', pt2t='fra', pt3='fra', pt5=''): 'bar'}
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
'Historical'
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

### Other Language Names

In addition to their reference name, some language identifiers may be associated with other names. You can list them using the `other_names` method.
```python
>>> lg = Lang("ast")
>>> lg.name
'Asturian'
>>> lg.other_names()
['Asturleonese', 'Bable', 'Leonese']
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

## Speed

`iso639-lang` loads its mappings into memory to process calls much [faster](https://github.com/LBeaudoux/benchmark-iso639) than libraries that rely on an embedded database.

## Sources

As of August 21, 2024, `iso639-lang` is based on the latest tables provided by the ISO 639 registration authorities.
 
| Set                                                                            | Description                                                                                                                   | Registration Authority |
| ------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------- | ---------------------- |
| [Set 1](https://iso639-3.sil.org/sites/iso639-3/files/downloads/iso-639-3.tab) | _two-letter language identifiers for major, mostly national individual languages_                                            | Infoterm               |
| [Set 2](https://www.loc.gov/standards/iso639-2/ISO-639-2_utf-8.txt)            | _three-letter language identifiers for a larger number of widely known individual languages and a number of language groups_ | Library of Congress    |
| [Set 3](https://iso639-3.sil.org/sites/iso639-3/files/downloads/iso-639-3.tab) | _three-letter language identifiers covering all individual languages, including living, extinct and ancient languages_       | SIL International      |
| [Set 5](http://id.loc.gov/vocabulary/iso639-5.tsv)                             | _three-letter language identifiers covering a larger set of language groups, living and extinct_                             | Library of Congress    |

