import os.path
import datetime


date = "".join(str(datetime.date.today()).split("-"))
f = open(os.path.dirname(__file__)+"/Data/"+date+"_script.txt","r")
data = f.read()
f.close()

img_prompt = ""
new_speaker = ""
script = ""
flag = 0
for i in data:
    if i=='[' :
        flag = 1
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
        new_speaker += "\n"
        continue

    if flag == 0:
        script+=i
    elif flag == 1:
        img_prompt += i
    elif flag == 2:
        new_speaker += i

f = open(os.path.dirname(__file__)+"/Data/"+date+"_script.txt","w")
f.write(script)

f = open(os.path.dirname(__file__)+"/Data/"+date+"_img.txt","w")
f.write(img_prompt)

f = open(os.path.dirname(__file__)+"/Data/"+date+"_speaker.txt","w")
f.write(new_speaker)

print(img_prompt+"\n" + new_speaker+"\n" + script)



