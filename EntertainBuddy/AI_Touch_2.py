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

def Talk_to_Rytr(prompt):
    time.sleep(1)
    # Click On Chat window
    browser.find_element(By.XPATH, '//button[@aria-controls="tabs--panel--2"]').click()
    # Clear old chat
    clear = browser.find_elements(By.XPATH, '//button[@class="_clear_1qglh_173"]')
    if clear != []:
        clear[0].click()
        browser.switch_to.alert.accept()
    wait = WebDriverWait(browser, 1000)

    # Wait for Chat window to open
    wait.until(expected_conditions.visibility_of_element_located((By.XPATH, '//p[text()="Start chatting now!"]')))

    instance_prompt = data[0].replace("\n", "") + prompt
    browser.find_element(By.XPATH, '//input[@placeholder="Enter your message..."]').send_keys(instance_prompt)

    # Wait for Response
    wait.until(expected_conditions.visibility_of_element_located((By.XPATH, '//div[@class="_item_nop3r_1 _bot_nop3r_35"]')))

    # Data folder with date is the basic path for any file in data folder
    base_path = os.path.dirname(__file__) + "/Data/" + date

    # Large nested If Else for selecting classifying prompt
    path = base_path+".txt" if "title" in prompt else base_path+"_meme.txt" if "meme" in prompt else base_path+"_hash.txt" if "hash" in prompt else base_path+"_hook.txt" if "ignorance" in prompt else base_path+"_script.txt"
    print("Info :", instance_prompt, prompt,path)

    # Chat is entire convo and dialog is particular dialog
    chat = browser.find_elements(By.XPATH, '// div[ @class ="_item_nop3r_1 _bot_nop3r_35"]')
    dialogs = chat[0].find_elements(By.XPATH, "//p")
    response = ""

    for i in dialogs:
        # Most of the response start with "
        # If didnt start with " Its len should be more than 8
        # To avoid picking dialog like Rytr or You or 11:29 am. They also come in dialogs
        if i.text.startswith("\"") or len(i.text)>8:
            response = i.text
            print(response)
            break
    if "title" in prompt:
        with open(path,"w") as f:
            # For Title, I need to write with news link on next line
            f.writelines([response.strip()+"\n", data[1]])
    else:
        # If not title then Just write on new file
        with open(path,"w") as f:
            f.write(response.strip())


f = open(os.path.dirname(__file__) + "/Data/" + date + ".txt", 'r')
data = f.readlines()

count = 0
# Note: If adding new prompt, add var, put in list of prompt var and give if else condition for base path and file name
prompt_for_title = ". Give SEO Optimized title which is less 100 characters \n"
prompt_for_content = ". Improve this into 30 words as newsletter. \n"
prompt_for_hook = ". Give a sentence that is outlining the dire consequences of ignorance the above news in 20 words.\n"
prompt_for_hashtag = ". Give 5 hashtags as SENTENCE.\n"
prompt_for_meme = ". Give 3 to 7 words only for meme. \n"
list_of_prompt = [prompt_for_title, prompt_for_content, prompt_for_hashtag, prompt_for_meme, prompt_for_hook]
while True:
    try:
        # Rytr Ai
        browser.get("https://app.rytr.me/create")
        for prompt in list_of_prompt:
            Talk_to_Rytr(prompt)
    except Exception as e:
        print("Error",e)
        count += 1
        if count > 2:
            print("Error Limit Reached")
            break
    else:
        browser.quit()
        break
