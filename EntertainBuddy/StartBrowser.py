import os
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


def Start_Lap(browser_name="EntertainBuddy"):
    # Initialization of web Driver
    opt = Options()
    # This option is used to verify the action part without starting from beginning
    opt.add_experimental_option('debuggerAddress',"localhost:1133")
    # CMD prompt is google-chrome --remote-debugging-port=1135 --user-data-dir="/home/sasi/PycharmProjects/EntertainBuddy/EntertainBuddy"
    path_of_browser = os.path.dirname(__file__) + '/%s' % browser_name
    print(path_of_browser)
    opt.add_argument(r'--user-data-dir=%s'%path_of_browser)
    services = Service(executable_path=os.path.dirname(__file__) + "/chromedriver")
    browser = Chrome(service=services, options=opt)
    browser.maximize_window()
    browser.implicitly_wait(15)
    return browser
