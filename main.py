from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.chrome.options import Options
import time
from datetime import datetime
import os
import json

ignored_exceptions = (NoSuchElementException,StaleElementReferenceException,)


def driver_wait(xpath, ie=ignored_exceptions, time = 10):

    # wait for element to load in DOM
    return WebDriverWait(driver, time, ignored_exceptions = ie)\
                    .until(expected_conditions.presence_of_element_located((By.XPATH, 
                                                                            xpath)))

def webpage_start():
    driver.execute_script("window.scrollTo(0, 200)") 

    # zoom out
    time.sleep(1)
    for i in range(2):
        driver_wait('//*[@id="map_canvas"]/div/div/div[12]/div/div[2]/div/button[2]').click()

    # wait for points to be initialised
    time.sleep(5)
    while True:
        try:
            get_points()
            time.sleep(30)
        except (TimeoutException,StaleElementReferenceException) as e:
            print(f"[INFO] {e}, refreshing webpage....")
            driver.refresh()
            webpage_start()
            time.sleep(10)

def get_points():
    json_lst = []
    points = driver.find_element_by_xpath('//*[@id="map_canvas"]/div/div/div[1]/div[3]/div/div[1]')
    points_lst = points.find_elements_by_xpath('div')[:-1]

    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print('\n')
    print(f"{dt_string}: Total of {len(points_lst)} lightning points")	
    
    # for txt in lig_text:
    #     print(txt.text)

    for i, point in enumerate(points_lst):
        
        # try:
        parsed = point.get_attribute('style').split('; ')
        status = 200
            # point.click()
            # time.sleep(0.3)
            # lig_text = driver_wait('//*[@id="testID"]').text.replace('\n',', ')
            # driver_wait('//*[@id="map_canvas"]/div/div/div[1]/div[3]/div/div[4]/div/div/div/div/button').click()
        # except (ElementNotInteractableException, NoSuchElementException) as e:
            # lig_text = e

        left = parsed[-2].split(': ')[1].replace('px', '')
        top = parsed[-1].split(': ')[1].replace('px;', '')
        json_lst.append({'node': i, 'status': status, 'date': dt_string, 'left': float(left), 'top': float(top)})
    
    print(json_lst)
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(json_lst, f, ensure_ascii=False, indent=4)

opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36")
opts.add_argument("--start-maximized")

path_driver = f"{os.getcwd()}/chromedriver_linux64/chromedriver"

driver = webdriver.Chrome(options = opts,
                          executable_path = path_driver)

link = 'http://www.weather.gov.sg/lightning/lightning/lightningalertinformationsystem.jsp'
print(f'[INFO] Getting lightning data...')
driver.get(link)
webpage_start()


