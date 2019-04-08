#/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from kiteconnect import KiteConnect
import requests
import time
import base64
import pickle
import sys

route="https://"+str(sys.argv[1])
pluginPath=str(sys.argv[2])
options = Options()
options.headless = False
browser = webdriver.Chrome(chrome_options=options)

browser.get(route)
xpath = {
    'loginWithOpenshift':'/html/body/div/div[2]/a',
    'openshiftLogin' : {
        'username': '//*[@id="inputUsername"]',
        'password': '//*[@id="inputPassword"]',
        'login': '/html/body/div/div/div[2]/form/div[3]/div[2]/button'
    },
    'pluginFileInput':'//*[@id="pluginsAdv"]/tbody/tr/td/form[2]/table/tbody/tr[2]/td/input',
    'uploadPlugin':'//*[@id="yui-gen8"]',
    'restartJenkins': '//*[@id="scheduleRestartCheckbox"]'
}

# Select Login with Openshift
browser.find_element_by_xpath(xpath['loginWithOpenshift']).click()

# Insert Username and Password
username = browser.find_element_by_xpath(xpath['openshiftLogin']['username'])
username.clear()
username.send_keys('admin')

password = browser.find_element_by_xpath(xpath['openshiftLogin']['password'])
password.clear()
password.send_keys('redhat')

# Login 
browser.find_element_by_xpath(xpath['openshiftLogin']['login']).click()

# Goto Advanced Setting for Manage Plugins and enter the plugin path
browser.get(route+'/pluginManager/advanced')
inputPlugin = browser.find_element_by_name('name')
inputPlugin.send_keys(pluginPath)

uploadButton = browser.find_element_by_xpath(xpath['uploadPlugin'])
uploadButton.click()

restart = browser.find_element_by_xpath(xpath['restartJenkins'])
restart.click()

# Close Browser
browser.close()
