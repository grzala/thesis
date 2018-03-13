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
                "file": "todo/" + f
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


text = {
    "text": "test",
    "character": "AGENT SMITH",
    "clip": [
        {
            "name": "test",
            "file": "todo/" + onlyfiles[0]
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

file = open("showcase.json", "w")
file.write(json.dumps(conversation, ensure_ascii=False, indent=4))
file.close()