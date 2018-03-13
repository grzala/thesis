from os import listdir
from os.path import isfile, join
import sys
import json

onlyfiles = [f for f in listdir(sys.argv[1]) if isfile(join(sys.argv[1], f))]
print onlyfiles

conversation = []

for f in onlyfiles:
    name = f.split(" ")[0]
    text = {
        "text": f,
        "character": "AGENT SMITH",
        "clip": [
            {
                "name": name,
                "file": f
            }
        ],
        "tones": {
            "joy": 0.0,
            "sadness": 0.0,
            "disgust": 0.0,
            "anger": 0.0,
            "surprise": 0.0,
            "fear": 0.0
        }
    }
    conversation.append(text)


textendtext = {
    "text": "test",
    "character": "AGENT SMITH 2",
    "clip": [
        {
            "name": "test",
            "file": onlyfiles[0]
        }
    ],
    "tones": {
        "joy": 0.0,
        "sadness": 0.0,
        "disgust": 0.0,
        "anger": 0.0,
        "surprise": 0.0,
        "fear": 0.0
    }
}

j = 0
for i in range(0, len(conversation), 10):
    starti = i
    endi = i+10
    if (endi >= len(conversation)):
        endi = len(conversation)-1
    con = conversation[starti:endi]

    file = open("showcases/showcase"+str(j)+".json", "w")
    file.write(json.dumps(con, ensure_ascii=False, indent=4))
    file.close()
    j += 1