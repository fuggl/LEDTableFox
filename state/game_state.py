import random

from state import settings_state as settings

STATUS_RUNNING = 0
STATUS_PAUSED = 1
STATUS_STOPPED = 2

status = STATUS_STOPPED
game_round = 0
action_round = 0
start_seat = 0
active_seat = 0

SEAT_WAITING = 0
SEAT_PASSED = 1
seats = {}
seat_order = []
seat_order_pass = []
pass_order = []
last_seat_to_pass_index = 0


def next_entry(a_list, entry):
    if entry in a_list:
        new_index = a_list.index(entry) + 1
    else:
        new_index = last_seat_to_pass_index
    if new_index == len(a_list):
        new_index = 0
    return a_list[new_index]


def is_running():
    return status == STATUS_RUNNING


def is_paused():
    return status == STATUS_PAUSED


def is_stopped():
    return status == STATUS_STOPPED


def order_is_complete():
    return len(seat_order) == player_count()


def has_active_seat():
    return active_seat > 0


def seat_is_active(seat):
    return seat == active_seat


def seat_has_passed(seat):
    return seats[seat] == SEAT_PASSED


def active_player_is_last():
    return order_is_complete() and (len(seat_order_pass) == 0 or active_seat == seat_order_pass[-1])


def player_count():
    return len(seats)


def passed_player_count():
    return len(pass_order)


def all_players_passed():
    return passed_player_count() == player_count()


def waiting_for_start():
    return game_round == 0 and action_round == 0


def reset_start_seat():
    global start_seat
    start_seat = 0


def rotate_start_seat():
    global start_seat
    start_seat = next_entry(seat_order, start_seat)


def randomize_start_seat():
    global start_seat
    start_seat = random.choice(list(seats.keys()))


def start():
    global game_round, action_round, seats, active_seat
    game_round = 1
    action_round = 1
    index = 0
    for active in settings.used_seats:
        if active:
            seats[index + 1] = SEAT_WAITING
        index += 1
    if settings.starting_player_first_round_is_random():
        randomize_start_seat()
        active_seat = start_seat
        add_seat_to_order(active_seat)


def set_status(new_status):
    global status
    status = new_status


def reset_order():
    global last_seat_to_pass_index
    seat_order.clear()
    seat_order_pass.clear()
    pass_order.clear()
    last_seat_to_pass_index = 0


def choose_starting_seat():
    if settings.starting_player_consecutive_rounds_is_rotating():
        rotate_start_seat()
    elif settings.starting_player_consecutive_rounds_is_first_to_input():
        reset_start_seat()
    elif settings.starting_player_consecutive_rounds_is_random():
        randomize_start_seat()


def add_seat_to_order(seat):
    seat_order.append(seat)
    seat_order_pass.append(seat)


def next_action_round():
    global action_round, active_seat
    action_round += 1
    if len(seat_order_pass) > 0:
        active_seat = seat_order_pass[0]
    else:
        active_seat = 0


def next_game_round():
    global game_round, action_round, active_seat
    game_round += 1
    action_round = 1
    reset_order()
    active_seat = 0
    choose_starting_seat()
    if start_seat > 0:
        active_seat = start_seat


def create_order_clockwise():
    global seat_order_pass
    seat_order.clear()
    i = start_seat - 1
    length = len(settings.used_seats)
    for x in range(length):
        if settings.used_seats[i]:
            add_seat_to_order(i + 1)
            i -= 1
            if i < 0:
                i = length - 1
    # seat_order_pass = seat_order.copy()


def create_order_counterclockwise():
    global seat_order_pass
    seat_order.clear()
    i = start_seat - 1
    length = len(settings.used_seats)
    for x in range(length):
        if settings.used_seats[i]:
            add_seat_to_order(i + 1)
            i += 1
            if i >= length:
                i = 0
    # seat_order_pass = seat_order.copy()


def create_first_turn_order():
    if settings.game_round_first_turn_order_is_clockwise():
        create_order_clockwise()
    elif settings.game_round_first_turn_order_is_counterclockwise():
        create_order_counterclockwise()


def create_reversed_turn_order():
    if settings.game_round_first_turn_order_is_clockwise():
        create_order_counterclockwise()
    elif settings.game_round_first_turn_order_is_counterclockwise():
        create_order_clockwise()
    else:
        seat_order.reverse()


def create_consecutive_turn_order():
    if settings.game_round_consecutive_turn_order_is_same():
        create_first_turn_order()
    elif settings.game_round_consecutive_turn_order_is_reverse():
        create_reversed_turn_order()


def action_round_end_condition_is_met():
    return active_player_is_last()


def game_round_end_condition_is_met():
    if settings.game_round_end_condition_is_pass():
        if all_players_passed():
            return True
    else:
        if action_round > settings.game_round_end_condition:
            return True
    return False


def start_of_round(seat):
    global start_seat, active_seat
    start_seat = seat
    active_seat = seat
    add_seat_to_order(seat)
    if game_round == 1:
        create_first_turn_order()
    else:
        create_consecutive_turn_order()


def get_next_seat():
    return next_entry(seat_order_pass, active_seat)


def end_of_player_turn():
    global active_seat
    if order_is_complete():
        no_round_switch = True
        # count up action round if over
        if action_round_end_condition_is_met():
            next_action_round()
            no_round_switch = False
        # count up game round if over
        if game_round_end_condition_is_met():
            next_game_round()
            no_round_switch = False
        if no_round_switch:
            active_seat = get_next_seat()
    else:
        active_seat = 0


def next_player(seat):
    print("next: {}".format(seat))
    global start_seat, active_seat
    # there is no starting player -> start of action round
    if start_seat == 0:
        start_of_round(seat)
    else:
        # there is no active seat -> specific turn order, no end of player turn
        if not has_active_seat():
            # only react if seat has not already had a turn
            if seat not in seat_order:
                add_seat_to_order(seat)
                active_seat = seat
        # end of player turn at active seat
        else:
            end_of_player_turn()


def pass_player(seat):
    print("pass: {}".format(str(seat_order_pass)))
    global seats, pass_order, last_seat_to_pass_index
    if seats[seat] != SEAT_PASSED:
        seats[seat] = SEAT_PASSED
        last_seat_to_pass_index = seat_order_pass.index(seat)
        pass_order.append(seat)
        seat_order_pass.remove(seat)
    print("pass: {}".format(str(seat_order_pass)))


def undo_pass(seat):
    global seats, pass_order
    if passed_player_count() > 0 and seat == pass_order[-1]:
        seats[seat] = SEAT_WAITING
        seat_order_pass.insert(last_seat_to_pass_index, seat)
        pass_order.remove(seat)


def reset():
    global game_round, action_round, start_seat, active_seat,\
        seats, seat_order, last_seat_to_pass_index, pass_order
    game_round = 0
    action_round = 0
    reset_start_seat()
    active_seat = 0
    seats.clear()
    seat_order.clear()
    seat_order_pass.clear()
    last_seat_to_pass_index = 0
    pass_order.clear()


def update(setter):
    setter("seat_order", str(seat_order).strip('[]'))
    setter("status", status)
    setter("game_round", game_round)
    setter("action_round", action_round)
    setter("start_seat", start_seat)
    setter("active_seat", active_seat)
