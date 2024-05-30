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
    new_speaker = new_speaker.strip() + " Thanks Entertain Buddy."
    f = open(os.path.dirname(__file__) + "/Data/" + date + "_script.txt", "w")
    f.write(script.strip())

    f = open(os.path.dirname(__file__) + "/Data/" + date + "_img.txt", "w")
    f.write(img_prompt.strip())

    f = open(os.path.dirname(__file__) + "/Data/" + date + "_speaker.txt", "w")
    f.write(new_speaker.strip())

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

browser = StartBrowser.Start_Lap("EntertainmentBuddy")

f = open(os.path.dirname(__file__) + "/Data/" + date + ".txt", 'r')
data = f.readlines()

count = 0
# Note: If adding new prompt, add var, put in list of prompt var and give if else condition for base path and file name
prompt_for_title = ". Give eye catching title with extreme emotions which is less 100 characters without emoji in 3 to 6 words\n"
prompt_for_content = "You are an expert in Instagram reels script writer creating viral and shareable scripts. I am a script writer for a tech news named as Entertain Buddy who has mostly audience of age between 18 to 28 from India. Create a reels script with the above news in MY format. The script should contain image prompt of that sentence in between sentences enclosed in [] and a very short dialogue for a second speaker who is impacted because of the sentence which is enclosed in (). Like Script [image prompt] (second speaker dialogue only) Followed by next sentence as same paragraph. The script should tone like inspiring, use short sentence and easy to use frequent english words, dont sound like AI, avoid obvious knowledge, start with catchy hook like If you don't want to feel clueless when your friends rave about the newest gaming releases, watch this video till the end. If you don't want to feel left out when your friends discuss the hottest fashion trends, stay tuned for the full video or If you don't want to feel awkward when your friends talk about the latest viral debate, make sure to watch this entire video (hook should provoke fear). Recollect what are the things required in a script and write a script in above format and constraints as single paragraph without emoji.Example : If you don't want to feel clueless when your friends rave about the newest twitter releases of Suchi, watch this video till the end. Singer Suchitra shook the industry with a Twitter leak bombshell in 2017. [Image of Suchitra surrounded by controversy] (Whoa, what happened?) Private moments of Tamil celebs went public! [Image of Dhanush and Trisha] (Seriously?) Dhanush and Trisha, Anirudh Ravichander and Andrea, caught in the spotlight. [Image of Anirudh Ravichander and Andrea] (That's intense!) Then, Suchitra claimed she was roughed up by Dhanush's team! [Image of Suchitra showing bruises] (What a shocker!) But wait, twist in the tale: her husband clarified her account was hacked! [Image of Suchitra and her husband] (Phew, what a relief!). Make sure even the Last line of script also follow the format of script [] ()\n"
#prompt_for_content = ". You are the best Question Answer Framer who can re-write news to Questions and Answer with comparative examples for better understanding and related to a common man. Write 4 meaningful and short and relatable Questions With Answer using the above news in one paragraph. The Question should contain image prompt of that sentence in between sentences enclosed in [] and a very short dialogue for a second speaker who gives Answer for the question which is enclosed in (). Example, Can Selena Gomez and Benny Blanco’s romance get any hotter? [A cozy photo of Selena and Benny snuggled up] (They're setting the love bar sky-high!).Why is Selena Gomez sharing intimate moments on Instagram? [An affectionate snapshot of Selena and Benny] (To show off their sweet love story!).Are Selena Gomez and Benny Blanco the newest power couple? [A picture capturing Selena and Benny's adorable bond] (Their romance is stealing the spotlight!).What's making Selena Gomez's fans swoon on social media? [A heartwarming image of Selena and Benny together] (Seeing her so happy with Benny is melting hearts!). Question and answer in the pattern of Question [img] (sec speaker Answer with facts and comparative examples). Only make the first question more crazy and curious to hook the audience based on news But rest of the Questions and Answers to give more facts and comparative examples with positive voice. Question and answers are short in length with minimum 8 to maximum 12 words to make audience listen before they scroll  and make all 4 sentence one after other separated by '.' and without space as a single sentence.Tone is Very Simple english (15 years old) and friendly and more facts from news. Output formate is same as example (in paragraph)\n"
#prompt_for_content = ". Write a paragraph of youtube shorts video script and take that script more emotional and carry a strong feeling in it and script should contain exactly 4 sentece and each sentence of the script should be small and concise. That script should be made out of news above. That script should contain image prompt of that sentence in between them enclosed in [] and a very short dialogue for a second speaker who is impacted because of the sentence which is enclosed in () and the sentence should be in first person like (I am a driver, I that funny for a car to go itself ?) as a first person speaker. The pattern is News sentence [] (). Example: News sentence1 [Image Prompt for that sentence] (second speaker who gives clarity). Next sentence [ Image Prompt] (second speaker who shows the impact from the sentence with emotion as dialogue only and it should be short with who is he and how it affects like As a freelancer I'm so impressed of this or Its a happy news to hear as a doctor or I'm so happy for it or Will I get fired? or am I safe?). Keeps on going [Image Prompt] (Its a happy news to hear as a doctor or I'm so happy for it or Will I get fired? or am I safe? or Good to know or humorous or some emotional dialogs in first person). Make sure 1st sentence have an eye-catchy image and controversial dialogue.This is the actual example On April 19, Bitcoin underwent a monumental shift, Do You know Why?. [A dramatic image of a Bitcoin splitting in half] (As a small business owner, will my Bitcoin savings still secure my future?). Cryptocurrency enthusiasts brace for impact. [A worried individual checking their phone for Bitcoin prices] (As an investor, should I hold or sell?)... upto 4 sentence. Make sure the first sentence act as a video hook which Pose Intriguing Questions for building curiosity. First sentence should be 5 to 7 words only and make them feel curious. And use easy or simple words\n"
# prompt_for_hook = ". Formulate a compelling hook in 15 words with a negative tone for above news. If it's [negative aspect], engage with '[Related emotion] [related audience]? A critical issue demanding your attention.\n"
#prompt_for_hook = ". Begin with short story which is interesting,creative and related to the news in 15 words as hook.\n"
prompt_for_hashtag = ". Give 5 POPULAR hashtags as SENTENCE like ' #abc #def #xyx #fgh #xlm '.\n"
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
