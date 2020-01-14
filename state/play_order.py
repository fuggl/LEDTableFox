import random

PLAYER_WAITING = 0
PLAYER_PASSED = 1
player_state = {}  # {player seat: state}

player_order = []
active_player_index = -1

player_pass_order = []


# ==== info
# == info: starting player
def has_starting_player():
    return len(player_order) > 0


def starting_player_seat():
    if has_starting_player():
        return player_order[0]
    return 0


def is_starting_player(player_seat):
    return player_seat == starting_player_seat()


# == info: active player
def has_active_player():
    return active_player_index >= 0


def active_player_seat():
    if has_active_player():
        return player_order[active_player_index]
    return 0


def is_active_player(player_seat):
    return player_seat == active_player_seat()


def random_player_seat():
    return random.choice(list(player_state.keys()))


# == info: player
def player_count():
    return len(player_state)


# == player order
def player_is_in_order(player_seat):
    return player_seat in player_order


def player_order_is_complete():
    return len(player_order) == player_count()


# == info: passing
def player_has_passed(player_seat):
    return player_state[player_seat] == PLAYER_PASSED


def player_passed_count():
    return len(player_pass_order)


def every_player_has_passed():
    return player_passed_count() == player_count()


# ==== setters
# == setters: init
def init_player_state(seat_use):
    player_seat = 0
    for used in seat_use:
        player_seat += 1
        if used:
            player_state[player_seat] = PLAYER_WAITING


# == setters: reset
def reset_pass_order():
    player_pass_order.clear()


def reset():
    global active_player_index
    active_player_index = -1
    player_order.clear()


# == setters: player
def add_player(player_seat):
    global active_player_index
    active_player_index = len(player_order)
    player_order.append(player_seat)


def cycle_player():
    global active_player_index
    if player_order_is_complete():
        active_player_index += 1
        if active_player_index >= len(player_order):
            active_player_index = 0
    else:
        active_player_index = -1


# ==== passing
def pass_active_player():
    player_seat = player_order[active_player_index]
    player_state[player_seat] = PLAYER_PASSED
    player_pass_order.append(player_seat)


def undo_pass(player_seat):
    player_state[player_seat] = PLAYER_WAITING
    player_pass_order.remove(player_seat)


# ==== starting player
def same_stating_player():
    old_starting_player_seat = starting_player_seat()
    reset()
    add_player(old_starting_player_seat)


def rotating_starting_player():
    new_starting_player_seat = player_order[1]
    reset()
    add_player(new_starting_player_seat)


def random_starting_player():
    reset()
    add_player(random_player_seat())


# ==== order
def roll_order(reference_list):
    index = reference_list.index(starting_player_seat())
    size = len(reference_list)
    for x in range(size - 1):  # -1 for starting player, who is already in order
        index += 1
        if index == size:
            index = 0
        player_order.append(reference_list[index])


def clockwise():
    if has_starting_player():
        keys = list(player_state.keys())
        keys.reverse()
        roll_order(keys)


def counterclockwise():
    if has_starting_player():
        keys = list(player_state.keys())
        roll_order(keys)


def pass_fifo():
    global player_order
    player_order = player_pass_order.copy()


def pass_lifo():
    global player_order
    player_order = player_pass_order.copy()
    player_order.reverse()
