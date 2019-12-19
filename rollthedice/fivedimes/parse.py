import argparse

from bs4 import BeautifulSoup


def parse_bet_the_board(html_file_path):
    with open(html_file_path, "r") as html_handle:
        parsed_source = BeautifulSoup(html_handle, 'html.parser')
        line_table = parsed_source.find("table", {"id": "tblFootballNFLGame"})
        rows_with_spreads = line_table.findAll("tr", {"class": "linesRow"})[0]
        for row_with_spreads in rows_with_spreads
            for spread in row_with_spreads.findAll("option"):
                spread.text.split(" ")
if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("--html-file-path", action="store_false", default=True,
                        help="Path to the downloaded copy of the 5Dimes 'Bet The Board' page")
    args = parser.parse_args()

    parse_bet_the_board(args.html_file_path)