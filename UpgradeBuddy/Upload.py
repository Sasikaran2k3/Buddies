import os
import StartBrowser
import time
import datetime
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
    
def ErrorCorrection():
    browser = StartBrowser.Start_Lap("UpgradeBuddy")
    browser.get("https://studio.youtube.com/")
    input()
#ErrorCorrection()


def YoutubeUpload():
    # Open Yt Studio
    browser.get("https://studio.youtube.com/")
    browser.minimize_window()
    browser.maximize_window()
    # Create Button
    browser.find_element(By.ID, "create-icon").click()
    browser.find_element(By.ID, "text-item-0").click()
    data = os.path.dirname(__file__) + "/" + date + ".mp4"
    print(data)
    browser.find_element(By.CSS_SELECTOR, 'input[type="file"]').send_keys(data)
    print(title, "\n\n", desc)
    text_boxes = browser.find_elements(By.CSS_SELECTOR, 'div[id="textbox"]')
    time.sleep(10)
    text_boxes[0].clear()
    text_boxes[0].send_keys(title) if len(title) < 100 else text_boxes[0].send_keys(title[:100])
    text_boxes[1].clear()
    text_boxes[1].send_keys(desc + link + yt_hashtags + "#shorts")
    browser.find_element(By.XPATH,
                         '//tp-yt-paper-radio-button[@class="style-scope ytkc-made-for-kids-select"][2]').click()
    browser.find_element(By.XPATH, '//div[text() = "Next"]').click()
    browser.find_element(By.XPATH, '//div[text() = "Next"]').click()
    browser.find_element(By.XPATH, '//div[text() = "Next"]').click()
    browser.find_element(By.XPATH, '//div[text()="Public"]').click()
    browser.find_element(By.XPATH, '//div[text() = "Publish"]').click()
    time.sleep(10)
    browser.implicitly_wait(25)

def InstaUplaod():
    # Insta
    data = os.path.dirname(__file__) + "/" + date + ".mp4"
    browser.get("https://www.instagram.com/")
    browser.implicitly_wait(25)
    browser.find_element(By.CSS_SELECTOR, 'svg[aria-label="New post"]').click()
    browser.find_element(By.XPATH, '//span[text()="Post"]').click()
    video_path = str(data)
    print(video_path)
    browser.find_element(By.XPATH, '//input[@accept="image/jpeg,image/png,image/heic,image/heif,video/mp4,video/quicktime"]').send_keys(video_path)
    time.sleep(5)
    browser.find_element(By.CSS_SELECTOR, 'svg[aria-label="Select Crop"]').click()
    browser.find_element(By.CSS_SELECTOR, 'svg[aria-label="Crop portrait icon"]').click()
    browser.find_element(By.XPATH, '//div[text()="Next"]').click()
    time.sleep(3)
    browser.find_element(By.XPATH, '//div[text()="Next"]').click()
    print(desc + link + yt_hashtags)
    act = ActionChains(browser)
    act.move_to_element((browser.find_element(By.XPATH, '//div[@aria-label="Write a caption..."]'))).perform()
    act.double_click()
    # act.click((browser.find_element(By.XPATH, '//div[@aria-label="Write a caption..."]'))).perform()
    act.send_keys(desc + link + yt_hashtags)
    act.perform()
    """for i in desc+link+yt_hashtags:
        browser.find_element(By.XPATH, '//div[@aria-label="Write a caption..."]').send_keys(i)"""
    time.sleep(10)
    browser.find_element(By.XPATH, '//div[text()="Share"]').click()
    wait = WebDriverWait(browser, 1000)
    wait.until(expected_conditions.invisibility_of_element((By.XPATH, '//div[text()="Sharing"]')))
    time.sleep(5)


# date is used for naming the files
date = "".join(str(datetime.date.today()).split("-"))


browser = StartBrowser.Start_Lap("UpgradeBuddy")
count = 0
while True:
    try:
        f = open(os.path.dirname(__file__) + "/Data/" + date + ".txt", "r")
        content = f.readlines()
        print(content)
        title = content[0]
        desc = "\nOpen the link to know more details\n"
        link = content[1]
        Ai_hash = open(os.path.dirname(__file__) + "/Data/" +date+"_hash.txt","r").read()
        my_hash = " #upgradebuddy #tech #technews #latestnews #trending "
        yt_hashtags = "\n"+Ai_hash + my_hash #" ".join(["#"+i.text for i in hash_result]) + my_hash
        print(yt_hashtags)
        YoutubeUpload()
        InstaUplaod()
    except Exception as e:
        print(e)
        print(count)
        browser.refresh()
        try:
            browser.switch_to.alert.accept()
        except:
            pass

        count += 1
        if count > 2:
            print("Publish error")
            break
    else:
        print("Published Successfully")
        break
