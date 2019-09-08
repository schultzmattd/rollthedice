import argparse
import datetime
import logging
import os
import time

from daemon import daemon
from selenium import webdriver

from rollthedice.action_network import ACTION_DIRECTORY, SPORT_PAGES, handler
from rollthedice.action_network.utilities import login_to_action_network, parse_next_data

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# add the handlers to the logger
logger.addHandler(handler)

def create_chrome_driver(headless=True):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1280x1696')
    chrome_options.add_argument('--user-data-dir=/tmp/user-data')
    chrome_options.add_argument('--hide-scrollbars')
    chrome_options.add_argument('--enable-logging')
    chrome_options.add_argument('--log-level=0')
    chrome_options.add_argument('--v=99')
    chrome_options.add_argument('--single-process')
    chrome_options.add_argument('--data-path=/tmp/data-path')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--homedir=/tmp')
    chrome_options.add_argument('--disk-cache-dir=/tmp/cache-dir')
    chrome_options.add_argument(
        'user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 '
        'Safari/537.36')
    chrome_options.binary_location = os.getcwd() + "/bin/headless-chromium"
    chrome_options.add_argument("--test-type")
    if headless:
        chrome_options.add_argument("--headless")
    chrome_driver = webdriver.Chrome(chrome_options=chrome_options)
    return chrome_driver

def poll_action_network(headless=True):

    chrome_driver = create_chrome_driver(headless=headless)

    while True:
        poll_loop(chrome_driver)
        time.sleep(500)

    chrome_driver.close()


def lambda_poll_loop(event, context):
    poll_loop(chrome_driver=None, headless=True)

def poll_loop(chrome_driver=None,headless=True):
    if chrome_driver is None:
        chrome_driver = create_chrome_driver(headless=headless)
    logger.info("Starting poll loop")
    chrome_driver = login_to_action_network(chrome_driver, password_file_path=os.path.join(ACTION_DIRECTORY, ".action"))
    for sport_type in SPORT_PAGES.keys():
        for page_type in SPORT_PAGES[sport_type]:
            parse_next_data(chrome_driver=chrome_driver, sport_type=sport_type, page_type=page_type)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("--no-headless", action="store_false", default=True,
                        help="Whether or not to run Selenium in headless mode. Don't enable if debugging")
    args = parser.parse_args()
    datestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    with open(os.path.join(ACTION_DIRECTORY, "{}_stdout.txt".format(datestamp)), 'w') as stdout_log, \
            open(os.path.join(ACTION_DIRECTORY, "{}_stderr.txt".format(datestamp)), 'w') as stderr_log:
        with daemon.DaemonContext(stdout=stdout_log, stderr=stderr_log, uid=os.getuid(), gid=os.getgid()):
            poll_action_network(headless=args.no_headless)
