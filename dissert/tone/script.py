import tone
import parse


conversations = parse.parsefile("matrix.txt")

for conversation in conversation:
    tones = tone.analyze(conversation["text"])

    print(conversation["character"] + " said: " + conversation["text"])