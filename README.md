
# iso639-lang

  
**iso639-lang** is a simple library to handle the ISO 639 series of international standards for language codes.

```python
>>> from iso639 import Lang
>>> Lang("fr")
Lang(name='French', pt1='fr', pt2b='fre', pt2t='fra', pt3='fra', pt5='')
```

iso639-lang allows you to switch from one language code to another easily. 
There’s no need to manually download or parse data files, just use the `Lang` class!

ISO 639-1, ISO 639-2, ISO 639-3  and ISO 639-5 parts are all supported.

## Installing iso639-lang and Supported Versions

iso639-lang is available on PyPI:

```console
$ pip install iso639-lang
```
iso639-lang supports Python 3.6+.  
  
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

An instance of `Lang` can be modified.
```python
>>> lg.pt1 = 'de'
>>> lg.name
'German'
```

`Lang` instances are comparable to each other.
```python
>>> other_lg = Lang("deu")
>>> lg == other_lg
True
```

## Data included in iso639-lang

iso639-lang is based on the official code tables provided by the ISO 639 registration authorities.
 
 
| Standard  | Name                                                                                       | Registration Authority | First edition | Current   |
| --------- | ------------------------------------------------------------------------------------------ | ---------------------- | ------------- | --------- |
| [ISO 639-1](https://iso639-3.sil.org/sites/iso639-3/files/downloads/iso-639-3.tab) | *Part 1: Alpha-2 code*                                                                       | Infoterm               | 1967          | 2002      |
| [ISO 639-2](https://www.loc.gov/standards/iso639-2/ISO-639-2_utf-8.txt) | *Part 2: Alpha-3 code*                                                                       | Library of Congress    | 1998          | 1998      |
| [ISO 639-3](https://iso639-3.sil.org/sites/iso639-3/files/downloads/iso-639-3.tab) | *Part 3: Alpha-3 code for comprehensive coverage of languages*                               | SIL International      | 2007          | 2007      |
| ISO 639-4 | *Part 4: Implementation guidelines and general principles for language coding* (not a list)  | ISO/TC 37/SC 2         | 2010          | 2010      |
| [ISO 639-5](http://id.loc.gov/vocabulary/iso639-5.tsv) | *Part 5: Alpha-3 code for language families and groups*                                      | Library of Congress    | 2008          | 2013      |
| ISO 639-6 | *Part 6: Alpha-4 representation for comprehensive coverage of language variants* | Geolang                | 2009          | withdrawn |
