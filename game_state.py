STATUS_RUNNING = 0
STATUS_PAUSED = 1
STATUS_STOPPED = 2

status = STATUS_STOPPED
game_round = 0
action_round = 0
start_seat = 0
active_seat = 0

seat_order = []


def is_running():
    return status == STATUS_RUNNING


def has_active_seat():
    return active_seat > 0


def seat_is_active(seat):
    return seat == active_seat


def waiting_for_start():
    return game_round == 0 and action_round == 0


def start():
    global game_round, action_round
    game_round = 1
    action_round = 1


def randomize_start_seat():
    global active_seat
    active_seat = 1  # TODO: randomize


def set_status(new_status):
    global status
    status = new_status


def next_round():
    global game_round
    game_round += 1


def pass_player(seat):
    return  # TODO: pass


def undo_pass(seat):
    return  # TODO: undo pass


def reset():
    global game_round, action_round, start_seat, active_seat
    game_round = 0
    action_round = 0
    start_seat = 0
    active_seat = 0


def update(setter):
    setter("status", status)
    setter("game_round", game_round)
    setter("action_round", action_round)
    setter("start_seat", start_seat)
    setter("active_seat", active_seat)
