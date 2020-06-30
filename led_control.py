import asyncio
import sys
from subprocess import call

from connect import websocket as web
from gpio import led_test as led, button_test as button
from state import game_state as game

COLOR_OFF = led.Color(0, 0, 0, 0)
COLOR_SHUTDOWN = led.Color(0, 0, 0, 40)
COLOR_DEFAULT = led.Color(0, 0, 255, 0)
COLOR_ACTIVE = led.Color(0, 255, 0, 0)
COLOR_PASSED = led.Color(255, 146, 0, 0)

event_loop = None


def ignore(value):
    return value


def update_game_state():
    game.update(web.set_state)


def update_settings_state():
    game.settings.update(web.set_state)


def update_seat_color(player_seat, show):
    if game.order.player_has_passed(player_seat):
        led.set_seat_color(player_seat, COLOR_PASSED, show)
    elif game.order.is_active_player(player_seat):
        led.set_seat_color(player_seat, COLOR_ACTIVE, show)
    else:
        led.set_seat_color(player_seat, COLOR_DEFAULT, show)


def lights_on():
    for player_seat in game.order.player_state:
        update_seat_color(player_seat, show=False)
    led.show_changes()


def lights_off():
    led.set_color(color=COLOR_OFF)


def monitor_changes(player_seat, call_fct):
    game_round = game.game_round
    call_fct(player_seat)
    if game_round != game.game_round:
        lights_on()
    else:
        update_seat_color(player_seat, show=False)
        if game.order.has_active_player() and not game.order.is_active_player(player_seat):
            update_seat_color(game.order.active_player_seat(), show=False)
        led.show_changes()


def button_pressed(seat_number, button_idx):
    event_loop.call_soon_threadsafe(button_press, seat_number, button_idx)


# ==== web calls ---- game state
def play(value1, value2):
    print("play {} {}".format(value1, value2))
    if game.waiting_for_start():
        game.start()
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
    if game.is_stopped():
        print("shutdown {} {}".format(value1, value2))
        led.set_color(color=COLOR_SHUTDOWN)
        call("sudo shutdown -h 0", shell=True)
        sys.exit(0)


# ==== web calls ---- settings state
def seat(number, value2):
    ignore(value2)
    if game.is_stopped():
        game.settings.toggle_seat_used(int(number))
        update_settings_state()


def starting_player_fr(value1, value2):
    ignore(value2)
    if game.is_stopped():
        game.settings.starting_player_first_round = value1
        update_settings_state()


def starting_player_cr(value1, value2):
    ignore(value2)
    if game.game_round < 2:
        game.settings.starting_player_consecutive_rounds = value1
        update_settings_state()


def game_round_fto(value1, value2):
    ignore(value2)
    if game.is_stopped():
        game.settings.game_round_first_turn_order = value1
        update_settings_state()


def game_round_ec(value1, value2):
    ignore(value2)
    if game.is_stopped():
        game.settings.game_round_end_condition = int(value1)
        update_settings_state()


def game_round_cto(value1, value2):
    ignore(value2)
    if game.game_round < 2:
        game.settings.game_round_consecutive_turn_order = value1
        update_settings_state()


# ==== web calls ---- GPIO input
def button_press(value1, value2):
    seat_number = int(value1)
    button_idx = int(value2)
    if game.is_running() and game.settings.seat_is_in_use(seat_number):
        if button_idx == button.BUTTON_IDX_LEFT:
            monitor_changes(seat_number, game.next_button)
        else:
            monitor_changes(seat_number, game.pass_button)
    update_game_state()


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
    event_loop = asyncio.get_event_loop()
    button.init()
    led.init()
    button.register(button_pressed)
    web.set_consumer(consume)
    update_game_state()
    update_settings_state()
    web.init()
