import tone
import parse
import json


conversations = parse.parsefile("matrix.txt")

for conversation in conversations:
    tones = tone.analyze(conversation["text"])

    conversation["tones"] = tones

file = open("scene.txt", "w")
file.write(json.dumps(conversations, ensure_ascii=False))
file.close()