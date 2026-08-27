import argparse
from pathlib import Path

from bikeshare.data.download import RAW_DATA_DIR, URL, download


def main() -> None:
    parser = argparse.ArgumentParser(description="Download the UCI bike sharing data")
    parser.add_argument("--output", type=Path, default=RAW_DATA_DIR)
    args = parser.parse_args()

    print(f"Downloading {URL}")
    paths = download(args.output)
    print(f"Saved {len(paths)} files to {args.output}")


if __name__ == "__main__":
    main()
