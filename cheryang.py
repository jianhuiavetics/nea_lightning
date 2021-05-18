from multiprocessing.queues import Queue
from multiprocessing.spawn import freeze_support
import string
from flask import Flask
from flask import Request
import threading
from multiprocessing import Process, Value, Queue
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from enum import Enum, auto
from pyproj import Proj
import requests
import json
import time
import math


#pls rename this file to main.py
CGJson = None
def obtainLightningData():
    try:
        driver.execute_script('window.location.reload()')
        time.sleep(5)
        typelist = driver.execute_script("return lsResult")
        if (typelist != None):
            length_ = driver.execute_script("return lsResult.length")
            for i in range(length_):
                lat = typelist[i]['latitude']
                lng = typelist[i]['longitude']
                #print(lat, lng)
                Northing,Easting = myProj(lng, lat)
                Northing,Easting = int(Northing), int(Easting)
                #print(Northing, Easting)
                typelist[i]['latitude'] = Easting
                typelist[i]['longitude'] = Northing
        CGjson = json.dumps(typelist)
        #print(CGjson)
        return CGjson
    except:
        print("lightning is undefined")
        driver.execute_script('window.location.reload()')
        #obtainLightningData()

myProj = Proj("+proj=utm +zone=48N, +north +ellps=WGS84 +datum=WGS84 +units=m +no_defs")
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
driver = webdriver.Chrome(executable_path = '/Users/avetics/Downloads/chromedriver', options = chrome_options)

def run_(json1):
    driver.get("http://www.weather.gov.sg/lightning/lightning/lightningalertinformationsystem.jsp")
    print(driver.title)
    time.sleep(5)
    while(True):
        json1.put(obtainLightningData())
        time.sleep(3)


app = Flask(__name__)

@app.route("/")
def home():  
    return "Hello"

@app.route("/json_example", methods=['GET', 'POST'])
def json_example():
    return json1.get()

if __name__ == "__main__":
    json1 = Queue()
    p = Process(target=run_, args=(json1,))
    p.start()
    app.run(debug = False)
    p.join()
