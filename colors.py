import random

def get():
    c = ['red', 'blue', 'green', 'yellow', 'orange', 'pink', 'purple', 'green', 'black', 'white'/
            'grey', 'yellow', 'brown', 'light blue', 'light green']
    selected_color = c[random.randint(0, len(c)-1)]
    if random.randint(0,1)==1:
        selected_color += 'ish'
    return selected_color
