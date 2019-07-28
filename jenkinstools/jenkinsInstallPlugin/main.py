#/usr/bin/env python

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import requests
import time
import base64
import pickle
import sys

class JIP:
    def __init__(self):
        # Get Jenkins Route
        self.route="https://"+str(sys.argv[1])
        # Get Path to the Plugin which has to be uploaded
        self.pluginPath=""
        # instantiate Webdriver
        options = Options()
        options.headless = False
        self.browser = webdriver.Chrome(chrome_options=options)
        # XPATHS for elements on the page
        self.xpaths = {
            'loginWithOpenshift':'/html/body/div/div[2]/a',
            'chooseUserOS4': '/html/body/div/div/div/a[1]',
            'openshiftLogin' : {
                'username': '//*[@id="inputUsername"]',
                'password': '//*[@id="inputPassword"]',
                'login': '/html/body/div/div/div[2]/form/div[3]/div[2]/button'
            },
            'pluginFileInput':'//*[@id="pluginsAdv"]/tbody/tr/td/form[2]/table/tbody/tr[2]/td/input',
            'uploadPlugin':'//button[text()="Upload"]',
            'restartJenkins': '//*[@id="scheduleRestartCheckbox"]'
        }
        self.username=""
        self.password=""

    # Navigate to Jenkins
    def openJenkins(self):
        self.browser.get(self.route)
    # Insert Username and Password
    def inputUserPass(self):
        try:
            usernameLink = self.browser.find_element_by_xpath(self.xpaths['openshiftLogin']['username'])
            usernameLink.clear()
            usernameLink.send_keys(self.username)
            passwordLink = self.browser.find_element_by_xpath(self.xpaths['openshiftLogin']['password'])
            passwordLink.clear()
            passwordLink.send_keys(self.password)
        except:
            print("DEBUG: Not able to input credentials : ")
    #Define a login cycle
    def loginCycle(self):
        try:
            self.inputUserPass()
        except:
            self.browser.find_element_by_xpath(self.xpaths['chooseUserOS4']).click()
            self.inputUserPass()

    # Login
    def login(self):
        # Press "Login with Openshift"
        self.browser.find_element_by_xpath(self.xpaths['loginWithOpenshift']).click()
        try:
            try:
                with file.open("~/.kubedeets","r") as kubedeets :
                    username=kubedeets.next()
                    password=kubedeets.next()
                    self.loginCycle()
            except:
                # Set username and password vars
                self.username="admin"
                self.password="redhat"
                self.loginCycle()
            finally:
                # Press the Login Button
                self.browser.find_element_by_xpath(self.xpaths['openshiftLogin']['login']).click()
        except:
            if self.username is "admin" and password is "redhat":
                print("DEBUG: Could not do generic login")
            else:
                print("""
                DEBUG: Could not login via ~/.kubedeets
                If you have not set it, do it as follows :-
                ```
                cat > ~/.kubedeets<<EOF
                ocadmin
                ocpasword
                EOF
                ```
                """)
    # Navigate and Input the plugin path
    def uploadPlugin(self):
        # Set the plugin path
        self.pluginPath=str(sys.argv[2])
        # Navigate to Manage Plugins Advanced Settings and Input Plugin path
        self.browser.get(self.route+'/pluginManager/advanced')
        inputPlugin = self.browser.find_element_by_name('name')
        inputPlugin.send_keys(self.pluginPath)
        # Upload the plugin
        uploadButton = self.browser.find_element_by_xpath(self.xpaths['uploadPlugin'])
        uploadButton.click()
    def restartJenkins(self):
        # Restart Jenkins
        restart = self.browser.find_element_by_xpath(self.xpaths['restartJenkins'])
        restart.click()
    def closeBrowser(self):
        # Close Browser
        self.browser.close()

# Run
jip = JIP()
jip.openJenkins()
jip.login()
if len(sys.argv) == 3:
    jip.uploadPlugin()
    jip.restartJenkins()
    jip.closeBrowser()
