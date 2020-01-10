import sys

from gpio import led_test as led, button_test as button
from connect import websocket as web
from state import settings_state as settings, game_state as game

COLOR_OFF = led.Color(0, 0, 0, 0)
COLOR_DEFAULT = led.Color(0, 0, 255, 0)
COLOR_ACTIVE = led.Color(0, 255, 0, 0)
COLOR_PASSED = led.Color(255, 146, 0, 0)


def ignore(value):
    return value


def update_game_state():
    game.update(web.set_state)


def update_settings_state():
    settings.update(web.set_state)


def show_active_seat():
    if game.has_active_seat():
        led.set_seat_color(game.active_seat, COLOR_ACTIVE)


def lights_on():
    for player_seat in game.seats:
        if game.seat_has_passed(player_seat):
            led.set_seat_color(player_seat, COLOR_PASSED, show=False)
        elif game.seat_is_active(player_seat):
            led.set_seat_color(player_seat, COLOR_ACTIVE, show=False)
        else:
            led.set_seat_color(player_seat, COLOR_DEFAULT, show=False)
    led.show_changes()


def lights_off():
    led.set_color(color=COLOR_OFF)


def player_next(invoker_seat):
    game.next_player(invoker_seat)
    # set invoker color to default if player is not active after button press
    if not game.seat_is_active(invoker_seat):
        led.set_seat_color(invoker_seat, COLOR_DEFAULT)
    show_active_seat()
    update_game_state()


def player_pass(invoker_seat):
    # pass pressed by active player -> pass and next
    if game.seat_is_active(invoker_seat):
        game.pass_player(invoker_seat)
        game.next_player(invoker_seat)
        led.set_seat_color(invoker_seat, COLOR_PASSED)
        show_active_seat()
    # pass pressed by inactive player -> undo pass or ignore
    else:
        game.undo_pass(invoker_seat)
        led.set_seat_color(invoker_seat, COLOR_DEFAULT)
    update_game_state()


def button_pressed(seat_number, button_idx):
    # ignore if game is paused or stopped, or pressed button belongs to inactive seat
    if game.is_running() and settings.seat_is_active(seat_number):
        # pass functionality: pass button is pressed and game supports pass
        if button_idx > 1 and settings.game_round_end_condition_is_pass():
            player_pass(seat_number)
        # next functionality: pass functionality not used and seat belongs to active player
        elif game.seat_is_active(seat_number):
            player_next(seat_number)


# ==== web calls ---- game state
def play(value1, value2):
    print("play {} {}".format(value1, value2))
    if game.waiting_for_start():
        game.start(settings.active_seats, settings.starting_player_first_round_is_random())
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
    ignore(value2)
    if game.is_stopped():
        settings.toggle_seat_active(int(number))
        update_settings_state()


def starting_player_fr(value1, value2):
    ignore(value2)
    if game.is_stopped():
        settings.starting_player_first_round = value1
        update_settings_state()


def starting_player_cr(value1, value2):
    ignore(value2)
    if game.game_round < 2:
        settings.starting_player_consecutive_rounds = value1
        update_settings_state()


def game_round_fto(value1, value2):
    ignore(value2)
    if game.is_stopped():
        settings.game_round_first_turn_order = value1
        update_settings_state()


def game_round_ec(value1, value2):
    ignore(value2)
    if game.is_stopped():
        settings.game_round_end_condition = value1
        update_settings_state()


def game_round_cto(value1, value2):
    ignore(value2)
    if game.game_round < 2:
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
