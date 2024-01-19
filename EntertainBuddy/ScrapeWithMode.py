import os
import wget
import time
import datetime
from selenium.webdriver.common.by import By
import StartBrowser


# Used to Scrape Data
def StartScrape(mode):
    count = 0
    # A refers to AutoScrape
    if mode == "A":
        print("Auto Scraping")
        today_link = ShuffleNewsPageLinks()
        browser.get(today_link)
        page = browser.find_element(By.CSS_SELECTOR, 'div[class="thumb"]>a')
        link = page.get_attribute("href")
        page.click()
    else:
        link = my_news_link_data[0]
        browser.get(link)
        my_news_link.truncate(0)
        print("Selected Scraping")
    while True:
        try:
            check = browser.find_element(By.CSS_SELECTOR, image_selector)
            title = browser.find_element(By.CSS_SELECTOR, title_selector).text
            img_desc = browser.find_element(By.XPATH, '//p[@class="caption"]').text
            url = check.get_attribute("src")
            print(img_desc)
            additional_images(img_desc)
            browser.quit()
            time.sleep(2)
            file = open(os.path.dirname(__file__) + "/Data/" + "%s.txt" % (date), "w")
            file.write(title + "\n" + link)
            pic_name = os.path.dirname(__file__) + "/Data/" + date + "_0.png"
            # wget is used to download image from its url and saves with given name
            wget.download(url, out=pic_name)
            file.close()
        except Exception as e:
            print(e)
            count += 1
            if count > 5:
                print("Scrap Error")
                break
        else:
            browser.quit()
            print("\nScrap Successful\n")
            break


def additional_images(img_desc, flag=0, no_of_images=6):
    # img_desc = "The ruling could require Apple to allow developers to provide external payment options"
    browser.get("https://www.google.com/imghp")
    browser.find_element(By.XPATH, "//textarea[@type='search']").click()
    browser.find_element(By.XPATH, "//textarea[@type='search']").send_keys(img_desc + "\n")
    all_img = browser.find_elements(By.XPATH, '//div[@class="fR600b islir"]//img')
    c = 1 if flag == 0 else 0
    for i in all_img:
        i.click()
        time.sleep(4)
        url = browser.find_elements(By.XPATH, '//div[@class="p7sI2 PUxBg"]//img')
        pic_name = os.path.dirname(__file__) + "/Data/" + date + "_%d" % c + ".png"
        for j in url:
            if "http" in j.get_attribute("src"):
                j.screenshot(pic_name)
                print("downloaded")
                c += 1
                break
        if c == no_of_images:
            break


# Used to Shuffle the order of different news pages links
def ShuffleNewsPageLinks():
    f = open(os.path.dirname(__file__) + "//NewsPageLink.txt", "r+")
    f.seek(0)
    Links = f.readlines()
    today_link = Links.pop(0)
    Links.append(today_link)
    f.seek(0)
    f.writelines(Links)
    f.close()
    return today_link


browser = StartBrowser.Start_Lap("EntertainBuddy")
date = "".join(str(datetime.date.today()).split("-"))
title_selector = "div[class='lead_heading header_wrap']>h1"
image_selector = "div[class='fullstoryImage']>div[class = 'heroimg']>img"

my_news_link = open(os.path.dirname(__file__) + "//my_news_link.txt", "r+")
my_full_news = open(os.path.dirname(__file__) + "//my_full_news.txt", "r+")

my_full_news_data = my_full_news.readlines()
my_news_link_data = my_news_link.readlines()

# All files in Data Folder is deleted
l = os.listdir(os.path.dirname(__file__) + "/Data")
for i in l:
    os.remove(os.path.dirname(__file__) + "/Data/" + i)

# Selecting the mode of scrap
if len(my_full_news_data) == 2:
    print("No Scraping")
    time.sleep(2)
    with open(os.path.dirname(__file__) + "/Data/" + date + '.txt', 'w') as f:
        f.writelines(my_full_news_data)
    additional_images(my_full_news_data[0], 1)
    my_full_news.truncate(0)
    browser.quit()
elif my_news_link_data != []:
    print("selected scrap")
    StartScrape("S")
else:
    l = os.listdir(os.path.dirname(__file__) + "/Data")
    print("auto scrape")
    StartScrape("A")
