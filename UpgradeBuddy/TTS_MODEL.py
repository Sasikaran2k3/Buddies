import datetime
import os
import time

import wget
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
import StartBrowser


date = "".join(str(datetime.date.today()).split("-"))


browser = StartBrowser.Start_Lap("UpgradeBuddy")
browser.implicitly_wait(15)

browser.get("https://colab.research.google.com/drive/1ISvpY3YSeBKvdYj99uSP3bPADZwABQvV?usp=sharing")
act = ActionChains(browser)
act.send_keys(Keys.ARROW_DOWN).send_keys(Keys.ARROW_DOWN).perform()
act.key_down(Keys.CONTROL)
act.send_keys("a").key_up(Keys.CONTROL).send_keys(Keys.DELETE).perform()
f = open(os.path.dirname(__file__) + "//Data//" + date + "_script.txt", "r")
content = f.readlines()
print(content)
stripped_content = ""
for i in content:
    stripped_content += i.strip()
    stripped_content = stripped_content.replace("\"", " ")
text = stripped_content
prompt = """
import requests

API_URL = "https://api-inference.huggingface.co/models/facebook/mms-tts-eng"
headers = {"Authorization": "Bearer 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"}

response = requests.post(API_URL, headers=headers, json={"inputs": "%s",})
audio_bytes = response.content
from IPython.display import Audio
Audio(audio_bytes)
"""%text
act.send_keys(prompt).perform()
act.key_down(Keys.CONTROL).send_keys(Keys.ENTER).key_up(Keys.CONTROL).perform()

browser.find_element(By.XPATH,'//mwc-button[text()="Run anyway"]').click()
time.sleep(20)
wait = WebDriverWait(browser,10000)
print("Audio Preparing")
wait.until(expected_conditions.visibility_of_element_located((By.XPATH,'//div[@class="mwc-icon success"]')))
browser.switch_to.frame(browser.find_element(By.XPATH,'//div[@class="output-iframe-sizer"]//iframe'))
wait.until(expected_conditions.visibility_of_element_located((By.XPATH,'//div[@id="output-body"]')))
print("Switched")
print(browser.find_element(By.XPATH,"//body/div").get_attribute("id"))
wait.until(expected_conditions.visibility_of_element_located((By.XPATH,'//div[@class="output-iframe-sizer"]//iframe//div[@id="output-body"]//audio//source')))
audioTag = browser.find_element(By.XPATH,'//div[@id="output-body"]//audio//source')
print(audioTag.get_attribute("src"))
quit()
while True:
    audioTag = browser.find_elements(By.XPATH,'//div[@id="output-body"]//audio//source')
    print(audioTag)
    if audioTag:
        print("Ready")
        print(audioTag[0].get_attribute("src"))
        break
wget.download(url=audioTag.get_attribute("src"),out="summa.wav")