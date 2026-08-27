from io import BytesIO
from pathlib import Path
from urllib.request import urlopen
from zipfile import ZipFile

URL = "https://archive.ics.uci.edu/static/public/275/bike+sharing+dataset.zip"
FILES = ("hour.csv", "day.csv", "Readme.txt")
RAW_DATA_DIR = Path("data/raw")


def download(output_dir: Path = RAW_DATA_DIR) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)

    with urlopen(URL) as response:
        content = response.read()

    with ZipFile(BytesIO(content)) as archive:
        members = {Path(name).name: name for name in archive.namelist()}
        paths: list[Path] = []

        for filename in FILES:
            path = output_dir / filename
            path.write_bytes(archive.read(members[filename]))
            paths.append(path)

    return paths
