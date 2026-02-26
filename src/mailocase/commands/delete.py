from mailocase.config import find_config


def cmd_delete(name: str) -> None:
    cfg_path = find_config()
    if cfg_path is None:
        print("Error: Not in a mailocase directory.")
        return

    base = cfg_path.parent
    draft_path = base / "draft" / name
    mail_path = base / "mail" / name

    if draft_path.exists():
        draft_path.unlink()
        print(f"Deleted draft: {name}")
    elif mail_path.exists():
        mail_path.unlink()
        print(f"Deleted sent mail: {name}")
    else:
        print(f"Error: '{name}' not found in drafts or sent mail.")
