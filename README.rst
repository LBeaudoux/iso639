ISO 639
=======

A lightweight library for ISO 639-1, ISO 639-2 and ISO 639-3 language representation standards.


Installation
------------

This library requires Python 3.6. 

.. code:: sh

    pip3 install iso639-lang


Usage
-----

.. code-block:: python

    >>> from iso639 import Lang

    >>> language = Lang("fr")
    >>> language.pt1
    'fr'
    >>> language.pt2b
    'fre'
    >>> language.pt2t
    'fra'
    >>> language.pt3
    'fra'    
    >>> language.name
    'French'   

    >>> language.name = 'German'
    >>> language.pt1
    'de'
    >>> language.pt2b
    'ger'
    >>> language.pt2t
    'deu'
    >>> language.pt3
    'deu'    
    >>> language.name
    'German'   

    >>> other_language = Lang("ger")
    >>> language == other_language
    True

    >>> other_language = Lang(language)
    >>> language == other_language
    True



Contains external data
----------------------

- `ISO 639-3 Code Set`_, dated 2020-01-20

.. _ISO 639-3 Code Set: https://iso639-3.sil.org/sites/iso639-3/files/downloads/iso-639-3.tab

