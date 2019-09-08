import datetime
import filecmp
import json
import logging
import os
import re
import time

import boto3
from bs4 import BeautifulSoup

from rollthedice.action_network import (ACTION_DATA_BUCKET_NAME, ACTION_DATA_S3_KEY, handler)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# add the handlers to the logger
logger.addHandler(handler)
from rollthedice.action_network import DATA_PATH





def load_password_file(password_file_path=".action"):
    with open(password_file_path, 'r') as handle:
        line = handle.readline()
        username, password = line.split(",")

    return username, password


def login_to_action_network(chrome_driver, password_file_path=".action"):
    # If can't find creds in environment (e.g., via AWS lambda) try to load them
    # from a local password file

    if "ACTION_USERNAME" not in os.environ or "ACTION_PASSWORD" not in os.environ:
        username, password = load_password_file(password_file_path=password_file_path)
    else:
        username = os.environ["ACTION_USERNAME"]
        password = os.environ["ACTION_PASSWORD"]

    chrome_driver.get("https://www.actionnetwork.com")
    if chrome_driver.page_source.find("text-success mr-2 fz-2 font-weight-bold") != -1:
        logger.info("Already logged in.")
        return chrome_driver
    else:

        chrome_driver.get('https://www.actionnetwork.com/login')

        email_field = chrome_driver.find_elements_by_xpath("//input[@name='email']")[0]
        email_field.send_keys(username)

        password_field = chrome_driver.find_elements_by_xpath("//input[@name='password']")[0]
        password_field.send_keys(password)

        submit_button = chrome_driver.find_elements_by_xpath("//button[text()='Sign In']")[0]
        submit_button.click()
        time.sleep(5)

    return chrome_driver


def parse_next_data(chrome_driver, sport_type, page_type):
    chrome_driver.get("https://www.actionnetwork.com/{}/{}/".format(sport_type, page_type))
    parsed_source = BeautifulSoup(chrome_driver.page_source, 'html.parser')
    data_dump = [i for i in parsed_source.find_all("script") if "__NEXT_DATA__" in i.text][0].text
    data_dump = data_dump[data_dump.find("{"):data_dump.rfind("[]}") + 3]

    data_dump_json = json.loads(data_dump)

    check_for_new_data(data_dump_json, page_type, sport_type)



def ordered(obj):
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)
    else:
        return obj


def get_latest_s3_data(page_type, sport_type, s3_client=None):
    if s3_client is None:
        s3_client = boto3.client('s3')

    data_regex = re.compile(".*_{}_{}.json".format(sport_type, page_type))

    json_files = s3_client.list_objects(Bucket=ACTION_DATA_BUCKET_NAME, Prefix=ACTION_DATA_S3_KEY)
    if "Contents" not in json_files:
        return {}

    json_files = json_files["Contents"]

    json_files = [json_file["Key"] for json_file in json_files if re.match(data_regex, json_file["Key"])]

    if len(json_files) != 0:
        json_files = sorted(json_files)
        latest_json_file = json_files[-1]
        s3_object = s3_client.get_object(Bucket=ACTION_DATA_BUCKET_NAME, Key=latest_json_file)
        latest_json_dict = json.loads(s3_object["Body"].read().decode('utf-8'))
    else:
        latest_json_dict = {}

    return latest_json_dict


def check_for_new_data(new_json, page_type, sport_type):
    latest_json_dict = get_latest_s3_data(page_type, sport_type)
    temp_json_path = os.path.join(DATA_PATH, "temp_{}_{}.json".format(sport_type, page_type))
    latest_json_path = os.path.join(DATA_PATH, "latest_{}_{}.json".format(sport_type, page_type))

    latest_json_string = json.dumps(latest_json_dict, sort_keys=True)

    temp_json_string = json.dumps(new_json, sort_keys=True)

    # with open(latest_json_path, 'w') as handle:
    #     json.dump(latest_json_dict, handle, sort_keys=True)
    #
    # with open(temp_json_path, 'w') as handle:
    #     json.dump(new_json, handle, sort_keys=True)

    # if filecmp.cmp(temp_json_path, latest_json_path):
    if latest_json_string == temp_json_string:
        logger.info(
                "Latest data dump for {} from the {} page match previously downloaded data. Skipping.".format(
                        sport_type,
                        page_type))
        return False
    else:

        datestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        new_json_path = os.path.join(DATA_PATH, "{}_{}_{}.json".format(datestamp, sport_type, page_type))
        logger.info("New JSON file for page {} from {}".format(page_type, sport_type))
        s3_client = boto3.client('s3')
        key = os.path.join(ACTION_DATA_S3_KEY, os.path.basename(new_json_path))
        s3_client.put_object(Body=json.dumps(new_json), Bucket=ACTION_DATA_BUCKET_NAME, Key=key)

        # # Dump locally as well. Useful for debugging
        # with open(new_json_path, 'w') as handle:
        #     json.dump(new_json, handle, sort_keys=True)
        return True
        # return new_json_path
