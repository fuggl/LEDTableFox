import RPi.GPIO as GPIO

# Button channels
BUTTON_CH_1 = [4, 27, 23, 5, 16, 20]  # left buttons
BUTTON_CH_2 = [17, 22, 24, 6, 26, 21]  # right buttons
BUTTON_IDX_LEFT = 1
BUTTON_IDX_RIGHT = 2

SEAT_IDX = {}
BUTTON_IDX = {}


def empty_listener(seat_idx, button_idx):
    print("{} {}".format(seat_idx, button_idx))


listener = empty_listener


def register(button_callback):
    global listener
    listener = button_callback


def button_press(channel):
    listener(SEAT_IDX[channel], BUTTON_IDX[channel])


def setup_button(channel):
    GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def setup_button_interrupt(channel):
    GPIO.add_event_detect(channel, GPIO.FALLING, callback=button_press, bouncetime=500)


def init():
    GPIO.setmode(GPIO.BCM)
    global SEAT_IDX, BUTTON_IDX
    i = 0
    while i < len(BUTTON_CH_1):
        # add button channels with current seat
        seat_index = i + 1
        SEAT_IDX[BUTTON_CH_1[i]] = seat_index
        SEAT_IDX[BUTTON_CH_2[i]] = seat_index
        # add button channels with button index
        BUTTON_IDX[BUTTON_CH_1[i]] = BUTTON_IDX_LEFT
        BUTTON_IDX[BUTTON_CH_2[i]] = BUTTON_IDX_RIGHT
        # setup channels
        setup_button(BUTTON_CH_1[i])
        setup_button(BUTTON_CH_2[i])
        setup_button_interrupt(BUTTON_CH_1[i])
        setup_button_interrupt(BUTTON_CH_2[i])
        i += 1