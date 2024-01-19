import os
import time
import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
import StartBrowser

# date is used for naming the files
date = "".join(str(datetime.date.today()).split("-"))

browser = StartBrowser.Start_Lap("EntertainBuddy")


def ErrorCorrection():
    browser.get("https://app.rytr.me/create")
    input()


#ErrorCorrection()

f = open(os.path.dirname(__file__) + "/Data/" + date + ".txt", 'r')
data = f.readlines()

count = 0

while True:
    try:
        # Rytr Ai
        browser.get("https://app.rytr.me/create")
        time.sleep(2)
        browser.find_element(By.XPATH, '//button[@aria-controls="tabs--panel--2"]').click()
        # Clear old chat
        clear = browser.find_elements(By.XPATH, '//button[@class="_clear_1qglh_173"]')
        if clear != []:
            clear[0].click()
            browser.switch_to.alert.accept()
        wait = WebDriverWait(browser, 1000)
        wait.until(expected_conditions.visibility_of_element_located((By.XPATH, '//p[text()="Start chatting now!"]')))

        prompt = data[0].replace("\n", "") + ". improve this into 50 words as dialogs and give a title. \n"
        print("prompt :", prompt)
        browser.find_element(By.XPATH, '//input[@placeholder="Enter your message..."]').send_keys(prompt)
        time.sleep(10)

        chat = browser.find_elements(By.XPATH, '// div[ @class ="_item_nop3r_1 _bot_nop3r_35"]')
        print(len(chat))
        dialogs = chat[0].find_elements(By.XPATH, "//p")
        script = []

        for i in dialogs:
            dialog = i.text
            print(dialog)
            if "Title" in dialog:
                new_title = ":".join(dialog.split(":")[1:])
                continue
            if "Rytr" not in dialog and "[" not in dialog and "You" != dialog and len(dialog.split(":")[-1]) != 5:
                script.append(dialog.split(":")[-1] + "\n")
        print(new_title)
        print(script)
        output = [new_title.strip() + "\n", data[1]]
        print(output)
        f = open(os.path.dirname(__file__) + "/Data/" + date + ".txt", 'w')
        f.writelines(output)
        f.close()
        f = open(os.path.dirname(__file__) + "/Data/" + date + "_script.txt", 'w')
        f.writelines(script)
        f.close()
    except Exception as e:
        count += 1
        if count > 2:
            print("Error Limit Reached")
            break
        print(e)
    else:
        browser.quit()
        break
