import json
import os.path
from screeninfo import get_monitors

MAIN_SCREEN_INFO = get_monitors()[0]
BUTTONS = ["Play_menu", "Play_mode_main_menu", "Play_mode_sub_menu"]

def load_json_save():
    path = "config\\config.json"
    if not os.path.isfile(path):
        with open(path, "w+") as outfile:
            json.dump(
                {"config_path": path, "rectangles" : {}},
                outfile,
                indent=4,
                sort_keys=True,
            )

    with open(path, "r") as f:
        config = json.load(f)
    return config


def save_config(config):
    with open(config["config_path"], "w+") as outfile:
        json.dump(config, outfile, indent=4, sort_keys=True)


def edit_config(key, value, config):
    config[key] = value
    save_config(config)


def load_config():
    config = load_json_save()
    return config
