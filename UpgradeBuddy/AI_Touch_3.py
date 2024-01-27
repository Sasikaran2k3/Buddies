import os
import time
import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
import StartBrowser

# date is used for naming the files
date = "".join(str(datetime.date.today()).split("-"))

browser = StartBrowser.Start_Lap("UpgradeBuddy")


def ErrorCorrection():
    browser.get("https://chat.openai.com/")
    time.sleep(5)
    text_box = browser.find_element(By.XPATH, '//textarea[@id="prompt-textarea"]')
    prompt_for_content = ". Improve this into 20 words as newsletter. \n"
    f = open(os.path.dirname(__file__) + "/Data/" + date + ".txt", 'r')
    data = f.readlines()
    instance_prompt = data[0].replace("\n", "") + prompt_for_content
    text_box.send_keys("write 100 words abt sea\n")
    wait = WebDriverWait(browser, 1000)
    wait.until(expected_conditions.visibility_of_element_located((By.XPATH, '//div[@class="flex"]')))
    time.sleep(3)
    response = browser.find_elements(By.XPATH, '//div[@data-message-author-role="assistant"]//p')
    response[0].click()
    print(response[0].text)
    quit()

#ErrorCorrection()

def Talk_to_Gpt(prompt):
    time.sleep(4)


    instance_prompt = data[0].replace("\n", "") + prompt
    browser.find_element(By.XPATH, '//textarea[@id="prompt-textarea"]').send_keys(instance_prompt)

    # Wait for Response
    wait = WebDriverWait(browser, 1000)
    wait.until(expected_conditions.visibility_of_element_located((By.XPATH, '//div[@class="flex"]')))

    # Data folder with date is the basic path for any file in data folder
    base_path = os.path.dirname(__file__) + "/Data/" + date

    # Large nested If Else for selecting classifying prompt
    path = base_path+".txt" if "title" in prompt else base_path+"_meme.txt" if "meme" in prompt else base_path+"_hash.txt" if "hash" in prompt else base_path+"_hook.txt" if "hook" in prompt else base_path+"_script.txt"
    print("Info :", instance_prompt, prompt,path)
    time.sleep(8)

    # Response From chatGPT
    response = browser.find_element(By.XPATH, '//div[@data-message-author-role="assistant"]//p').text
    print(response)
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
prompt_for_title = ". Give SEO Optimized title which is less 100 characters\n"
prompt_for_content = ". Give a 30 words artical\n"
prompt_for_hashtag = ". Give 5 hashtags in one line.\n"
prompt_for_meme = ". Give a meme in 3 to 7 words only.\n"
list_of_prompt =[prompt_for_title, prompt_for_content, prompt_for_hashtag, prompt_for_meme]
while True:
    try:
        for prompt in list_of_prompt:
            browser.get("https://chat.openai.com/")
            Talk_to_Gpt(prompt)
    except Exception as e:
        print("Error",e)
        count += 1
        if count > 2:
            print("Error Limit Reached")
            break
    else:
        browser.close()
        break
