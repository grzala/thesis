# -*- coding: utf-8 -*-
import csv

file = open('dataset.txt', 'w')

i = 0
with open('isear.csv', 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter='|', quotechar='|')
    for row in spamreader:
        emo = row[36]
        sentence = row[-3]
        print emo + ' ' + sentence
        print i
        i += 1
        file.write(sentence.replace("á", "") + ' || ' + emo + "\n")

file.close()