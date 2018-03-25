from __future__ import print_function
import json
from os.path import join, dirname
from watson_developer_cloud import ToneAnalyzerV3

tone_analyzer = ToneAnalyzerV3(
  version='2016-05-19',
  username='67d2d5fd-57ef-4833-a7c0-b44429221b94',
  password='d7qX61lIE7TT'
)

def analyze(text):
    utterances = [{'text': text}]
    response = tone_analyzer.tone(tone_input=text, content_type="text/plain")

    analysis = []

    for tone in response['document_tone']['tone_categories'][0]['tones']:
        newtone = {}
        newtone["name"] = tone["tone_id"]
        newtone["score"] = tone["score"]
        analysis.append(newtone)
    

    return analysis

def __main__():
    text = "I have to go now."
    print(analyze(text))


if __name__ == "__main__":
    __main__()

