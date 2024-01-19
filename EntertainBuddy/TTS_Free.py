import os
import requests
import wget
import time
import datetime
import StartBrowser
from selenium.webdriver import Chrome, ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait


def ConvertText(content):
    browser.get("https://ttsfree.com/")
    #browser.refresh()
    browser.find_element(By.CSS_SELECTOR, 'textarea[name="input_text"]').send_keys(content)
    act = ActionChains(browser)
    lang_select = browser.find_element(By.CSS_SELECTOR, 'span[class="selection"]')
    drop = Select(browser.find_element(By.ID, "select_lang_bin"))
    drop.select_by_value("en-IN")
    time.sleep(2)
    time.sleep(10)
    browser.find_element(By.CSS_SELECTOR, 'a[title="Convert now"]').click()
    wait = WebDriverWait(browser, 100)
    wait.until(expected_conditions.visibility_of_element_located((By.PARTIAL_LINK_TEXT, 'Download Mp3')))
    audio = browser.find_element(By.XPATH, '//div[@class="label_process text-left"]/audio/source[2]')
    url = str(audio.get_attribute("src"))
    print(url)
    r = requests.get(url)
    with open(os.path.dirname(__file__) + "\\Data\\" + "%s.mp3" % (date),"wb") as f:
        f.write(r.content)


# date is used for naming the files
date = "".join(str(datetime.date.today()).split("-"))

count = 0

browser = StartBrowser.Start_Lap("EntertainBuddy")
while True:
    try:
        # Login
        browser.get("https://ttsfree.com/login")
        browser.find_element(By.CSS_SELECTOR, 'div[class="icheckbox_square-green"]').click()
        browser.refresh()
        browser.get("https://ttsfree.com/login")
        browser.find_element(By.CSS_SELECTOR, 'div[class="icheckbox_square-green"]').click()
        browser.find_element(By.CSS_SELECTOR, 'input[value="Login"]').click()
        time.sleep(7)
        f = open(os.path.dirname(__file__) + "//Data//" + date + "_script.txt", "r")
        content = f.readlines()
        print(content)
        stripped_content = ""
        for i in content:
            stripped_content += i.strip()+"\n"
            stripped_content = stripped_content
        ConvertText(stripped_content)
    except Exception as e:
        count += 1
        if count > 10:
            print("TTS error")
            break
        print(e)
    else:
        browser.quit()
        break
