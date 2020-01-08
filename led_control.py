import gpio_button as button
import gpio_led as led
import websocket as web

COLOR_OFF = led.Color(0, 0, 0, 0)
COLOR_DEFAULT = led.Color(0, 0, 255, 0)
COLOR_ACTIVE = led.Color(0, 255, 0, 0)
COLOR_PASSED = led.Color(255, 146, 0, 0)
game_round = 0
START_SEAT = 0
ACTIVE_SEAT = 0
RUNNING = False


def lights_off():
    led.set_color(color=COLOR_OFF)


def lights_on():
    led.set_color(color=COLOR_DEFAULT)
    if ACTIVE_SEAT > 0:
        led.set_seat_color(ACTIVE_SEAT, COLOR_ACTIVE)


def next_round():
    global game_round
    game_round += 1
    web.set_state("round_nr", game_round)


def button_pressed(seat_idx, button_idx):
    global START_SEAT, ACTIVE_SEAT, RUNNING
    if not RUNNING:
        return
    # check if this is the first round
    if START_SEAT == 0:
        START_SEAT = seat_idx
        ACTIVE_SEAT = seat_idx
        led.set_seat_color(ACTIVE_SEAT, COLOR_ACTIVE)
    # only continue if seat is viable for input
    elif seat_idx == ACTIVE_SEAT:
        if seat_idx == START_SEAT:
            next_round()
        ACTIVE_SEAT = seat_idx - 1
        if ACTIVE_SEAT < 1:
            ACTIVE_SEAT = 6
        led.set_seat_color(seat_idx, COLOR_DEFAULT)
        led.set_seat_color(ACTIVE_SEAT, COLOR_ACTIVE)
        # print ("{} {}".format(seat,button))


def play(value1, value2):
    global RUNNING
    RUNNING = True
    lights_on()


# while paused turn off lights and ignore button presses
def pause(value1, value2):
    global RUNNING
    RUNNING = False
    lights_off()


# turn off lights and shutdown raspberry pi
def shutdown(value1, value2):
    print("shutdown")


def seat(number, checked):
    button_pressed(int(number), checked)


CALLS = {
    "play": play,
    "pause": pause,
    "shutdown": shutdown,
    "seat": seat}


def consume(action, value1, value2):
    CALLS[action](value1, value2)


if __name__ == '__main__':
    button.init()
    led.init()
    button.register(button_pressed)
    web.set_consumer(consume)
    web.init()
