import datetime
import os.path
import random
import time
from moviepy.editor import *
import moviepy.video.fx.all as vfx
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from pilmoji.source import FacebookEmojiSource
from pilmoji import Pilmoji
from PIL import Image, ImageFont
import StartBrowser


def image_for_all_sentence(no_of_sentence):
    print("No of Sentence : %d" % no_of_sentence)

    for i in range(no_of_sentence):
        # sp1 - Speaker 1
        sp1 = AudioFileClip(os.path.dirname(__file__) + "/Data/" + date + "_" + str(i) + "sp1.wav").duration

        # one image per second so audio divided by time of each image
        no_of_img_per_sentence = int(sp1 // no_of_img_per_second)
        print(f"no_of_img_per_second : {no_of_img_per_sentence}")
        additional_images(no_of_img_per_sentence, i)


def additional_images(no_of_img_per_sentence=2, sentence_no=0):
    f = open(os.path.dirname(__file__) + "/Data/" + date + "_img.txt")
    prompts = f.readlines()
    # img_desc = "The ruling could require Apple to allow developers to provide external payment options"
    browser.get("https://www.google.com/imghp")
    browser.find_element(By.XPATH, "//textarea[@title='Search']").click()
    browser.find_element(By.XPATH, "//textarea[@title='Search']").send_keys(
        prompts[sentence_no].replace('"', '') + "\n")
    all_img = browser.find_elements(By.XPATH, '//div[@class="wIjY0d jFk0f"]//img')
    c = 0
    for i in all_img[::2]:
        try:
            i.click()
            time.sleep(4)
            url = browser.find_elements(By.XPATH, '//img[@class="sFlh5c pT0Scc iPVvYb"]')
            for j in url:
                if "http" in j.get_attribute("src"):
                    pic_name = os.path.dirname(__file__) + "/Data/%s_%d%d" % (date, sentence_no, c) + ".png"
                    j.screenshot(pic_name)
                    c += 1
                    print(f"downloaded - %d %d" % (sentence_no, c))
                    break
        except Exception as e:
            print(e)
            continue
        if c == no_of_img_per_sentence:
            break


def subtitle(no_of_sentence):
    f = open(os.path.dirname(__file__) + "/Data/" + date + "_script.txt", "r")
    content = f.readlines()
    for c, i in enumerate(content):
        # Subtitle box size
        box = (1060, 600)

        # Font size is high and reduced later
        font_size = 100
        with Image.open(os.path.dirname(__file__) + "/Background/subtitle_background.jpg") as image:

            image = image.convert('RGBA')
            # Split the image into its components
            r, g, b, a = image.split()
            # Adjust the alpha channel
            a = a.point(lambda p: p * 0.1)
            # Merge the channels back
            image = Image.merge("RGBA", (r, g, b, a))

            font = ImageFont.truetype('Montserrat Extra Bold.otf', font_size)
            # Break the sentence into words and add New line at middle or at every 3 words
            words = i.split()
            occupy = 0
            for word in range(len(words)):
                if occupy > 15:
                    words.insert(word, '\n')
                    occupy = 0
                occupy += len(words[word])

            # split_range = 5
            # for word in range(split_range, len(words), split_range):
            #     words.insert(word, '\n')
            print(words)
            # Pilmoji is used to place emoji in image
            with Pilmoji(image, source=FacebookEmojiSource) as pilmoji:
                text = " ".join(words)
                size = pilmoji.getsize(text, spacing=40, emoji_scale_factor=2, font=font)

                # Loops till the font is small that fits exactly inside the box
                while size[0] > box[0] or size[1] > box[1]:
                    font_size -= 2
                    font = ImageFont.truetype('Montserrat Extra Bold.otf', font_size)
                    size = pilmoji.getsize(text, spacing=40, emoji_scale_factor=2, font=font)
                # print(size,box,((box[0] - size[0]) // 2, (box[1] - size[1]) // 2))
                # (box[0] - size[0]) // 2, (box[1] - size[1]) // 2) Middle of the box calc
                pilmoji.text(((box[0] - size[0]) // 2, (box[1] - size[1]) // 2), text, (255, 255, 0), font,
                             stroke_fill="black", stroke_width=7, spacing=40, emoji_scale_factor=2 )
            # For a better look
            # image = image.rotate(angle=random.randint(-3, 3), fillcolor="white",
            #                      center=((box[0] - size[0]) // 2, (box[1] - size[1]) // 2))

            image.save(os.path.dirname(__file__) + "/Data/" + f"{date}_sub{c}.png")
            c += 1


def make_video(no_of_sentence, i):
    sp1 = AudioFileClip(os.path.dirname(__file__) + "/Data/" + date + "_" + str(i) + "sp1.wav")
    # Pop and Click Sound
    # sound_effects = AudioFileClip(
    #     os.path.dirname(__file__) + "/Background/" + f"Sound_Effects%d.mp3" % random.randint(4, 5))
    image_per_sentence = int(sp1.duration // no_of_img_per_second)
    avatar_flag = 1 # 0 if i == no_of_sentence - 1 else 1
    if avatar_flag == 0:
        global avatar
        sp2 = AudioFileClip(os.path.dirname(__file__) + "/Data/" + date + "_" + str(i) + "sp2.wav").set_start(
            sp1.duration)
        avatar = VideoFileClip(os.path.dirname(__file__) + "//Background/EntertainBuddyAvatar.mp4").set_start(
            sp1.duration).set_duration(sp2.duration).fx(vfx.mask_color, color=(255, 0, 0), thr=100, s=5)
        avatar = avatar.set_position("center")
        audio = concatenate_audioclips([sp1, sp2])
    else:
        audio = sp1

    # Consider 5 images for one sentence. This clip collection will have 5 video of var-image_per_second
    clip_collection = []
    canva = ColorClip(color=(0, 0, 0), size=(1080, 1920)).set_duration(no_of_img_per_second).set_fps(24)
    for j in range(image_per_sentence):
        path = os.path.dirname(__file__) + "/Data/" + date + "_" + str(i) + str(j) + ".png"

        center_image = ImageClip(path).fx(vfx.resize, width=1080)
        center_image = center_image.set_duration(no_of_img_per_second).set_fps(24).set_position(
            (1080 / 2 - center_image.w / 2, 1920 / 2 - center_image.h / 2))

        background_img = center_image.fx(vfx.resize, height=1920)
        background_img = background_img.set_position((1080 / 2 - background_img.w / 2, 0)).set_duration(
            no_of_img_per_second).set_fps(24)

        out = CompositeVideoClip([canva, background_img, center_image])
        clip_collection.append(out)

    clip = concatenate_videoclips(clip_collection)
    overlay_mask_color = (0, 165, 86)
    overlay = VideoFileClip(
        os.path.dirname(__file__) + f"/Background/OverLayClip%d.mp4" % random.randint(1, 3)).set_duration(
        clip.duration)
    clip = CompositeVideoClip(
        [clip, overlay.fx(vfx.mask_color, color=overlay_mask_color, thr=100, s=5).fx(vfx.resize, (1080, 1920))])
    if avatar_flag == 0:
        clip = CompositeVideoClip([clip, avatar])

    sub_position = (10, 800)
    sub = ImageClip(os.path.dirname(__file__) + "/Data/" + f"{date}_sub{i}.png").set_duration(audio.duration-1)
    sub = sub.set_position(sub_position)

    clip = CompositeVideoClip([clip, sub])
    audio = CompositeAudioClip([audio, clip.audio])
    clip = clip.set_audio(audio)
    img_of_each_clip.append(clip.to_ImageClip())

    clip.write_videofile(os.path.dirname(__file__) + "/Data/%s_sentence%d.mp4" % (date, i), fps=24)


def add_transition(no_of_sentence):
    # Transition layer will contain all the effects and clips
    transition_layer = ColorClip(color=(0, 0, 0), size=(1080, 1920)).set_duration(0)

    # On previous version clips are simply merged.
    # Now Clips are merged with effects
    for i in range(no_of_sentence - 1):
        # As of now 5 Transition green screen clips are store so 1 to 5 any random effect is selected
        # effects = VideoFileClip(
        #     os.path.dirname(__file__) + f"/Background/TransitionClip%d.mp4" % random.randint(3, 5)).fx(vfx.resize,
        #                                                                                                (1080, 1920))
        video = VideoFileClip(os.path.dirname(__file__) + "/Data/%s_sentence%d.mp4" % (date, i))
        # The effects has to start with end of current iteration clip ie final[i] and mask green is removed
        # effects = effects.set_start(video.duration - 0.5).fx(vfx.mask_color, color=(47, 163, 43), thr=100, s=5)

        # clip with effect is concated with transition layer
        transition_layer = concatenate([transition_layer, video])

    # Last clip is added with transition without effect and named as out
    out = concatenate([transition_layer,
                       VideoFileClip(os.path.dirname(__file__) + "/Data/%s_sentence%d.mp4" % (date, no_of_sentence - 1))
                       ])

    background = AudioFileClip(os.path.dirname(__file__) + "/Background/Background_Reduced.mp3")
    out_audio = CompositeAudioClip([out.audio, background.set_duration(out.duration)])
    out = out.set_audio(out_audio)

    # Audio is implated and exported
    out.write_videofile(os.path.dirname(__file__) + "/%s.mp4" % date, fps=24)


def find_total_lines():
    lines = open(os.path.dirname(__file__) + "/Data/" + date + "_script.txt", 'r').readlines()
    for i in lines:
        if len(i) < 3:
            lines.remove(i)
    return len(lines)


def delete_old_video():
    # Delete Old final video
    l = os.listdir(os.path.dirname(__file__))
    for i in l:
        if ".mp4" in i:
            os.remove(os.path.dirname(__file__) + "/" + i)


date = "".join(str(datetime.date.today()).split("-"))

no_of_img_per_second = 1
final = []
img_of_each_clip = []

no_of_sentence = find_total_lines()

delete_old_video()

# browser = StartBrowser.Start_Lap("EntertainmentBuddy")
# image_for_all_sentence(no_of_sentence)

subtitle(no_of_sentence)
for i in range(no_of_sentence):
    make_video(no_of_sentence, i)
add_transition(no_of_sentence)
