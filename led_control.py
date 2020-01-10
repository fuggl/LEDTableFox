import sys

import gpio_button_test as button
import gpio_led_test as led
import websocket as web
import game_state

COLOR_OFF = led.Color(0, 0, 0, 0)
COLOR_DEFAULT = led.Color(0, 0, 255, 0)
COLOR_ACTIVE = led.Color(0, 255, 0, 0)
COLOR_PASSED = led.Color(255, 146, 0, 0)

active_seats = [True, True, True, True, True, True]

STARTING_PLAYER_FR_FIRST_INPUT = 0
STARTING_PLAYER_FR_RANDOM = 1
starting_player_first_round = STARTING_PLAYER_FR_FIRST_INPUT

STARTING_PLAYER_CR_SAME = 0
STARTING_PLAYER_CR_ROTATING = 1
STARTING_PLAYER_CR_FIRST_INPUT = 2
STARTING_PLAYER_CR_RANDOM = 3
starting_player_consecutive_rounds = STARTING_PLAYER_CR_SAME

GAME_ROUND_FTO_CLOCKWISE = 0
GAME_ROUND_FTO_COUNTERCLOCKWISE = 1
GAME_ROUND_FTO_SPECIFIC = 2
game_round_first_turn_order = GAME_ROUND_FTO_CLOCKWISE

GAME_ROUND_EC_PASS = 0
game_round_end_condition = 1  # >0: after n action rounds

GAME_ROUND_CTO_SAME = 0
GAME_ROUND_CTO_REVERSE = 1
GAME_ROUND_CTO_SPECIFIC = 2
GAME_ROUND_CTO_PASS_FIFO = 3
GAME_ROUND_CTO_PASS_LIFO = 4
game_round_consecutive_turn_order = GAME_ROUND_CTO_SAME


def update_game_state():
    web.set_state("status", game_state.status)
    web.set_state("game_round", game_state.game_round)
    web.set_state("action_round", game_state.action_round)
    web.set_state("start_seat", game_state.start_seat)
    web.set_state("active_seat", game_state.active_seat)


def update_settings_state():
    web.set_state("active_seats", active_seats)
    web.set_state("starting_player_first_round", starting_player_first_round)
    web.set_state("starting_player_consecutive_rounds", starting_player_consecutive_rounds)
    web.set_state("game_round_first_turn_order", game_round_first_turn_order)
    web.set_state("game_round_end_condition", game_round_end_condition)
    web.set_state("game_round_consecutive_turn_order", game_round_consecutive_turn_order)


def lights_off():
    led.set_color(color=COLOR_OFF)


def lights_on():
    led.set_color(color=COLOR_DEFAULT)
    if active_seat > 0:
        led.set_seat_color(active_seat, COLOR_ACTIVE)


def first_input():
    return


def button_pressed(seat_idx, button_idx):
    if not game_state.is_running():
        return
    if not game_state.waiting_for_start():
        first_input()
    #elif
    global start_seat, active_seat
    # check if this is the first round
    if start_seat == 0:
        start_seat = seat_idx
        active_seat = seat_idx
        led.set_seat_color(active_seat, COLOR_ACTIVE)
    # only continue if seat is viable for input
    elif seat_idx == active_seat:
        if seat_idx == start_seat:
            game_state.next_round()
        active_seat = seat_idx - 1
        if active_seat < 1:
            active_seat = 6
        led.set_seat_color(seat_idx, COLOR_DEFAULT)
        led.set_seat_color(active_seat, COLOR_ACTIVE)
        # print ("{} {}".format(seat,button))


# ==== web calls ---- game state
def play(value1, value2):
    print("play {} {}".format(value1, value2))
    if not game_state.is_running() and starting_player_first_round == STARTING_PLAYER_FR_RANDOM:
        game_state.next_round()  # randomize start_seat
    lights_on()
    game_state.set_status(game_state.STATUS_RUNNING)
    update_game_state()


# while paused turn off lights and ignore button presses
def pause(value1, value2):
    print("pause {} {}".format(value1, value2))
    lights_off()
    game_state.set_status(game_state.STATUS_PAUSED)
    update_game_state()


def stop(value1, value2):
    print("stop {} {}".format(value1, value2))
    lights_off()
    game_state.reset()
    game_state.set_status(game_state.STATUS_STOPPED)
    update_game_state()


# turn off lights and shutdown raspberry pi
def shutdown(value1, value2):
    print("shutdown {} {}".format(value1, value2))
    sys.exit(0)


# ==== web calls ---- settings state
def seat(number, value2):
    global active_seats
    index = int(number) - 1
    active_seats[index] = not active_seats[index]
    update_settings_state()


def starting_player_fr(value1, value2):
    global starting_player_first_round
    starting_player_first_round = value1
    update_settings_state()


def starting_player_cr(value1, value2):
    global starting_player_consecutive_rounds
    starting_player_consecutive_rounds = value1
    update_settings_state()


def game_round_fto(value1, value2):
    global game_round_first_turn_order
    game_round_first_turn_order = value1
    update_settings_state()


def game_round_ec(value1, value2):
    global game_round_end_condition
    game_round_end_condition = value1
    update_settings_state()


def game_round_cto(value1, value2):
    global game_round_consecutive_turn_order
    game_round_consecutive_turn_order = value1
    update_settings_state()


# ==== web calls ---- testing
def button_press(value1, value2):
    print("pressing button {}, {}".format(value1, value2))
    button_pressed(int(value1), value2)


CALLS = {
    "play": play,
    "pause": pause,
    "stop": stop,
    "shutdown": shutdown,
    "seat": seat,
    "starting_player_fr": starting_player_fr,
    "starting_player_cr": starting_player_cr,
    "game_round_fto": game_round_fto,
    "game_round_ec": game_round_ec,
    "game_round_cto": game_round_cto,
    "button_press": button_press
}


def consume(action, value1, value2):
    CALLS[action](value1, value2)


if __name__ == '__main__':
    button.init()
    led.init()
    button.register(button_pressed)
    web.set_consumer(consume)
    update_game_state()
    update_settings_state()
    web.init()
