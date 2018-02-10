import os

file2 = open('dataset2.csv', 'w')
i = 0
for filename in os.listdir(os.getcwd()): 
    if filename[-4:len(filename)] != '.txt':
        continue
    file = open(filename, 'r')

    if "ANGER" in filename:
        emo = "anger"
    elif "JOY" in filename:
        emo = "joy"
    elif "FEAR" in filename: 
        emo = "fear"
    elif "LOVE" in filename:
        emo = "love"
    elif "SADNESS" in filename:
        emo = "sadness"
    elif "SURPRISE" in filename:
        emo = "surprise"
    
    for line in file:
        line = line.replace("\n", "")
        line = line.replace("\r", "")
        if not line.isspace() and line != '':
            print emo + ' || ' + line
            file2.write(emo + ' || ' + line + "\n")

            i += 1

print str(i) + ' sentences'