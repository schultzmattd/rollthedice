from rollthedice.fivedimes.parse import parse_bet_the_board
from rollthedice.fivedimes.tests.constants import TEST_BET_THE_BOARD_FILE_PATH

def test_parse_bet_the_board():
    result = parse_bet_the_board(TEST_BET_THE_BOARD_FILE_PATH)
