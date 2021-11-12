from multiprocessing import Process

import PySimpleGUI as sg
from PIL import Image

from src.config import save_config
from src.core import main_process
from src.utils import (
    RectangleSelection,
    take_screenshot,
    make_window,
    set_process_state,
)
from src.config import load_config, BUTTONS


def event_save_rec(window, run_key, config, name_rectangle):
    down_run_key = set_process_state(False, window, run_key)
    img = Image.fromarray(take_screenshot(True))
    selector = RectangleSelection(img, name_rectangle)
    while not selector.done:
        pass
    selector.close()
    config["rectangles"][name_rectangle] = selector.rectangle
    save_config(config)
    return down_run_key


def main():
    run_key = "F9"
    config = load_config()
    window = make_window("Warzone - Idle Exp Bot", run_key)
    down_run_key = False
    p = None

    while True:
        event, values = window.read()

        if event == "Exit" or event == sg.WIN_CLOSED:
            if p:
                p.terminate()
            break
        for name_rectangle in BUTTONS:
            if event == name_rectangle:
                if p:
                    p.terminate()
                down_run_key = event_save_rec(window, run_key, config, name_rectangle)

        if event == run_key:
            down_run_key = set_process_state(not down_run_key, window, run_key)

        if down_run_key:
            print("Starting process")
            p = Process(
                target=main_process,
                args=(config["rectangles"],),
            )
            p.start()
        else:
            if p:
                p.terminate()


if __name__ == "__main__":
    main()
