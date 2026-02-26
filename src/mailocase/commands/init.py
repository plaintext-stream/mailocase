import copy
from pathlib import Path

from mailocase.config import DEFAULT_CONFIG, save_config


def cmd_init(location: str = ".") -> None:
    path = Path(location).resolve()
    path.mkdir(parents=True, exist_ok=True)
    (path / "draft").mkdir(exist_ok=True)
    (path / "mail").mkdir(exist_ok=True)
    (path / "static").mkdir(exist_ok=True)

    cfg_path = path / "config.json"
    if cfg_path.exists():
        print(f"Already initialized at {path}")
    else:
        save_config(copy.deepcopy(DEFAULT_CONFIG), cfg_path)
        print(f"Initialized mailocase at {path}")
        print(f"Edit {cfg_path} to configure your mailing list.")
