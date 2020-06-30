import time
from threading import Thread

BUTTON_IDX_LEFT = 1
BUTTON_IDX_RIGHT = 2


def empty_listener(seat_idx, button_idx):
    print("{} {}".format(seat_idx, button_idx))


listener = empty_listener


def register(button_callback):
    global listener
    listener = button_callback


def test_button():
    time.sleep(30)
    print("test button")
    listener(1, 1)


def init():
    Thread(target=test_button).start()
    return
