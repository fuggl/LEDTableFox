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


def toggle_seat_active(seat_number):
    global active_seats
    index = seat_number - 1
    active_seats[index] = not active_seats[index]


def starting_player_first_round_is_first_to_input():
    return starting_player_first_round == STARTING_PLAYER_FR_FIRST_INPUT


def starting_player_first_round_is_random():
    return starting_player_first_round == STARTING_PLAYER_FR_RANDOM


def starting_player_consecutive_rounds_is_same_as_before():
    return starting_player_consecutive_rounds == STARTING_PLAYER_CR_SAME


def starting_player_consecutive_rounds_is_rotating():
    return starting_player_consecutive_rounds == STARTING_PLAYER_CR_ROTATING


def starting_player_consecutive_rounds_is_first_to_input():
    return starting_player_consecutive_rounds == STARTING_PLAYER_CR_FIRST_INPUT


def starting_player_consecutive_rounds_is_random():
    return starting_player_consecutive_rounds == STARTING_PLAYER_CR_RANDOM


def game_round_first_turn_order_is_clockwise():
    return game_round_first_turn_order == GAME_ROUND_FTO_CLOCKWISE


def game_round_first_turn_order_is_counterclockwise():
    return game_round_first_turn_order == GAME_ROUND_FTO_COUNTERCLOCKWISE


def game_round_first_turn_order_is_specific():
    return game_round_first_turn_order == GAME_ROUND_FTO_SPECIFIC


def game_round_end_condition_is_pass():
    return game_round_end_condition == GAME_ROUND_EC_PASS


def game_round_consecutive_turn_order_is_same():
    return game_round_consecutive_turn_order == GAME_ROUND_CTO_SAME


def game_round_consecutive_turn_order_is_reverse():
    return game_round_consecutive_turn_order == GAME_ROUND_CTO_REVERSE


def game_round_consecutive_turn_order_is_specific():
    return game_round_consecutive_turn_order == GAME_ROUND_CTO_SPECIFIC


def game_round_consecutive_turn_order_is_pass_order_fifo():
    return game_round_consecutive_turn_order == GAME_ROUND_CTO_PASS_FIFO


def game_round_consecutive_turn_order_is_pass_order_lifo():
    return game_round_consecutive_turn_order == GAME_ROUND_CTO_PASS_LIFO


def update(setter):
    setter("active_seats", active_seats)
    setter("starting_player_first_round", starting_player_first_round)
    setter("starting_player_consecutive_rounds", starting_player_consecutive_rounds)
    setter("game_round_first_turn_order", game_round_first_turn_order)
    setter("game_round_end_condition", game_round_end_condition)
    setter("game_round_consecutive_turn_order", game_round_consecutive_turn_order)
