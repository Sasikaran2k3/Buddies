import os
import time
import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
import StartBrowser


def ErrorCorrection():
    time.sleep(5)
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


# ErrorCorrection()




def ProcessResponse():
    f = open(os.path.dirname(__file__) + "/Data/" + date + "_script.txt", "r")
    data = f.read()
    f.close()

    img_prompt = ""
    new_speaker = ""
    script = ""
    flag = 0
    for i in data:
        if i == '[':
            flag = 1
            script+="\n"
            continue

        elif i == ']':
            flag = 0
            img_prompt += "\n"
            continue

        elif i == '(':
            flag = 2
            continue

        elif i == ')':
            flag = 0
            new_speaker += "\n"
            continue
        elif flag == 0 and i.isalpha():
            flag = 3

        if flag == 3:
            script += i
        elif flag == 1:
            img_prompt += i
        elif flag == 2:
            new_speaker += i


    f = open(os.path.dirname(__file__) + "/Data/" + date + "_script.txt", "w")
    f.write(script)

    f = open(os.path.dirname(__file__) + "/Data/" + date + "_img.txt", "w")
    f.write(img_prompt)

    f = open(os.path.dirname(__file__) + "/Data/" + date + "_speaker.txt", "w")
    f.write(new_speaker)

    print(img_prompt + "\n" + new_speaker + "\n" + script)


def Talk_to_Gpt(prompt):
    print("Waiting to open")
    time.sleep(5)

    instance_prompt = data[0].replace("\n", "") + prompt
    browser.find_element(By.XPATH, '//textarea[@id="prompt-textarea"]').send_keys(instance_prompt)

    # Wait for Response
    wait = WebDriverWait(browser, 1000)
    browser.find_element(By.XPATH, '//div[@data-message-author-role="assistant"]//p').click()
    wait.until(expected_conditions.visibility_of_element_located((By.XPATH, '//div[@class="flex"]')))

    # Data folder with date is the basic path for any file in data folder
    base_path = os.path.dirname(__file__) + "/Data/" + date

    # Large nested If Else for selecting classifying prompt
    path = base_path+".txt" if "title" in prompt else base_path+"_meme.txt" if "meme" in prompt else base_path+"_hash.txt" if "hash" in prompt else base_path+"_script.txt"
    print("Info :", instance_prompt, prompt, path)
    time.sleep(5)

    # Response From chatGPT
    response = browser.find_element(By.XPATH, '//div[@data-message-author-role="assistant"]//p').text
    print(response)
    if "title" in prompt:
        with open(path, "w") as f:
            # For Title, I need to write with news link on next line
            f.writelines([response.strip() + "\n", data[1]])
    else:
        # If not title then Just write on new file
        with open(path, "w") as f:
            f.write(response.strip())

# date is used for naming the files
date = "".join(str(datetime.date.today()).split("-"))

browser = StartBrowser.Start_Lap("UpgradeBuddy")

f = open(os.path.dirname(__file__) + "/Data/" + date + ".txt", 'r')
data = f.readlines()

count = 0
# Note: If adding new prompt, add var, put in list of prompt var and give if else condition for base path and file name
prompt_for_title = ". Give eye catching title with extreme emotions which is less 100 characters without emoji\n"
prompt_for_content = ". Write a paragraph of video script and take that script more emotional and carry a strong feeling in it and script should contain exactly 6 sentece and each sentence of the script should be small and concise. That script should be made out of news above. That script should contain image prompt of that sentence in between them enclosed in [] and a very short dialogue for a second speaker who is impacted because of the sentence which is enclosed in () and the sentence should be in first person like (I am a driver, I that funny for a car to go itself ?) as a first person speaker. The pattern is News sentence [] (). Example: News sentence1 [Image Prompt for that sentence] (second speaker who gives clarity). Next sentence [ Image Prompt] (second speaker who shows the impact from the sentence with emotion as dialogue only and it should be short with who is he and how it affects like As a freelancer I'm so impressed of this or Its a happy news to hear as a doctor or I'm so happy for it or Will I get fired? or am I safe?). Keeps on going [Image Prompt] (Its a happy news to hear as a doctor or I'm so happy for it or Will I get fired? or am I safe? or Good to know or humorous or some emotional dialogs in first person). Make sure 1st sentence have an eye-catchy image and controversial dialogue.This is the actual example On April 19, Bitcoin underwent a monumental shift. [A dramatic image of a Bitcoin splitting in half] (As a small business owner, will my Bitcoin savings still secure my future?). Make sure the first sentence act as a video hook which Pose Intriguing Questions or Highlight a Problem for building curiosity. First sentence should be 5 to 7 words only and make them feel curious and in negative tone. And use easy or simple words\n"
# prompt_for_hook = ". Formulate a compelling hook in 15 words with a negative tone for above news. If it's [negative aspect], engage with '[Related emotion] [related audience]? A critical issue demanding your attention.\n"
prompt_for_hook = ". Begin with short story which is interesting,creative and related to the news in 15 words as hook.\n"
prompt_for_hashtag = ". Give 5 hashtags as SENTENCE like ' #abc #def #xyx #fgh #xlm '.\n"
prompt_for_meme = ". Give a 3 to 7 worded sentence for meme. \n"
list_of_prompt = [prompt_for_title, prompt_for_content, prompt_for_hashtag]
while True:
    try:
        #input()
        for prompt in list_of_prompt:
            browser.get("https://chat.openai.com/")
            Talk_to_Gpt(prompt)
        ProcessResponse()
    except Exception as e:
        print("Error", e)
        count += 1
        if count > 2:
            print("Error Limit Reached")
            break
    else:
        browser.quit()
        break
