import tone
import parse
import json
import db
import sys
import pprint

# This is the main script of the analyzer module
# Command line arguments - filepath to script to analyze
# This program takes in a script as input, analyzes emotions, matches the animations
# This program outputs a json file instructions of how to assemble the animation


# Ensure emotions are compatible for use by the db.py
def normalize_emotions(conversation):
    # Move the tones to one dictionary instead of a list of dictionaries
    tones = {}
    for tone in conversation['tones']:
        tones[tone['name']] = tone['score']

    newtones = {}
    newtones['anger'] = tones['anger']
    newtones['fear'] = tones['fear']
    newtones['joy'] = tones['joy']
    newtones['disgust'] = tones['disgust']
    newtones['surprise'] = 0.0 # Surprise is not supported by IBM Watson; ensure value is always 0
    newtones['sadness'] = tones['sadness']
    conversation['tones'] = newtones

    # Decrease the value of joy if anger is detected
    # Anger is a more important conflicting emotion that shadows joy
    if newtones['anger'] > 0.2:
        newtones["joy"] /= 4.0

# Ensure animations do not repeat too often
def analyze_repeating(conversations):
    previously_used = []
    for conversation in conversations:
        lastindex = 0
        # Iterate the list of matching animations
        for clip in conversation['clip']:
            if clip['name'] not in previously_used: # Choose the animation that was not yet used
                break
            lastindex += 1

        # Choose betweent the most matching and never previously used animation
        newclip = conversation['clip'][lastindex]
        if newclip['score'] >= 0.2: # If match score is bigger than 0.2, use the never used animation
            conversation['clip'] = [newclip]
        else: # Use the most matching animation
            conversation['clip'] = [conversation['clip'][0]]
        previously_used.append(conversation['clip'][0]['name']) # Remember the names of used animations



def main():
    # Read script from provided file
    conversations = parse.parsefile(sys.argv[1])

    # For each dialogue line analyze emotions
    for conversation in conversations:
        tones = tone.analyze(conversation["text"]) # use tone.py to analyze emotions
        conversation["tones"] = tones

    # Normalize emotions of each dialogue line
    for conversation in conversations:
        normalize_emotions(conversation)

    # Find animations matching each dialogue line
    for conversation in conversations:
        conversation['clip'] = db.get_matching_gestures(conversation["text"], conversation['tones'])

    # Ensure animations do not repeat too often
    analyze_repeating(conversations)

    # Save the instructions to JSON
    file = open("scene.json", "w")
    file.write(json.dumps(conversations, ensure_ascii=False, indent=4))
    file.close()

    print("output: scene.json")

main()