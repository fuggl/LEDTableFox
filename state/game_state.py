import random

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
seats_passed = []
seat_order = []


def is_running():
    return status == STATUS_RUNNING


def is_paused():
    return status == STATUS_PAUSED


def is_stopped():
    return status == STATUS_STOPPED


def has_active_seat():
    return active_seat > 0


def seat_is_active(seat):
    return seat == active_seat


def seat_has_passed(seat):
    return seats[seat] == SEAT_PASSED


def player_count():
    return len(seats)


def waiting_for_start():
    return game_round == 0 and action_round == 0


def randomize_start_seat():
    global start_seat
    start_seat = seats[random.randint(0, len(seats)-1)]


def start(active_seats, random_starting_player):
    global game_round, action_round, seats, active_seat
    game_round = 1
    action_round = 1
    index = 0
    for active in active_seats:
        if active:
            seats[index + 1] = SEAT_WAITING
        index += 1
    if random_starting_player:
        randomize_start_seat()
        active_seat = start_seat


def set_status(new_status):
    global status
    status = new_status


def next_round():
    global game_round
    game_round += 1


def next_player(seat):
    return  # TODO: next


def pass_player(seat):
    global seats_passed
    seats_passed[seat] = SEAT_PASSED


def undo_pass(seat):
    global seats_passed
    seats_passed[seat] = SEAT_WAITING


def reset():
    global game_round, action_round, start_seat, active_seat, seats, seat_order
    game_round = 0
    action_round = 0
    start_seat = 0
    active_seat = 0
    seats.clear()
    seat_order.clear()


def update(setter):
    setter("status", status)
    setter("game_round", game_round)
    setter("action_round", action_round)
    setter("start_seat", start_seat)
    setter("active_seat", active_seat)
