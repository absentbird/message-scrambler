from flask import Flask, render_template, request
from english_words import get_english_words_set
import json
import random
import re
import string

app = Flask(__name__)

wordlist = list(get_english_words_set(['web2'], lower=True))
GAPMIN = 2 # Minimum number of non-matching letters
HITRATE = 0.5 # Ratio of matching to non-matching

def suitable(characters, word):
    gaps = 0
    hits = []
    index = 0
    # Check which letters fit into the word and record their indices
    for position, char in enumerate(word):
        if index >= len(characters):
            gaps += 1
            continue
        tomatch = characters[index]
        if char == tomatch:
            hits.append(position)
            index += 1
        else:
            gaps += 1
    score = len(hits)
    # Give score preference to fewer words
    if score == len(characters):
        score += 1
    ratio = score * 1.0 / len(word)
    if ratio >= HITRATE and gaps > GAPMIN:
        return hits
    return []

def scramble(text):
    text = text.replace(' ', '').lower()
    gibberish = ''
    keys = []
    while len(text) > 0:
        word = random.choice(wordlist)
        fit = suitable(text, word)
        while len(fit) == 0:
            word = random.choice(wordlist)
            fit = suitable(text, word)
        for key in fit:
            keys.append(key+len(gibberish))
        text = text[len(fit):]
        gibberish += word + ' '
    return (gibberish[:-1], keys)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/scramble")
def new_scramble():
    text = request.args.get('text').lower().strip()
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    color = request.args.get('color')
    if not color:
        color = '#a020ef'
    words = []
    if len(text) > 0:
        for word in text.split():
            words.append(scramble(word))
    print(words)
    return render_template(
        "scramble.html",
        words=json.dumps(words),
        color=color,
    )

if __name__ == "__main__":
    app.run(debug=True)
