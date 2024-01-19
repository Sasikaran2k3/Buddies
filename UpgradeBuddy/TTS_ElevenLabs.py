import os
import time
import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import StartBrowser


def ConvertText(content):
    browser.get("https://elevenlabs.io/speech-synthesis")
    browser.find_element(By.CSS_SELECTOR, 'textarea[name="text"]').send_keys(Keys.CONTROL+"a")
    browser.find_element(By.CSS_SELECTOR, 'textarea[name="text"]').send_keys(Keys.DELETE)
    time.sleep(5)
    browser.find_element(By.CSS_SELECTOR, 'textarea[name="text"]').send_keys(content)
    time.sleep(2)
    browser.find_element(By.XPATH,'//button[text()="Generate"]').click()
    wait = WebDriverWait(browser, 100)
    wait.until(expected_conditions.invisibility_of_element_located((By.XPATH, '//button[text()="Generating"]')))
    browser.find_element(By.XPATH, '//button[@aria-label="Download Audio"]').click()
    time.sleep(8)
    l = os.listdir(os.path.dirname(__file__) + "\\Data")
    details = {}
    for file in l:
        if ".mp3" in file:
            details[time.ctime(os.path.getmtime(os.path.dirname(__file__) + "/Data/" + file))] = file
    os.rename(os.path.dirname(__file__) + "/Data/" + details[max(details)],os.path.dirname(__file__) + "/Data/%s.mp3" % date)
    print(details[max(details)])


# date is used for naming the files
date = "".join(str(datetime.date.today()).split("-"))

count = 0

browser = StartBrowser.Start_Lap("UpgradeBuddy")

while True:
    try:
        f = open(os.path.dirname(__file__) + "//Data//" + date + "_script.txt", "r")
        content = f.readlines()
        print(content)
        stripped_content = ""
        for i in content:
            stripped_content += i.strip()+"\n"
        print(stripped_content)
        ConvertText(stripped_content)
    except Exception as e:
        count += 1
        if count > 5:
            print("TTS error")
            break
        print(e)
    else:
        browser.quit()
        break
