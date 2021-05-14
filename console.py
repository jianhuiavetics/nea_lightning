from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import JavascriptException
import time
import os
from datetime import datetime
import json
import requests

def get_datetime():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

    return dt_string

def get_lighting_strikes(driver):
    try:
        time.sleep(15)
        points = driver.execute_script('return lsResult')
        length = driver.execute_script('return lsResult.length')
    except JavascriptException as e:
        dt_string = get_datetime()
        print(f"[ERR]  {dt_string}: {e}")
        driver.execute_script('window.location.reload()')
        points, length = get_lighting_strikes(driver)

    return points, length

def main():
    opts = Options()
    opts.add_argument("--headless")
    opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36")
    path_driver = f"{os.getcwd()}/chromedriver_linux64/geckodriver"

    driver = webdriver.Chrome(options = opts, executable_path = path_driver)

    link = 'http://www.weather.gov.sg/lightning/lightning/lightningalertinformationsystem.jsp'
    print(f'[INFO] Getting lightning data...')
    driver.get(link)

    while True:
        points, length = get_lighting_strikes(driver)

        dt_string = get_datetime()
        print(f"[INFO] {dt_string}: {length} lightning strikes detected")

        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(points, f, ensure_ascii=False, indent=4)

        # r = requests.post('http://httpbin.org/post', json=points)
        time.sleep(45)
        driver.execute_script('window.location.reload()')

if __name__ == "__main__":
    main()