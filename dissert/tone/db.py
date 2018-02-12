import sqlite3, operator

con = sqlite3.connect("animation.db")

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

def get_quety_string(emotion):
    return "SELECT * FROM animations WHERE animations." + emotion + " > 0.0"

def get_matching_gestures(emotions):
    sorted_emo = sorted(emotions.items(), key=operator.itemgetter(1))[::-1][:2:]

    con.row_factory = dict_factory
    cur = con.cursor()
    
    retrieved = []
    cur.execute(get_quety_string(sorted_emo[0][0]))
    retrieved.append(cur.fetchall())
    cur.execute(get_quety_string(sorted_emo[1][0]))
    retrieved.append(cur.fetchall())
    retrieved = remove_duplicates(retrieved)

    return retrieved

emos = {
    'joy': 0.0,
    'anger': 0.1,
    'fear': 0.9,
    'surprise': 0.2,
    'sadness': 0.6,
    'disgust': 0.1,
}

print get_matching_gestures(emos)