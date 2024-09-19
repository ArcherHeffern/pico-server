import os
from pathlib import Path

def is_subpath(base: Path, longer: Path) -> bool:
    if len(base.parts) > len(longer.parts):
        return False
    for bse, lng in zip(base.parts, longer.parts):
        if bse != lng:
            return False
    return True

def get_file(path: Path):
    with open(path, "r") as f:
        return f.read()

static_path = Path("./lib/collections")
file = Path("./lib/collections/two_way_dict.py")
if is_subpath(static_path, file):
    print(get_file(file))



