import datetime
import os
from transformers import VitsModel, AutoTokenizer
import torch
import scipy

date = "".join(str(datetime.date.today()).split("-"))

model = VitsModel.from_pretrained("facebook/mms-tts-eng")
tokenizer = AutoTokenizer.from_pretrained("facebook/mms-tts-eng")

f = open(os.path.dirname(__file__) + "//Data//" + date + "_script.txt", "r")
content = f.readlines()
stripped_content = ""
for i in content:
    stripped_content += i.strip() + "\n"
    stripped_content = stripped_content

print(stripped_content)
text = stripped_content
inputs = tokenizer(text, return_tensors="pt")

with torch.no_grad():
    output = model(**inputs).waveform

#path = os.path.dirname(__file__) + "//Data//" + str(date) + ".wav"
path = f"{os.path.dirname(__file__)}//Data//{date}.wav"
print(path)
scipy.io.wavfile.write(path, rate=model.config.sampling_rate,
                       data=output.float().numpy().T)
