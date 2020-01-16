from state import play_order as order
from state import settings_state as settings

STATUS_RUNNING = 0
STATUS_PAUSED = 1
STATUS_STOPPED = 2

status = STATUS_STOPPED
action_round = 0
game_round = 0


def do_nothing():
    return


# ==== starting player
first_round_starting_player = {
    settings.STARTING_PLAYER_FR_FIRST_INPUT: order.reset_player_order,
    settings.STARTING_PLAYER_FR_RANDOM: order.random_starting_player
}
consecutive_round_starting_player = {
    settings.STARTING_PLAYER_CR_SAME: order.same_stating_player,
    settings.STARTING_PLAYER_CR_ROTATING: order.rotating_starting_player,
    settings.STARTING_PLAYER_CR_FIRST_INPUT: order.reset_player_order,
    settings.STARTING_PLAYER_CR_RANDOM: order.random_starting_player
}


# ==== round order
def same_order():
    first_round_order[settings.game_round_first_turn_order]()


def reverse_order():
    return


first_round_order = {
    settings.GAME_ROUND_FTO_CLOCKWISE: order.clockwise,
    settings.GAME_ROUND_FTO_COUNTERCLOCKWISE: order.counterclockwise,
    settings.GAME_ROUND_FTO_SPECIFIC: do_nothing
}
consecutive_round_order = {
    settings.GAME_ROUND_CTO_SAME: same_order,
    settings.GAME_ROUND_CTO_REVERSE: reverse_order,
    settings.GAME_ROUND_CTO_SPECIFIC: do_nothing,
    settings.GAME_ROUND_CTO_PASS_FIFO: order.pass_fifo,
    settings.GAME_ROUND_CTO_PASS_LIFO: order.pass_lifo
}


# ==== info
# == info: status
def is_running():
    return status == STATUS_RUNNING


def is_paused():
    return status == STATUS_PAUSED


def is_stopped():
    return status == STATUS_STOPPED


def waiting_for_start():
    return game_round == 0 and action_round == 0


# == info: rounds
def is_first_game_round():
    return game_round == 1


# ==== setters
# == setters: status
def set_status(new_status):
    global status
    status = new_status


# == setters: rounds
def increment_action_round():
    global action_round
    action_round += 1
    order.reset_player_turn_counter()


def increment_game_round():
    global game_round, action_round
    game_round += 1
    action_round = 1


def action_round_end_condition_is_met():
    return order.player_turn_count() == order.player_count()


def game_round_end_condition_is_met():
    if settings.game_round_end_condition_is_pass():
        return order.every_player_has_passed()
    else:
        return action_round > settings.game_round_end_condition


# ==== button press handling
def choose_starting_player():
    consecutive_round_starting_player[settings.starting_player_consecutive_rounds]()


def choose_order():
    if is_first_game_round():
        first_round_order[settings.game_round_first_turn_order]()
    else:
        consecutive_round_order[settings.game_round_consecutive_turn_order]()
    order.reset_pass()
    order.reset_player_turn_counter()


def end_active_player_turn():
    order.increment_player_turn_counter()
    if not order.every_player_has_passed():
        order.cycle_player()
        while order.player_has_passed(order.active_player_seat()):
            order.cycle_player()
    if action_round_end_condition_is_met():
        increment_action_round()
    if game_round_end_condition_is_met():
        increment_game_round()
        choose_starting_player()
        choose_order()


def finish_order_if_one_player_left():
    if order.players_missing() == 1:
        for player_seat in order.player_state.keys():
            if not order.player_is_in_order(player_seat):
                order.add_player(player_seat)
                return


def add_player_to_order(player_seat):
    if not order.has_starting_player():
        order.add_active_player(player_seat)
        choose_order()
        finish_order_if_one_player_left()
    elif not order.player_is_in_order(player_seat):
        order.add_active_player(player_seat)
        finish_order_if_one_player_left()


def start():
    order.init_player_state(settings.seat_use)
    increment_game_round()
    first_round_starting_player[settings.starting_player_first_round]()
    choose_order()


def next_button(player_seat):
    if order.is_active_player(player_seat):
        end_active_player_turn()
    elif not order.has_active_player():
        add_player_to_order(player_seat)


def pass_button(player_seat):
    if settings.game_round_end_condition_is_pass():
        if order.is_active_player(player_seat):
            order.pass_active_player()
            next_button(player_seat)
        elif order.player_has_passed(player_seat):
            order.undo_pass(player_seat)
    else:
        next_button(player_seat)


def reset():
    global game_round, action_round
    game_round = 0
    action_round = 0
    order.reset()


def update(setter):
    setter("seat_order", str(order.player_order).strip('[]'))
    setter("pass_order", str(order.player_pass_order).strip('[]'))
    setter("status", status)
    setter("game_round", game_round)
    setter("action_round", action_round)
    setter("start_seat", order.starting_player_seat())
    setter("active_seat", order.active_player_seat())
