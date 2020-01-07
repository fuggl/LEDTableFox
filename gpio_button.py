import RPi.GPIO as GPIO

# Button channels
BUTTON_1_CHANNEL = [4, 27, 23, 20, 16, 5]  # left buttons
BUTTON_2_CHANNEL = [17, 22, 24, 21, 26, 6]  # right buttons
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
    while i < len(BUTTON_1_CHANNEL):
        # add button channels with current seat
        seat_index = i + 1
        channel_b1 = BUTTON_1_CHANNEL[i]
        channel_b2 = BUTTON_2_CHANNEL[i]
        SEAT_IDX[channel_b1] = seat_index
        SEAT_IDX[channel_b2] = seat_index
        # add button channels with button index
        BUTTON_IDX[channel_b1] = BUTTON_IDX_LEFT
        BUTTON_IDX[channel_b2] = BUTTON_IDX_RIGHT
        # setup channels
        setup_button(channel_b1)
        setup_button(channel_b2)
        setup_button_interrupt(channel_b1)
        setup_button_interrupt(channel_b2)
        i += 1
