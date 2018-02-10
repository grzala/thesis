from __future__ import print_function
import json
from os.path import join, dirname
from watson_developer_cloud import ToneAnalyzerV3

tone_analyzer = ToneAnalyzerV3(
  version='2017-09-21',
  username='67d2d5fd-57ef-4833-a7c0-b44429221b94',
  password='d7qX61lIE7TT'
)

def analyze(text):
    utterances = [{'text': text}]
    response = tone_analyzer.tone_chat(utterances)
    analysis = []

    for tone in response["utterances_tone"]:
        for t in tone["tones"]:
            newtone = {}
            newtone["name"] = t["tone_id"]
            newtone["score"] = t["score"]
            analysis.append(newtone)

    return analysis

