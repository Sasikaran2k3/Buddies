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
from PIL import Image, ImageDraw, ImageFont
import numpy as np


def ErrorCorrection():
    template = ImageClip(os.path.dirname(__file__) + "/Background/Buddy_Template_Green.png")
    effects = VideoFileClip(os.path.dirname(__file__) + f"/Background/TransitionClip%d.mp4" % 5)
    effects.fx(vfx.resize, (1080, 1920))
    effects.write_videofile(os.path.dirname(__file__) + f"/Background/TransitionClip%d.mp4" % 5)
    quit()


#ErrorCorrection()

def additional_images():
    f = open(os.path.dirname(__file__) + "/Data/" + date + "_img.txt")
    prompts = f.readlines()
    for k in range(len(prompts)):
        # img_desc = "The ruling could require Apple to allow developers to provide external payment options"
        browser.get("https://www.google.com/imghp")
        browser.find_element(By.XPATH, "//textarea[@title='Search']").click()
        browser.find_element(By.XPATH, "//textarea[@title='Search']").send_keys(prompts[k].replace('"', '') + "\n")
        all_img = browser.find_elements(By.XPATH, '//div[@class="wIjY0d jFk0f"]//img')
        c = 0
        for i in all_img[::2]:
            i.click()
            time.sleep(4)
            url = browser.find_elements(By.XPATH, '//div[@class="p7sI2 PUxBg"]//img')
            for j in url:
                if "http" in j.get_attribute("src"):
                    try:
                        pic_name = os.path.dirname(__file__) + "/Data/%s_%d%d" % (date, k, c) + ".png"
                        j.screenshot(pic_name)
                        c += 1
                        print(f"downloaded - %d %d" % (k, c))
                        break
                    except:
                        continue
            if c == 2:
                break


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
    for _ in range(8):
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
    wait = WebDriverWait(browser, 1000)
    wait.until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, 'div[class = "common-module_smallControlButton_xMfva ExportRow-module_buttonStyle_K-mdn ExportRow-module_studioColor_Xf7VQ"]')))
    browser.find_element(By.CSS_SELECTOR, 'div[class = "common-module_smallControlButton_xMfva ExportRow-module_buttonStyle_K-mdn ExportRow-module_studioColor_Xf7VQ"]').click()
    print("Download Page")

    # Waits till the size of the file appears and then dowload button is clicked
    time.sleep(5)
    wait.until(expected_conditions.visibility_of_element_located(
        (By.XPATH, '//div[@class="VideoContainer-module_commentsMetaDataFileSize_6KG5K"]')))
    time.sleep(5)
    print("Download Available")
    while True:
        no_of_item = len(os.listdir(os.path.dirname(__file__) + "/Data"))
        wait.until(expected_conditions.visibility_of_element_located((By.XPATH, '//span[text() = "Download file" ]')))
        browser.find_element(By.XPATH, '//span[text() = "Download file" ]').click()
        time.sleep(3)
        if os.listdir(os.path.dirname(__file__) + "/Data") != no_of_item:
            print("Download Started")
            time.sleep(60)
            break
    print("Download Completed Successfully")
    print("Kapwing Closed")


def make_video():
    def video_editor(i, j, no_of_img_per_sentence, audio_duration):
        time_limit = audio_duration / no_of_img_per_sentence

        path = os.path.dirname(__file__) + "/Data/" + date + "_" + str(i) + str(j) + ".png"

        canva = ColorClip(color=(0, 0, 0), size=(1080, 1920))

        center_image = ImageClip(path).fx(vfx.resize, width=1080)
        center_image = center_image.set_duration(time_limit).set_fps(24).set_position(
            lambda t: shaking_position(t, size=[center_image.w, center_image.h]))

        background_img = center_image.fx(vfx.resize, height=1920)
        background_img = background_img.set_position((1080 / 2 - background_img.w / 2, 0)).set_duration(
            time_limit).set_fps(24)

        global out
        if i % 2 != 0 and j != 1:
            print("effect 1 pan")
            temp = ImageClip(path).fx(vfx.resize, width=(1080 * 1.5)).set_duration(time_limit).set_fps(24)

            out = out = CompositeVideoClip(
                [canva.set_duration(time_limit),
                 ImageClip(path).fx(vfx.resize, width=1080, height=1920).set_position(
                     (1080 / 2 - background_img.w / 2, 0)).set_duration(time_limit).set_fps(24)
                 .set_position(lambda t: (-(t / time_limit) * (temp.w - 1080), 1920 / 2 - temp.h / 2))
                 ]
            )
        elif j == 0:
            print("effect 2 shake")

            out = CompositeVideoClip(
                [canva.set_duration(time_limit),
                 ImageClip(path).fx(vfx.resize, width=1080, height=1920).set_position(
                     (1080 / 2 - background_img.w / 2, 0)).set_duration(time_limit).set_fps(24),
                 ImageClip(path).fx(vfx.resize, width=1080).set_duration(time_limit).set_fps(
                     24).set_position(lambda t: shaking_position(t, size=center_image.size))
                 ]
            )
        else:
            print("effect 3 zoom")

            out = CompositeVideoClip(
                [canva.set_duration(time_limit),
                 ImageClip(path).fx(vfx.resize, width=1080, height=1920).set_position(
                     (1080 / 2 - background_img.w / 2, 0)).set_duration(time_limit).set_fps(
                     24),
                 ImageClip(path).fx(vfx.resize, width=1080).set_duration(
                     time_limit).set_fps(
                     24).fx(vfx.resize, zoom_in).set_position(("center"))
                 ]
            )
        overlay_mask_color = (0, 165, 86)
        overlay = VideoFileClip(
            os.path.dirname(__file__) + f"/Background/OverLayClip%d.mp4" % random.randint(1, 3)).set_duration(
            out.duration)
        out = CompositeVideoClip(
            [out, overlay.fx(vfx.mask_color, color=overlay_mask_color, thr=100, s=5).fx(vfx.resize, (1080, 1920))])
        return out

    def shaking_position(t, freq=1, magnitude=10, size=[0, 0]):
        x_offset = magnitude * np.sin(freq * 2 * np.pi * t)
        y_offset = magnitude * np.cos(freq * 2 * np.pi * t)
        return 1080 / 2 - x_offset - size[0] / 2, 1920 / 2 - y_offset - size[1] / 2

    def move_left(t):
        # t/divider give a percentage like 0 to 100%
        # width of resized img - width of template - x which is gap from 0 to template position.
        # This will stop video when image touches the end and not let the img leave the canva fully
        # concept is 0-100% of total width is displayed as video.
        # if t is 1 and duration is 2 then 50% of width of the img is the position and
        # if t is 2 then 100% of width of img is covered
        posi = -(t / (2)) * (dimension_of_full_green_resize[1] - dimension_of_full_green_temp[1] - x), y
        return posi

    def zoom_in(t):
        # Zoom in effect
        # t is very small so to have a zooming factor we add 1
        # 0.15 is for speed
        # if t is 1 second the zoom is 1.15 and if t is 2 then 1.3
        return 1 + t * 0.15

    lines = open(os.path.dirname(__file__) + "/Data/" + date + "_script.txt", 'r').readlines()
    for i in lines:
        if len(i) < 3:
            lines.remove(i)
    no_of_sentence = len(lines)
    print(no_of_sentence)
    no_of_img_per_sentence = 2

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

    # Sentence 1 to write on top of video
    # text1 = TextClip(parts_of_meme, font="Montserrat-ExtraBold", color="white", method="caption",
    #                  size=(1080 - 18 - 18, 200),
    #                  align="south", kerning=-5).set_position((18, 400 - 10)).set_duration(divider)
    # print("First Sentence = ", parts_of_meme)
    #d = 0
    for i in range(no_of_sentence):
        sp1 = AudioFileClip(os.path.dirname(__file__) + "/Data/" + date + "_" + str(i) + "sp1.wav")
        effect = AudioFileClip(os.path.dirname(__file__) + f"/Background/Sound_Effects%d.mp3" % random.randint(1, 3))
        back = concatenate_audioclips([effect])
        sound_effects = AudioFileClip(os.path.dirname(__file__) + "/Background/" + f"Sound_Effects%d.mp3" % random.randint(4, 5))

        audio = sp1

        # Always Have Second Voice
        animation_pattern = 0 # i%2 every 2 sentences

        clip_collection = []

        # if animation_pattern == 0 then Logo and meme pattern
        if animation_pattern == 0:
            global avatar
            sp2 = AudioFileClip(os.path.dirname(__file__) + "/Data/" + date + "_" + str(i) + "sp2.wav")
            avatar = VideoFileClip(os.path.dirname(__file__) + "/Background/EntertainBuddyAvatar.mp4").set_start(
                sp1.duration).set_duration(sp2.duration).fx(vfx.mask_color, color=(255, 0, 0), thr=100, s=5)
            avatar = avatar.set_position("center")
            audio = concatenate_audioclips([sp1, sound_effects, sp2])

        for j in range(no_of_img_per_sentence):
            out = video_editor(i, j, no_of_img_per_sentence, audio.duration)
            out = out.set_audio(sound_effects.set_start(out.duration - 0.5))
            clip_collection.append(out)
        clip = concatenate_videoclips(clip_collection)

        if animation_pattern == 0:
            clip = CompositeVideoClip([clip, avatar])
        audio = CompositeAudioClip([audio, back.set_duration(audio.duration), clip.audio])
        audio = concatenate_audioclips([audio, sound_effects])
        clip = clip.set_audio(audio)

        # Clip is added to final
        final.append(clip)

        # Image is extracted and added
        img_of_each_clip.append(clip.to_ImageClip())
        # d+=1
        # if d == 2:
        #     break
    # Transition layer will contain all the effects and clips
    transition_layer = ColorClip(color=(0, 0, 0), size=(1080, 1920)).set_duration(0)

    # On previous version clips are simply merged.
    # Now Clips are merged with effects
    for i in range(len(final) - 1):
        # As of now 5 Transition green screen clips are store so 1 to 5 any random effect is selected
        effects = VideoFileClip(
            os.path.dirname(__file__) + f"/Background/TransitionClip%d.mp4" % random.randint(3, 5)).fx(vfx.resize,
                                                                                                       (1080, 1920))

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

    background = AudioFileClip(os.path.dirname(__file__) + "/Background/Background_Reduced.mp3")
    out_audio = CompositeAudioClip([out.audio, background.set_duration(out.duration)])
    out = out.set_audio(out_audio)

    # Audio is implated and exported
    out.write_videofile(os.path.dirname(__file__) + "/%s.mp4" % date, fps=24)


# Delete Old final video
l = os.listdir(os.path.dirname(__file__))
for i in l:
    if ".mp4" in i:
        os.remove(os.path.dirname(__file__) + "/" + i)


date = "".join(str(datetime.date.today()).split("-"))

browser = StartBrowser.Start_Lap("EntertainmentBuddy")
additional_images()

make_video()

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
