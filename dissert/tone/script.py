import tone
import parse
import json
import db

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

conversations = parse.parsefile("matrix.txt")

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

for conversation in conversations:
    normalize_emotions(conversation)

for conversation in conversations:
    conversation['clip'] = db.get_matching_gestures(conversation['tones'])

file = open("scene.txt", "w")
file.write(json.dumps(conversations, ensure_ascii=False))
file.close()