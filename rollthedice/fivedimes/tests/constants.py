import os
from pathlib import Path

TEST_DIRECTORY = Path(os.path.dirname(os.path.abspath(__file__)))
TEST_DATA_DIRECTORY = TEST_DIRECTORY / "data"
TEST_BET_THE_BOARD_FILE_PATH = TEST_DATA_DIRECTORY / "bet_the_board.html"