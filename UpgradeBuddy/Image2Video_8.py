import datetime
import os.path
import random
import StartBrowser
import time
from moviepy.editor import *
import moviepy.video.fx.all as vfx
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys


def ErrorCorrection():
    template = ImageClip(os.path.dirname(__file__) + "/Background/Buddy_Template_Green.png")


# ErrorCorrection()
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


# Delete Old final video
l = os.listdir(os.path.dirname(__file__))
for i in l:
    if ".mp4" in i:
        os.remove(os.path.dirname(__file__) + "/" + i)


def make_video():
    def move_left(t):
        # t/divider give a percentage like 0 to 100%
        # width of resized img - width of template - x which is gap from 0 to template position.
        # This will stop video when image touches the end and not let the img leave the canva fully
        # concept is 0-100% of total width is displayed as video.
        # if t is 1 and duration is 2 then 50% of width of the img is the position and
        # if t is 2 then 100% of width of img is covered
        posi = -(t / (divider)) * (dimension_of_full_green_resize[1] - dimension_of_full_green_temp[1] - x), y
        return posi

    def zoom_in(t):
        # Zoom in effect
        # t is very small so to have a zooming factor we add 1
        # 0.15 is for speed
        # if t is 1 second the zoom is 1.15 and if t is 2 then 1.3
        return 1 + t * 0.15

    audio = AudioFileClip(os.path.dirname(__file__) + "/Data/%s.wav" % date)
    effect = AudioFileClip(os.path.dirname(__file__) + "/Background/Sound_Effects2.mp3")
    background = AudioFileClip(os.path.dirname(__file__) + "/Background/Background.mp3")
    back = concatenate_audioclips([effect,background])

    dummy_size = (1920, 1080)
    dummy_back = ColorClip(size=dummy_size[::-1], color=(0, 0, 0)).set_duration(2)

    # Green Color code for removing mask
    green_screen_color = [0, 255, 0]

    # These are the Green Screen Dimension in each template
    dimension_of_full_green_temp = (1543, 972)
    dimension_of_logo_green_temp = (1114, 972)
    dimension_of_full_green_resize = []

    # Final Array will collect all the clips with animations
    final = []

    # img_of_each_clip collects img of each clip's 0th second for keeping on the other side of mask effect
    img_of_each_clip = []

    # x,y coordinate of logo template
    x, y = (54, 187)

    # No of image Shifts
    shift_count = 6

    # divider is the time for each clips of animations
    divider = audio.duration / shift_count

    # Sentence 1 to write on top of video
    text1 = TextClip(parts_of_meme, font="Montserrat-ExtraBold", color="white", method="caption",
                     size=(1080 - 18 - 18, 200),
                     align="south", kerning=-5).set_position((18, 400 - 10)).set_duration(divider)
    print("First Sentence = ", parts_of_meme)

    for i in range(shift_count):
        # Animation Pattern are logo and meme, fullSize
        # As of now 2 patterns so % 2 is used to select any of the patter
        animation_pattern = i % 2

        # 6 images are scraped from web so % 6 is used to select one among them
        pic_num = i % 6

        img_clip = ImageClip(os.path.dirname(__file__) + "/Data/%s_%d.png" % (date, pic_num))

        # if animation_pattern == 0 then Logo and meme pattern
        if animation_pattern == 0:
            # Background Template
            background = ImageClip(os.path.dirname(__file__) + "/Background/Buddy_Template_Green.png").set_duration(divider)

            # Set vid2 on the greenscreen of the template and resize
            vid2 = img_clip.set_position((54, 603)).set_duration(divider).fx(vfx.resize, (dimension_of_logo_green_temp[::-1]))

            # Add Zoom in effects to the image clip
            vid2 = vid2.fx(vfx.resize, zoom_in).set_position(("center"))

            # Mask the Background
            masked_clip = background.fx(vfx.mask_color, color=green_screen_color, thr=100, s=5)

            # Blend the background and vid2 and text and Produce the clip
            clip = CompositeVideoClip([dummy_back, vid2, masked_clip, text1]).set_fps(24)

        # if animation_pattern == 0 then Logo and meme pattern
        elif animation_pattern == 1:
            # Background Template
            background = ImageClip(os.path.dirname(__file__) + "/Background/Buddy_Template_GreenFull.png").set_duration(divider)

            # vid1 is resized and positioned based on template
            vid1 = img_clip.set_duration(divider).fx(vfx.resize, height=dimension_of_full_green_temp[0]).set_position((x, y))

            # After resize the height and width are noted down in array for calculation
            dimension_of_full_green_resize = [vid1.h, vid1.w]

            # Mask the Background
            masked_clip = background.fx(vfx.mask_color, color=green_screen_color, thr=100, s=5)

            # Blend the background and Produce the clip
            clip = CompositeVideoClip([dummy_back, vid1.set_position(move_left),masked_clip]).set_fps(24)

        # Stock Video is inserted only after 1st clip so. if i == 0 then add stock video to end of it
        if i == 0:
            # Stock Video Path
            stock_path = os.path.dirname(__file__) + "/Background/Stock" + str(random.randint(1,5)) + "_Edited.mp4"
            print(stock_path)

            # Resize stock video to logo template green screen
            stock = VideoFileClip(stock_path).fx(vfx.resize, (dimension_of_logo_green_temp[::-1])).set_position((54, 603))

            # Text is added to stock video to maintain the template
            stock = CompositeVideoClip([background.fx(vfx.mask_color, color=green_screen_color, thr=100, s=5).set_duration(stock.duration),stock, text1.set_duration(stock.duration)])

            # Stock video is added at end of clip
            clip = concatenate([clip, stock], method="compose")

        # Clip is added to final
        final.append(clip)

        # Image is extracted and added
        img_of_each_clip.append(clip.to_ImageClip())

    # Transition layer will contain all the effects and clips
    transition_layer = ColorClip(color=(0, 0, 0), size=(1080, 1920)).set_duration(0)

    # On previous version clips are simply merged.
    # Now Clips are merged with effects
    for i in range(len(final) - 1):
        # As of now 5 Transition green screen clips are store so 1 to 5 any random effect is selected
        effects = VideoFileClip(os.path.dirname(__file__) + f"/Background/TransitionClip%d.mp4" % random.randint(1, 5))

        # The effects has to start with end of current iteration clip ie final[i] and mask green is removed
        effects = effects.set_start(final[i].duration - 0.5).fx(vfx.mask_color, color=(47, 163, 43), thr=100, s=5)

        # Current Clip is concated with next clip image to have a static view till the effect is over
        clip_inst = concatenate([final[i], img_of_each_clip[i + 1].set_duration(effects.duration - 0.5)])

        # Effect and clip is combined
        clip_with_effect = CompositeVideoClip([clip_inst, effects])

        # clip with effect is concated with transition layer
        transition_layer = concatenate([transition_layer, clip_with_effect])

    # Last clip is added with transition without effect and named as out
    out = concatenate([transition_layer, final[-1]])
    out = CompositeVideoClip([out, text1]).set_duration(shift_count * divider)

    # Audio is implated and exported
    out = out.set_audio(CompositeAudioClip([audio, back.set_duration(divider * shift_count)]).set_duration(divider * shift_count))
    out.write_videofile(os.path.dirname(__file__) + "/%s.mp4" % date, fps=24)


date ="".join(str(datetime.date.today()).split("-"))
f = open(os.path.dirname(__file__) + "/Data/" + date + "_meme.txt", "r")
content = f.read()
print(content)
parts_of_meme = content[1:-1].upper()
print("Parts :", len(parts_of_meme), parts_of_meme)
make_video()

browser = StartBrowser.Start_Lap("EntertainBuddy")

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
        break
