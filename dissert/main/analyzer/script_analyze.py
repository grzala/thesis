import tone
import parse
import json
import db
import sys
import pprint

conversations = [
        {'text': " I hate this place.  This zoo. This prison.  This reality, whatever you want to call it, I can't stand it any longer.  It's the smell, if there is such a thing.  I feel saturated by it.  I can taste your stink and every time I do, I fear that I've somehow been infected by it.", 
        'character': 'AGENT SMITH',
        'tones': [{'score': 0.986412, 'name': u'frustrated'}, {'score': 0.91887, 'name': u'impolite'}, {'score': 0.836783, 'name': u'sad'}]},
        {'text': " Repulsive, isn't it?", 
        'character': 'AGENT SMITH', 
        'tones': []},
        {'text': ' I must get out of here, I must get free.  In this mind is tlie key. My key.', 
        'character': 'AGENT SMITH', 
        'tones': [{'score': 0.613018, 'name': u'sad'}]},
]

conversations = parse.parsefile(sys.argv[1])


for conversation in conversations:
    tones = tone.analyze(conversation["text"])

    conversation["tones"] = tones

def normalize_emotions(conversation):
    tones = {}
    for tone in conversation['tones']:
        tones[tone['name']] = tone['score']

    newtones = {}
    newtones['anger'] = tones['anger']
    newtones['fear'] = tones['fear']
    newtones['joy'] = tones['joy']
    newtones['disgust'] = tones['disgust']
    newtones['surprise'] = 0.0
    newtones['sadness'] = tones['sadness']
    conversation['tones'] = newtones

    if newtones['anger'] > 0.2:
        newtones["joy"] /= 4.0

def analyze_repeating(conversations):
    previously_used = []
    for conversation in conversations:
        clipcopy = list(conversation['clip'])
        lastindex = 0
        for clip in conversation['clip']:
            if clip['name'] not in previously_used:
                break
            lastindex += 1

        newclip = conversation['clip'][lastindex]
        if newclip['score'] >= 0.2:
            conversation['clip'] = [newclip]
        else: 
            conversation['clip'] = [conversation['clip'][0]]
        previously_used.append(conversation['clip'][0]['name'])

        print("FINAL CHOICE:", conversation["text"], "ANIM:", conversation['clip'][0]['name'])
        for clip in clipcopy:
            print clip["name"], ", ",
        print()


for conversation in conversations:
    normalize_emotions(conversation)

for conversation in conversations:
    conversation['clip'] = db.get_matching_gestures(conversation["text"], conversation['tones'])

analyze_repeating(conversations)


file = open("scene.json", "w")
file.write(json.dumps(conversations, ensure_ascii=False, indent=4))
file.close()

print("output: scene.json")