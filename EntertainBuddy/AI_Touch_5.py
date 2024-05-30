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
            script += "\n"
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
    path = base_path + ".txt" if "title" in prompt else base_path + "_meme.txt" if "meme" in prompt else base_path + "_hash.txt" if "hash" in prompt else base_path + "_script.txt"
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

prompt_file = open(os.path.dirname(__file__) + "/MyPrompt.txt", 'r+')
prompt = prompt_file.readlines()
if len(prompt) == 1:
    print("\nOwn Prompt\n", prompt)

    prompt_file.truncate(0)

count = 0
# Note: If adding new prompt, add var, put in list of prompt var and give if else condition for base path and file name
my_format_prompt = (
    'My format : The script should contain script sentence image prompt '
    'of that sentence in between sentences enclosed in [] and a very short dialogue for a second '
    'speaker who is impacted because of the sentence which is enclosed in (). Like Script Sentence [image '
    'prompt] (second speaker dialogue only) Followed by next sentence [] () as same paragraph. The script '
    'should tone like inspiring, use short sentence and easy to use frequent english words, '
    'dont sound like AI, avoid obvious knowledge, start with catchy hook like If You are a student '
    'You have to watch it or This is what will happen if this happen. Recollect what are the things '
    'required in a script and write a script in above format and constraints as single paragraph '
    'without emoji. Output should be only a single paragraph without any heading or response.Do not use any brackets in script sentence please.')

prompt_for_title = ". Give eye catching title with extreme emotions which is less 100 characters without emoji in 3 to 6 words\n"
# prompt_for_content = ". You are the best Question Answer Framer who can re-write news to Questions and Answer with comparative examples for better understanding and related to a common man. Write 4 meaningful and short and relatable Questions With Answer using the above news in one paragraph. The Question should contain image prompt of that sentence in between sentences enclosed in [] and a very short dialogue for a second speaker who gives Answer for the question which is enclosed in (). Example, Can Selena Gomez and Benny Blanco’s romance get any hotter? [A cozy photo of Selena and Benny snuggled up] (They're setting the love bar sky-high!).Why is Selena Gomez sharing intimate moments on Instagram? [An affectionate snapshot of Selena and Benny] (To show off their sweet love story!).Are Selena Gomez and Benny Blanco the newest power couple? [A picture capturing Selena and Benny's adorable bond] (Their romance is stealing the spotlight!).What's making Selena Gomez's fans swoon on social media? [A heartwarming image of Selena and Benny together] (Seeing her so happy with Benny is melting hearts!). Question and answer in the pattern of Question [img] (sec speaker Answer with facts and comparative examples). Only make the first question more crazy and curious to hook the audience based on news But rest of the Questions and Answers to give more facts and comparative examples with positive voice. Question and answers are short in length with minimum 8 to maximum 12 words to make audience listen before they scroll  and make all 4 sentence one after other separated by '.' and without space as a single sentence.Tone is Very Simple english (15 years old) and friendly and more facts from news. Output formate is same as example (Single Paragraph)\n"
if len(prompt)!=1:
    prompt_for_content = ("You are an expert in Instagram reels script writer creating viral and shareable scripts. I am a "
                          "script writer for a entertainment news channel named as Entertain Buddy who has mostly audience of age between 18 to 26 from India. Create a reels script with the above news in MY format." + my_format_prompt + "Example : If you're a student, you need to watch this! Elon Musk says AI will replace all "
                          "jobs. [Image of Elon Musk speaking] (What? No"
                          "jobs left?) He believes it's not a bad thing. \"Probably none of us will have a job,"
                          "\" Musk remarked at a Paris tech event. [Image of Paris tech event] (So, what will we do?) "
                          "Jobs will become optional. \"If you want to do a job as a hobby, you can.\" [Image of a "
                          "hobbyist working] (Just for fun?) Otherwise, AI and robots will provide any goods and "
                          "services. [Image of robots working] (That's crazy!).use short sentences and consider hook also as a script sentence.\n")
else:
    prompt_for_content = (
                "You are an expert in Instagram reels script writer creating viral and shareable scripts. I am a "
                "script writer for a tech news named as Entertain Buddy who has mostly audience of age between 18 to 26 from India. Create a reels script with my rough script idea in My format." + prompt[0] + my_format_prompt +"\n"
    )
                          # prompt_for_hook = ". Formulate a compelling hook in 15 words with a negative tone for above news. If it's [negative aspect], engage with '[Related emotion] [related audience]? A critical issue demanding your attention.\n"
prompt_for_hook = ". Begin with short story which is interesting,creative and related to the news in 15 words as hook.\n"
prompt_for_hashtag = ". Give 5 POPULAR hashtags as SENTENCE like ' #abc #def #xyx #fgh #xlm '.\n"
prompt_for_meme = ". Give a 3 to 7 worded sentence for meme. \n"
list_of_prompt = [prompt_for_content]#[prompt_for_title, prompt_for_content, prompt_for_hashtag]
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
