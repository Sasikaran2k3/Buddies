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
    video_prompt = ""
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
            video_prompt += "\n"
            continue
        elif flag == 0 and i.isalpha():
            flag = 3

        if flag == 3:
            script += i
        elif flag == 1:
            img_prompt += i
        elif flag == 2:
            video_prompt += i

    video_prompt = video_prompt.strip()
    f = open(os.path.dirname(__file__) + "/Data/" + date + "_script.txt", "w")
    f.write(script.strip())

    f = open(os.path.dirname(__file__) + "/Data/" + date + "_img.txt", "w")
    f.write(img_prompt.strip())

    f = open(os.path.dirname(__file__) + "/Data/" + date + "_vid.txt", "w")
    f.write(video_prompt.strip())

    print(img_prompt + "\n" + video_prompt + "\n" + script)


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

browser = StartBrowser.Start_Lap("UpgradeBuddy")

f = open(os.path.dirname(__file__) + "/Data/" + date + ".txt", 'r')
data = f.readlines()

prompt_file = open(os.path.dirname(__file__) + "/MyPrompt.txt", 'r+')
prompt = prompt_file.readlines()
if len(prompt) == 1:
    print("\nOwn Prompt\n", prompt)

    prompt_file.truncate(0)

count = 0
# Note: If adding new prompt, add var, put in list of prompt var and give if else condition for base path and file name
prompt_example = """Example : Environmental changes with {Flexed Biceps} Allu Arjun {Clapper Board}, you need to see this! {
Glowing Star} [Image of Allu Arjun smiling] (people impressed) The superstar is not just acting; he’s inspiring 
environmental change with a lot of money {Money Bag}. [Image of Environmental pollution] (environmental issues) {
Seedling} On World Environment Day {Herb}, he shared a powerful message {Speech Balloon} urging us to save the Earth 
{Earth Globe Europe-Africa}. [Image of Earth with greenery] (beautiful nature) His upcoming film {Clapper Board}, 
Pushpa 2: The Rule {Crown}, is set to release on August 15, 2024 {Calendar}. [Image of Pushpa 2 poster] (movie 
poster) It’s expected to be a blockbuster hit {Bomb} continuing the thrilling story {Movie Camera}. [Image of a 
thrilling scene from Pushpa] (exciting film scene) {Glowing Star} Allu Arjun’s dedication to environmental {Herb} 
causes is truly inspiring {Clapping Hands}. [Image of Allu Arjun planting a tree] (planting trees) Let’s follow his 
lead {World Map} and make a positive {Heavy Plus Sign} impact. [Image of people taking eco-friendly actions] (people 
taking eco-friendly actions)."""

base_prompt = """You are an expert in Instagram reels script writer creating viral and shareable scripts
with lot of emoji from given news. I am a script writer for a Tech news channel
named as Upgrade Buddy who has mostly audience of age between 18 and 34 from India."""

my_format_prompt = """Create a viral and shareable reels script with the above news in MY format.
My format : The script should contain script sentence image prompt
of that sentence in between sentences enclosed in [] and a generalized video prompt to search in pexels website
 which is enclosed in (). Like Script Sentence [image
prompt] (video prompt) Followed by next sentence [] () as same paragraph. The script
should tone like inspiring, use short sentence and easy to use frequent english words,
dont sound like AI, avoid obvious knowledge, start with catchy hook that is crazy about the news
but true and hook should be short and add emoji inside hook. Recollect what are the things
required in a script and write a script in above format and constraints as single paragraph.
Strictly Use atleast 3 emojis in each the script sentences alone but no emoji in image prompt and second
speaker that is no emoji inside [] and () dialogue. Output should be only a single paragraph without any
heading or response.Do not use any brackets in script sentence please and do not let any script sentence without
[] () including last sentence. Finally Strictly check these constraints in generated script :
content in {} MUST be replaced by emoji without {} and Each sentence in the script sentence must have minimum of 3
emojis and Each script sentence should have [image prompt] and (video prompt),
especially the last sentence and Each sentence in script sentence should have 8 to 15
words without obvious knowledge and Emoji should not present inside [] and (). Please Do not give {text} in generated script,
Use actual emojis and then give me that generated script."""

prompt_for_title = ". Give eye catching title with extreme emotions which is less 100 characters without emoji in 3 to 6 words\n"

if len(prompt) != 1:
    prompt_for_content = str(base_prompt + my_format_prompt + prompt_example).replace("\n"," ") + "\n"
else:
    prompt_for_content = str(base_prompt + prompt[0] + my_format_prompt + prompt_example).replace("\n"," ") + "\n"

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
