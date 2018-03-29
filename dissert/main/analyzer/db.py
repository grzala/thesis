import sqlite3, operator

# This script matches the analyzed text with the animations

# Constants
RELEVANCY_THRESHOLD = 0.2 # Emotional score below this value is irrelevant
WORDS_PER_SECOND = 2.1 # Speech speed
FRAMES_PER_SECOND = 24.0 # Animation speed

con = sqlite3.connect("animation.db")
neutral_query_string = "SELECT * FROM animations WHERE \
                                    animations.joy <= 0.0 AND \
                                    animations.sadness <= 0.0 AND \
                                    animations.surprise <= 0.0 AND \
                                    animations.disgust <= 0.0 AND \
                                    animations.anger <= 0.0 AND \
                                    animations.fear <= 0.0"

# Calculate speech length in seconds
def get_speech_len(text):
    return len(text.split(" ")) / WORDS_PER_SECOND

# Calculate animation length in seconds
def get_anim_len(frames):
    return frames / FRAMES_PER_SECOND

# Create dictionary from SQL row
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

# Remove duplicate animation clips
def remove_duplicates(result):
    newar = []

    for res in result:
        if not is_in_array(newar, res):
            newar.append(res)

    return newar

# Search animations by emotion score SQL statement
def get_query_string(emotion):
    return "SELECT * FROM animations WHERE animations." + emotion + " > 0.0"

# Calculate how well animation matches with text
def get_score(text, emotions, item, relevant_emotions, neutral = False):
    anim_len = get_anim_len(item["Frames"])
    text_len = get_speech_len(text)
    len_modifier = min(anim_len, text_len) / max(anim_len, text_len) # Calculate how well anim length matches speech length

    if neutral:
        return len_modifier # If there are no emotions attached to text, choose neutral animation of most matching length

    difs = []
    for rel in relevant_emotions:
        score0 = emotions[rel]
        score1 = item[rel]
        difs.append(abs(score0 - score1)) # Calculate the difference between text's emotion score and amin's emotion score

    # Average out each emotion's score
    average = 0.0
    for dif in difs:
        average += dif
    average /= len(difs)

    score = 1.0 - average # Score represents how well anim's emotions match text's emotions

    score *= len_modifier # Adjust for animation length

    return score 

# Get a list of animations sorted so that the most matching one is first
def get_matching_gestures(text, emotions):
    # Find the most relevant emotions
    sorted_emo = sorted(emotions.items(), key=operator.itemgetter(1))[::-1][:2:]
    con.row_factory = dict_factory
    cur = con.cursor()

    # If the most important emotion is below relevancy, choose neutral animation
    if sorted_emo[0][1] <= RELEVANCY_THRESHOLD:
        cur.execute(neutral_query_string) # Get all neutral anims
        retrieved = cur.fetchall()
        result = []

        for item in retrieved:
            item['score'] = get_score(text, emotions, item, {}, True) # Get score by anim's and text's lengths
            result.append(item)
        
        return sorted(result, key=lambda res: res['score'])[::-1] # Return most matching first
        
    else:
        # Find animations by emotion
        relevant_emotions = [sorted_emo[0][0]]
        if sorted_emo[1][1] > RELEVANCY_THRESHOLD: # If second most relevant emotion is above relevancy, use it
            relevant_emotions.append(sorted_emo[1][0])

        retrieved = []
        for relevant_emo in relevant_emotions:
            cur.execute(get_query_string(relevant_emo))
            retrieved += (cur.fetchall())
        retrieved = remove_duplicates(retrieved)

        # Calculate scores for retrieved animations
        result = []
        for item in retrieved:
            item['score'] = get_score(text, emotions, item, relevant_emotions)
            result.append(item)

        return sorted(result, key=lambda res: res['score'])[::-1] # Returned sorted animation clips (most relevant first)


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