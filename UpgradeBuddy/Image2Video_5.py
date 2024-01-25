import datetime
import os
import time
import moviepy
from moviepy.editor import *
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import StartBrowser

def ErrorCorrection():
    date = "".join(str(datetime.date.today()).split("-"))
    background_image = moviepy.editor.ImageClip(os.path.dirname(__file__) + "/Background3.jpg")
    background = background_image.resize((1080, 1920)).set_duration(3)
    background_image = moviepy.editor.ImageClip(os.path.dirname(__file__) + "/Background2.png")
    background1 = background_image.resize((900, 1500)).set_duration(3).set_position((90,350))
    out = CompositeVideoClip([background, background1])
    out.write_videofile(os.path.dirname(__file__) + "/%s.mp4" % date, fps=24)
    #MakeVideo()
    quit()


#ErrorCorrection()
def KapwingEdit():
    browser.get("https://www.kapwing.com/folder/")

    # Create Workspace and make new project
    browser.find_element(By.XPATH, '//div[@data-cy="workspace-new-project-button"]').click()
    create = browser.find_elements(By.XPATH, '//div[text() = "Create a New Project"]')

    # if no of workspace is less than 3
    if create: create[0].click()

    # Upload video
    browser.find_element(By.XPATH, '//input[@data-cy="upload-input"]').send_keys(
        os.path.dirname(__file__) + "/%s.mp4" % date)
    print("Video Sent")
    time.sleep(10)

    wait = WebDriverWait(browser, 1000)
    ActionChains(browser).send_keys(Keys.ESCAPE).perform()

    # Pressing Subtitle Buttons
    browser.find_element(By.XPATH, '//div[text() = "Subtitles"]').click()
    browser.find_element(By.XPATH, '//span[text() = "Auto subtitles"]').click()
    while browser.find_elements(By.XPATH, '//span[text() = "Auto Subtitle"]'):
        browser.find_element(By.XPATH, '//span[text() = "Auto Subtitle"]').click()
    print("Waiting in Subtitle")

    # Wait till subtitle appears
    wait.until(expected_conditions.invisibility_of_element((By.XPATH, "//span[text()='Generating Subtitles...']")))
    wait.until(expected_conditions.presence_of_element_located((By.XPATH, '//textarea[@data-cy="magic-textarea"]')))
    print("Sub Ready")
    # Move dragger to left to reduce subtitle length
    for _ in range(10):
        browser.find_element(By.XPATH, '//span[@role="slider"]').send_keys(Keys.LEFT)
    # Select Subtitle
    browser.find_element(By.XPATH, '//textarea[@data-cy="magic-textarea"]').click()
    act = ActionChains(browser)
    transform = browser.find_elements(By.XPATH, '//div[@data-cy="drag-handler"]')

    # Selects the subtitle style
    parent = browser.find_elements(By.XPATH, '//div[@class="PresetPreview-module_container_034hO"]')
    for i in parent:
        if i.find_element(By.TAG_NAME, 'input').get_attribute("value") == "My":
            i.click()
            break

    # Move the subtitle to Center by slowly changing y axis and stop when grid/Snap line is approched twice
    act.click_and_hold(transform[1]).move_to_element_with_offset(transform[0], 0, 0).release().perform()
    print("Placed Center")

    browser.find_element(By.CSS_SELECTOR, 'div[data-cy="create-button"]').click()

    # Export Panel
    browser.find_element(By.CSS_SELECTOR, 'div[data-cy="export-panel-create-button"]').click()
    time.sleep(5)
    browser.find_element(By.CSS_SELECTOR,
                         'div[class = "common-module_smallControlButton_66vuT ExportRow-module_buttonStyle_L6WYa '
                         'ExportRow-module_studioColor_ltubC "]').click()
    time.sleep(7)
    print("Download Page")

    # Waits till the size of the file appears and then dowload button is clicked
    wait = WebDriverWait(browser, 1000)
    wait.until(expected_conditions.visibility_of_element_located(
        (By.XPATH, '//div[@class="VideoContainer-module_commentsMetaDataFileSize_E7zW4"]')))
    time.sleep(5)
    print("Download Available")
    while True:
        no_of_item = len(os.listdir(os.path.dirname(__file__) + "/Data"))
        browser.find_element(By.XPATH, '//span[text() = "Download file" ]').click()
        time.sleep(3)
        if os.listdir(os.path.dirname(__file__) + "/Data") != no_of_item:
            print("Download Started")
            time.sleep(60)
            break
    print("Download Completed Successfully")
    print("Kapwing Closed")

def ImageAnimation(ImageClip, duration, flag):
    # Load the image
    image = ImageClip
    #background_image = moviepy.editor.ImageClip("Background1.png"  )
    # Set the desired duration in seconds (e.g., 10 seconds)
    duration = duration

    # Calculate the canvas dimensions (9:16 aspect ratio)
    canvas_width = 1080-18-18 # -18 is to fit in template
    canvas_height = 820

    # Resize the image to have a height of 1920 pixels and maintain its original aspect ratio
    resized_image = image.resize(height=canvas_height)
    #background = background_image.resize(height = 1920)
    # Create a black background clip with the canvas dimensions
    background = ColorClip(size=(canvas_width, canvas_height), color=(0, 0, 0))

    # Calculate the horizontal position to start the image on the left side of the canvas
    x_start_position_left = 0

    # Calculate the horizontal position to end the image on the right side of the canvas
    x_end_position_left = canvas_width - resized_image.size[0]

    # Create a function to animate the image's horizontal position to move left
    def move_image_left(t):
        x_position = int(x_start_position_left + (x_end_position_left - x_start_position_left) * t / duration)
        return x_position, 0

    # Calculate the horizontal position to start the image on the right side of the canvas
    x_start_position_right = x_end_position_left

    # Calculate the horizontal position to end the image on the left side of the canvas
    x_end_position_right = x_start_position_left

    # Create a function to animate the image's horizontal position to move right
    def move_image_right(t):
        x_position = int(x_start_position_right + (x_end_position_right - x_start_position_right) * t / duration)
        return x_position, 0

    if flag == "L":
        # Animate the image's horizontal position to move left within the given duration
        animated_image_left = resized_image.set_position(move_image_left).set_duration(duration)
        final = CompositeVideoClip([background.set_duration(duration), animated_image_left]).set_fps(24)
    else:
        # Animate the image's horizontal position to move right within the given duration
        animated_image_right = resized_image.set_position(move_image_right).set_duration(duration)
        final = CompositeVideoClip([background.set_duration(duration), animated_image_right]).set_fps(24)
    return final

# Delete Old final video
l = os.listdir(os.path.dirname(__file__))
for i in l:
    if ".mp4" in i:
        os.remove(os.path.dirname(__file__) + "/" + i)


def MakeVideo():
    audio = AudioFileClip(os.path.dirname(__file__) + "/Data/%s.wav" % date)
    back = AudioFileClip(os.path.dirname(__file__) + "/Background1.mp3")
    effect = AudioFileClip(os.path.dirname(__file__) + "/Background/Sound_Effects2.mp3")
    back = concatenate_audioclips([effect, back])
    final = []

    # No of image Shifts
    shift_count = 8
    divider = audio.duration / shift_count

    for i in range(shift_count):
        pic_num = i % 6
        print(pic_num)
        img = ImageClip(os.path.dirname(__file__) + "/Data/%s_%d.png" % (date, pic_num))
        img = ImageAnimation(img, divider, flag="L" if i % 2 == 0 else "R")
        final.append(img)


    # Color clip with black and reels size
    background = ColorClip(color=(0, 0, 0),size=(1080, 1920))
    background = ImageClip(os.path.dirname(__file__) + "/Background/Background_Template.png").set_duration(shift_count * divider)
    # 600px top and 720px Video and 600 bottom so total 1920
    # Combine all the small video to full video and place at y axis 800
    out = concatenate(final, method="compose").set_position((18, 720))

    # Sentence 1 to write on top of video with size of 300px
    text1 = TextClip(parts_of_meme, font="Montserrat-ExtraBold", color="black", method="caption", size=(1080-18-18, 200),
                     align="south", kerning=-5).set_position((18,480)).set_duration(divider*shift_count)
    print("First Sentence = ", parts_of_meme)


    out = CompositeVideoClip([background, out, text1]).set_duration(shift_count * divider)
    out = out.set_audio(CompositeAudioClip([audio, back]).set_duration(divider*shift_count))
    #out = concatenate_videoclips([VideoFileClip(os.path.dirname(__file__) + "/Background/Background_Template.mp4").subclip(0, 1.5),out])
    out.write_videofile(os.path.dirname(__file__) + "/%s.mp4" % date, fps=24)


date = "".join(str(datetime.date.today()).split("-"))
f = open(os.path.dirname(__file__) + "/Data/" + date + "_meme.txt", "r")
content = f.read()
print(content)
parts_of_meme = content[1:-1].upper()
print("Parts :",len(parts_of_meme),parts_of_meme)
MakeVideo()
browser = StartBrowser.Start_Lap("UpgradeBuddy")

count = 0
while True:
    try:
        KapwingEdit()
        time.sleep(20)
        # while loops till .mp4 file is found on Data folder
        while True:
            # Return list of files in data folder
            l = os.listdir(os.path.dirname(__file__) + "/Data")
            print("waiting")
            flag = 0
            for i in l:
                if ".mp4" in i:
                    flag = 1
                    break
            if flag == 1:
                break
        details = {}
        for i in l:
            if ".mp4" in i:
                # Delete All .mp4 file on root directory
                # After download from kapwing, Raw file is deleted and subtitled file from data is placed on root
                os.remove(os.path.dirname(__file__) + "/%s.mp4" % date)
                details[time.ctime(os.path.getmtime(os.path.dirname(__file__) + "/Data/" + i))] = i
        os.rename(os.path.dirname(__file__) + "/Data/" + details[max(details)],
                  os.path.dirname(__file__) + "/%s.mp4" % date)
        print(details[max(details)])
    except Exception as e:
        print(e)
        count += 1
        if count > 10:
            print("Kapwing Error")
            break
    else:
        browser.quit()
        break
