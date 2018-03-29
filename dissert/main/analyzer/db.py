import sqlite3, operator

RELEVANCY_THRESHOLD = 0.2
WORDS_PER_SECOND = 2.1
FRAMES_PER_SECOND = 24.0

con = sqlite3.connect("animation.db")
neutral_query_string = "SELECT * FROM animations WHERE \
                                    animations.joy <= 0.0 AND \
                                    animations.sadness <= 0.0 AND \
                                    animations.surprise <= 0.0 AND \
                                    animations.disgust <= 0.0 AND \
                                    animations.anger <= 0.0 AND \
                                    animations.fear <= 0.0"

def get_speech_len(text):
    return len(text.split(" ")) / WORDS_PER_SECOND

def get_anim_len(frames):
    return frames / FRAMES_PER_SECOND

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def is_in_array(ar, item1):
    for item2 in ar:
        if item2['id'] == item1['id']:
            return True
    return False

def remove_duplicates(result):
    newar = []

    for res in result:
        if not is_in_array(newar, res):
            newar.append(res)

    return newar

def get_query_string(emotion):
    return "SELECT * FROM animations WHERE animations." + emotion + " > 0.0"

def get_score(text, emotions, item, relevant_emotions, neutral = False):
    anim_len = get_anim_len(item["Frames"])
    text_len = get_speech_len(text)
    len_modifier = min(anim_len, text_len) / max(anim_len, text_len)

    if neutral:
        return len_modifier

    difs = []
    for rel in relevant_emotions:
        score0 = emotions[rel]
        score1 = item[rel]
        difs.append(abs(score0 - score1))

    average = 0.0
    for dif in difs:
        average += dif
    average /= len(difs)

    score = 1.0 - average

    score *= len_modifier

    return score 


def get_matching_gestures(text, emotions):
    sorted_emo = sorted(emotions.items(), key=operator.itemgetter(1))[::-1][:2:]
    con.row_factory = dict_factory
    cur = con.cursor()

    if sorted_emo[0][1] <= RELEVANCY_THRESHOLD: #neutral
        cur.execute(neutral_query_string)
        retrieved = cur.fetchall()
        result = []

        for item in retrieved:
            item['score'] = get_score(text, emotions, item, {}, True)
            result.append(item)
        
        return sorted(result, key=lambda res: res['score'])[::-1]
        
    else:
        relevant_emotions = [sorted_emo[0][0]]
        if sorted_emo[1][1] > RELEVANCY_THRESHOLD:
            relevant_emotions.append(sorted_emo[1][0])

        retrieved = []
        for relevant_emo in relevant_emotions:
            cur.execute(get_query_string(relevant_emo))
            retrieved += (cur.fetchall())
        retrieved = remove_duplicates(retrieved)

        result = []
        for item in retrieved:
            item['score'] = get_score(text, emotions, item, relevant_emotions)
            result.append(item)

        return sorted(result, key=lambda res: res['score'])[::-1]


def __main__():

    emos = {
        'joy': 0.0,
        'anger': 0.1,
        'fear': 0.9,
        'surprise': 0.2,
        'sadness': 0.6,
        'disgust': 0.1,
    }

    emos2 = {
        'joy': 0.0,
        'anger': 0.0,
        'fear': 0.0,
        'surprise': 0.0,
        'sadness': 0.0,
        'disgust': 0.0,
    }

    get_matching_gestures("I AM GROOT", emos)


if __name__ == "__main__":
    __main__()