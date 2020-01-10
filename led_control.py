import sys

import gpio_button_test as button
import gpio_led_test as led
import websocket as web
import game_state as game
import settings_state as settings

COLOR_OFF = led.Color(0, 0, 0, 0)
COLOR_DEFAULT = led.Color(0, 0, 255, 0)
COLOR_ACTIVE = led.Color(0, 255, 0, 0)
COLOR_PASSED = led.Color(255, 146, 0, 0)


def update_game_state():
    game.update(web.set_state)


def update_settings_state():
    settings.update(web.set_state)


def lights_off():
    led.set_color(color=COLOR_OFF)


def lights_on():
    led.set_color(color=COLOR_DEFAULT)
    if active_seat > 0:
        led.set_seat_color(active_seat, COLOR_ACTIVE)


def first_input():
    return


def button_pressed(seat_idx, button_idx):
    if not game.is_running():
        return
    if not game.waiting_for_start():
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
            game.next_round()
        active_seat = seat_idx - 1
        if active_seat < 1:
            active_seat = 6
        led.set_seat_color(seat_idx, COLOR_DEFAULT)
        led.set_seat_color(active_seat, COLOR_ACTIVE)
        # print ("{} {}".format(seat,button))


# ==== web calls ---- game state
def play(value1, value2):
    print("play {} {}".format(value1, value2))
    if not game.is_running() and settings.starting_player_first_round_is_random():
        game.next_round()  # randomize start_seat
    lights_on()
    game.set_status(game.STATUS_RUNNING)
    update_game_state()


# while paused turn off lights and ignore button presses
def pause(value1, value2):
    print("pause {} {}".format(value1, value2))
    lights_off()
    game.set_status(game.STATUS_PAUSED)
    update_game_state()


def stop(value1, value2):
    print("stop {} {}".format(value1, value2))
    lights_off()
    game.reset()
    game.set_status(game.STATUS_STOPPED)
    update_game_state()


# turn off lights and shutdown raspberry pi
def shutdown(value1, value2):
    print("shutdown {} {}".format(value1, value2))
    sys.exit(0)


# ==== web calls ---- settings state
def seat(number, value2):
    settings.toggle_seat_active(int(number))
    update_settings_state()


def starting_player_fr(value1, value2):
    settings.starting_player_first_round = value1
    update_settings_state()


def starting_player_cr(value1, value2):
    settings.starting_player_consecutive_rounds = value1
    update_settings_state()


def game_round_fto(value1, value2):
    settings.game_round_first_turn_order = value1
    update_settings_state()


def game_round_ec(value1, value2):
    settings.game_round_end_condition = value1
    update_settings_state()


def game_round_cto(value1, value2):
    settings.game_round_consecutive_turn_order = value1
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
