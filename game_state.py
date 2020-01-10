STATUS_RUNNING = 0
STATUS_PAUSED = 1
STATUS_STOPPED = 2

status = STATUS_STOPPED
game_round = 0
action_round = 0
start_seat = 0
active_seat = 0


def is_running():
    return status == STATUS_RUNNING


def waiting_for_start():
    return game_round == 0 and action_round == 0


def set_status(new_status):
    global status
    status = new_status


def next_round():
    global game_round
    game_round += 1


def reset():
    global game_round, action_round, start_seat, active_seat
    game_round = 0
    action_round = 0
    start_seat = 0
    active_seat = 0
