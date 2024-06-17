import emoji
from TTS.api import TTS
import os
import datetime

date = "".join(str(datetime.date.today()).split("-"))

f = open(os.path.dirname(__file__) + "//Data//" + date + "_script.txt", "r")
content = f.readlines()


stripped_content = ""


tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2", progress_bar=False)
path = f"{os.path.dirname(__file__)}/Data/{date}"


for i in range(len(content)):
    for char in content[i]:
        if not emoji.is_emoji(char):
            stripped_content += char
    if len(stripped_content) > 3:
        tts.tts_to_file(text=stripped_content, file_path=path + "_" + str(i) + "sp1.wav", language='en',
                        speaker_wav=os.path.dirname(__file__) + "/Audio_train_Boy.wav")
    stripped_content = ""
    print(stripped_content)
