import matplotlib.pyplot as plt
import numpy as np
import pyautogui
from matplotlib.widgets import RectangleSelector
import PySimpleGUI as sg
from os import listdir
from os.path import isfile, join
import cv2
from PIL import Image
import imagehash
from time import sleep
import pydirectinput
from src.config import BUTTONS


def crop_screenshot(img, x, y, w, h):
    return img[y : y + h, x : x + w]


def take_screenshot(pyautogui_default_color):
    img = np.array(pyautogui.screenshot())
    if pyautogui_default_color:
        return img
    return img[:, :, ::-1]


class RectangleSelection(object):
    def __init__(self, img, name):
        self.rectangle = None
        self.img = img
        self.done = False

        # Setup the figure
        self.fig, self.ax = plt.subplots()
        self.fm = plt.get_current_fig_manager()
        plt.ion
        plt.title(
            f"Draw a rectangle, using mouse, on {name} rectangle. Press `q` to continue."
        )
        plt.imshow(self.img)
        manager = plt.get_current_fig_manager()
        manager.full_screen_toggle()
        plt.margins(0, 0)

        self.RS = RectangleSelector(
            self.ax,
            self.onselect,
            drawtype="box",
            useblit=True,
            button=[1, 3],
            minspanx=5,
            minspany=5,
            spancoords="pixels",
            interactive=True,
        )

        plt.connect("key_press_event", self.toggle_selector)
        plt.show()

    def onselect(self, e_click, e_release):
        x1, y1 = e_click.xdata, e_click.ydata
        x2, y2 = e_release.xdata, e_release.ydata
        print("(%3.2f, %3.2f) --> (%3.2f, %3.2f)" % (x1, y1, x2, y2))
        pt1 = (x1, y1)
        pt2 = (x2, y2)
        # calculate top left corner coords, width, height
        min_x = min(int(pt1[0]), int(pt2[0]))  # left
        min_y = min(int(pt1[1]), int(pt2[1]))  # top
        width = max(int(pt1[0]), int(pt2[0])) - min_x
        height = max(int(pt1[1]), int(pt2[1])) - min_y
        self.rectangle = (min_x, min_y, width, height)

    def toggle_selector(self, event):
        if event.key in ["Q", "q"] and self.RS.active:
            self.RS.set_active(False)
            self.done = True

    def close(self):
        # plt.show(block=False)
        plt.close()


def set_process_state(is_running, window, key):
    window.Element(key).Update(
        ("PAUSED", "RUNNING")[is_running],
        button_color=(("white", ("red", "green")[is_running])),
    )
    return is_running


def make_layout(title, run_key):
    layout = [
        [
            [sg.Text(title)],
            [
                [sg.Button(f"Set {name_rectangle} button", key=name_rectangle)]
                for name_rectangle in BUTTONS
            ],
            [sg.Text("""Configure loadout name to "Myloadout" """)],
            [sg.Button("Run", key=run_key)],
        ]
    ]
    return layout


def make_window(title, run_key):
    window = sg.Window(title, make_layout(title, run_key), finalize=True)
    window.bind(f"<Key-{run_key}>", run_key)
    return window


def live_image_process(rectangle):
    x = rectangle[0]
    y = rectangle[1]
    w = rectangle[2]
    h = rectangle[3]

    img = take_screenshot(False)
    img = crop_screenshot(img, x, y, w, h)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return img


def has_template_in_image(rectangle, template):
    loc = pyautogui.locateOnScreen(
        template, region=rectangle, grayscale=True, confidence=0.5
    )
    print(loc)
    if loc:
        loc_point = pyautogui.center(loc)
        x, y = loc_point
        print(loc_point)
        pydirectinput.moveTo(x, y)
        pydirectinput.mouseDown()
        sleep(0.5)
        pydirectinput.mouseUp()
        print("clicked")
        return True
    else:
        return False


def load_sources():
    mypath = "img"
    file_names = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    imgs_src = []
    for source_img_index in range(len(file_names)):
        img = np.asarray(Image.open(mypath + "\\" + file_names[source_img_index]))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        imgs_src.append(img)
    return dict(zip(file_names, imgs_src))


def compare_imgs(img_src, img):
    hash0 = imagehash.average_hash(Image.fromarray(img_src).resize(size=(100, 100)))
    hash1 = imagehash.average_hash(Image.fromarray(img).resize(size=(100, 100)))
    return hash0 - hash1
