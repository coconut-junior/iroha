import random
import colors

present_verbs = ['laughing', 'grinning', 'yawning', 'staring']
passive_verbs = ['sighs', 'laughs', 'winks', 'whistles']
actions = ['strokes', 'touches', 'grabs', 'kicks', 'punches']
nouns = ['you']
structures = ["$action $noun1 why did you do that?", "$verb1 while $verb2", "$verb1 and $action $noun1"]

def getResponse(text):
    global present_verbs
    global passive_verbs
    global actions
    global nouns

    sentence = text.split(' ')
    print(sentence)
    if sentence[1] == 'you':
        answers = [sentence[0] + ' you back', sentence[0] + ' you harder']
    elif sentence[1] == 'at' and 'you' in text:
        answers = ['looks away, embarrassed', 'looks back at you']
    elif sentence[1] == 'ur':
        struct = structures[random.randint(0,len(structures)-1)]
        struct = struct.replace("$noun1", sentence[2])
        v1 = passive_verbs[random.randint(0,len(passive_verbs)-1)]
        v2 = present_verbs[random.randint(0,len(present_verbs)-1)]
        action = actions[random.randint(0,len(actions)-1)]
        struct = struct.replace("$verb1", v1)
        struct = struct.replace("$verb2", v2)
        struct = struct.replace("$action", action)
        answers = [struct]
    else:
        answers = ['looks around, confused']

    return answers
