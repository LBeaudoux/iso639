from typing import Iterator

from .iso639 import Lang
from .datafile import load_langs

Lang = Lang


def iter_langs() -> Iterator[Lang]:
    """Iterate through all not deprecated ISO 639 languages

    Yields
    -------
    Lang
        Lang instances in alphabetical order
    """
    sorted_langs = load_langs()

    return iter(sorted_langs)
