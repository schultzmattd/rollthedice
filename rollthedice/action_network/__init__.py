import logging
import os

handler = logging.StreamHandler()

handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

ACTION_DIRECTORY = os.path.dirname(__file__)
ACTION_DATA_BUCKET_NAME = "action-network"
ACTION_DATA_S3_KEY = "data/"
ACTION_DATA_S3_URL = os.path.join("s3://", ACTION_DATA_BUCKET_NAME, ACTION_DATA_S3_KEY)

SPORT_PAGES = {
    "nfl"  :["live-odds", "public-betting", "sharp-report", "nfl-against-the-spread-standings"],
    "ncaaf":["live-odds", "public-betting", "sharp-report", "ncaaf-against-the-spread-standings"],
    "mlb"  :["live-odds", "public-betting", "sharp-report"],
    "nba"  :["live-odds", "public-betting", "sharp-report", "nba-against-the-spread-standings"],
    "nhl"  :["live-odds", "public-betting", "sharp-report"],
    "ncaab":["live-odds", "public-betting", "sharp-report", "ncaab-against-the-spread-standings"],
    "wnba" :["live-odds", "wnba-against-the-spread-standings"]
    }

DATA_PATH = os.path.join(ACTION_DIRECTORY, "data")
# if not os.path.exists(DATA_PATH):
#     os.mkdir(DATA_PATH)
