from time import sleep

from src.config import BUTTONS, MAIN_SCREEN_INFO
from src.utils import take_screenshot, crop_screenshot
import pyautogui
import pydirectinput
import random
import easyocr


def make_action(rectangle):
    (x, y) = pyautogui.center(rectangle)
    print(x, y)
    pydirectinput.moveTo(x, y)
    pydirectinput.mouseDown()
    sleep(0.2)
    pydirectinput.mouseUp()


def move_randomly_in_game():
    keys = ["w", "a", "d"]
    for key in keys:
        print(f"Pressing {key}")
        pydirectinput.keyDown(key)
        sleep(random.uniform(0.5, 3))
        pydirectinput.keyUp(key)


def ocr_screen(reader, w, h, w_scaling, h_scaling):
    print("Reading screen")
    img = take_screenshot(True)
    img = crop_screenshot(
        img,
        w_scaling,
        h_scaling,
        w,
        h,
    )
    # im = Image.fromarray(img)
    # im.save("your_file.jpeg")
    return reader.readtext(img)


def get_rect_from_bbox(r, w_scaling, h_scaling):
    bbox = r[0]
    x, y = bbox[0]
    return [
        w_scaling + int(x),
        h_scaling + int(y),
        int(bbox[1][0] - bbox[0][0]),
        int(bbox[3][1] - bbox[0][1]),
    ]


def is_in_end_game_menu(reader):
    print("Checking if is in end game menu")
    has_play = False
    has_again = False
    has_play_again = False
    scaling = 3 / 2
    w = MAIN_SCREEN_INFO.width
    h = MAIN_SCREEN_INFO.height
    w_scaling = int(w / scaling)
    h_scaling = int(h / scaling)
    for r in ocr_screen(reader, w, h, w_scaling, h_scaling):
        if "play again with team" == r[1].lower():
            pass
        if "play again" == r[1].lower():
            print("play again")
            rectangle = get_rect_from_bbox(r, w_scaling, h_scaling)
            make_action(rectangle)
            has_play_again = True

    if (has_play and has_again) or has_play_again:
        for _ in range(2):
            pydirectinput.press("down")
        pydirectinput.press("space")
        return True
    else:
        return False


# Bot Logic
action_graph = {
    "Play_menu": "Play_mode_main_menu",
    "Play_mode_main_menu": "Play_mode_sub_menu",
    "Play_mode_sub_menu": "move_in_game",
    "move_in_game": "exit_game",
    "exit_game": "Play_menu",
}


def main_process(rectangles):
    # will take time at first to dl and build models. Should be instant after first run
    reader = easyocr.Reader(["en"])
    # Load source images
    status = "exit_game"
    while status:
        print(status)
        status = action_graph[status]
        if status in BUTTONS:
            make_action(rectangles[status])
        if status == "move_in_game":
            # Make security to exit and return to main menu? Timer => 20 minutes max until force exit
            while not is_in_end_game_menu(reader):
                # Select loadout
                results = ocr_screen(
                    reader, MAIN_SCREEN_INFO.width, MAIN_SCREEN_INFO.height, 1, 1
                )
                for r in results:
                    if r[1].lower() in ["myloadout", "yes"]:
                        rectangle = get_rect_from_bbox(r, 1, 1)
                        make_action(rectangle)
                pydirectinput.press("space")
                # move_randomly_in_game multiple times
                for _ in range(5):
                    move_randomly_in_game()
        sleep(1)
