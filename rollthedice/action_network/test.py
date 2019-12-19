import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.binary_location = os.getcwd() + "/bin/headless-chromium"

driver = webdriver.Chrome( chrome_options=options)
driver.get('https://github.com/')
print(driver.title)
driver.quit()
