from os import listdir
from os.path import isfile, join
import sys
import json

# This scripts creates a 'showcase'
# A showcase is an animation comprised of all clips in a folder
# The purpose of a showcase is to create a video that shows a clip and corresponding filename
# This allows to quickly watch and analyze emotions conveyed by each animation clip

# Get all the files from directory provided through a command line argument
onlyfiles = sorted([f for f in listdir(sys.argv[1]) if isfile(join(sys.argv[1], f))])
print onlyfiles

conversation = []

# Create a dialogue line for each animation clip
for f in onlyfiles:
    name = f.split(" ")[0]
    text = {
        "text": f, # The dialogue line is the animation's name
        "character": "AGENT SMITH",
        "clip": [
            {
                "name": name, # select animation file
                "file": f
            }
        ],
        "tones": { # Tones are irrelevant for generating a showcase but they cannot be null
            "joy": 0.0,
            "sadness": 0.0,
            "disgust": 0.0,
            "anger": 0.0,
            "surprise": 0.0,
            "fear": 0.0
        }
    }
    conversation.append(text)

j = 0
# Split the conversation into many conversations of 10 dialogue lines
# A few shorter scenes are easier to analyze and render than one long scene
for i in range(0, len(conversation), 10):
    starti = i
    endi = i+10
    if (endi >= len(conversation)):
        endi = len(conversation)-1
    con = conversation[starti:endi]

    # Save scenes to files
    file = open("showcases/showcase"+str(j)+".json", "w")
    file.write(json.dumps(con, ensure_ascii=False, indent=4))
    file.close()
    j += 1