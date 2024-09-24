import json
import logging
from io import StringIO
from typing import Any

import pandas as pd
import requests

from .datafile import DataFile

logger = logging.getLogger(__name__)


def download(file_name: str) -> None:
    """Downloads the file of an ISO 639 table to the project
    download directory.

    Parameters
    ----------
    file_name : str
        The name of an official ISO 639 data file.
    """
    data_file = DataFile(file_name)
    with requests.get(data_file.download_url) as r:
        file_encoding = r.apparent_encoding
        with open(data_file.path, "wb") as f:
            f.write(r.content)

    logger.info(
        f"{data_file.name} ({file_encoding} encoding) "
        f"downloaded at {data_file.path}"
    )


def scrape(file_name: str) -> None:
    """Scrapes an ISO 639 table to the project download directory.

    Parameters
    ----------
    file_name : str
        The name of an official ISO 639 data file.
    """
    data_file = DataFile(file_name)
    with requests.get(data_file.scrap_url) as r:
        html_str = StringIO(r.text)
        table = pd.read_html(html_str)[1]
    table.to_csv(data_file.path, sep="\t", index=False)

    logger.info(f"{data_file.name} scraped at {data_file.path}")


def get_data(file_name: str) -> pd.DataFrame:
    """Loads the file of an ISO 639 table as a dataframe.

    Parameters
    ----------
    file_name : str
        The name of a reference ISO 639 data file.

    Returns
    -------
    pd.DataFrame
        The dataframe of the file.
    """
    data_file = DataFile(file_name)
    return pd.read_csv(data_file.path, **data_file.params)


def serialize(data: Any, file_name: str) -> None:
    """Saves an ISO 639 mapping or list as a JSON file.

    Parameters
    ----------
    data : Union[List, Dict]
        An ISO 639 mapping or list.
    file_name : str
        The name of a reference ISO 639 data file.
    """
    data_file = DataFile(file_name)
    with open(data_file.path, "w", encoding="utf-8") as f:
        json.dump(data, f)
    logger.info(f"{data_file.name} serialized at {data_file.path}")
