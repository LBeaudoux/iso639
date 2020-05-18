ISO 639
=======

A simple library for ISO 639-1 and ISO 639-3 language codes.


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
    >>> language.pt3
    'fra'    
    >>> language.name
    'French'   

    >>> language.pt3 = 'eng'
    >>> language.pt1
    'en'    
    >>> language.name
    'English' 

    >>> language.name = 'German'
    >>> language.pt1
    'de'
    >>> language.pt3
    'deu'    


Contains external data
----------------------

- `ISO 639-3 Code Set`_, dated 2020-01-20

.. _ISO 639-3 Code Set: https://iso639-3.sil.org/sites/iso639-3/files/downloads/iso-639-3.tab

