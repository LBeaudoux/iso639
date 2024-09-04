import argparse
import logging

from dev_iso639 import (
    download_source_data_files,
    generate_library_embedded_data_files,
)

logging.basicConfig(level=logging.INFO, format="%(message)s")


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--download",
        action="store_true",
        help="Download source ISO 639 data files",
    )

    args = parser.parse_args()

    if args.download:
        download_source_data_files()

    generate_library_embedded_data_files()


if __name__ == "__main__":
    main()
