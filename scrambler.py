import random
import sys
from english_words import get_english_words_set
from PIL import Image, ImageDraw, ImageFont

wordlist = list(get_english_words_set(['web2'], lower=True))
GAPMIN = 2
HITRATE = 0.5

def suitable(characters, word):
    gaps = 0
    hits = []
    index = 0
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
    if score == len(characters):
        score += GAPMIN
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

text = 'example'
output = 'scramble.png'
if len(sys.argv) > 1:
    text = sys.argv[1]
    if len(sys.argv > 2):
        output = sys.argv[2]
words = []
longest = 0
for word in text.split():
    words.append(scramble(word))

font_path = 'LiberationMono-Regular.ttf'
font_size = 20
font = ImageFont.truetype(font_path, font_size)
longest = ''
for word in words:
    if len(word[0]) > len(longest):
        longest = word[0]
width = round(font.getlength(longest) + (2 * font.size))
height = (len(words) + 1) * font.size
img = Image.new('RGB', (width, height), color='white')
d = ImageDraw.Draw(img)
color1 = (0, 0, 0)
color2 = (255, 0, 0)
y = font.size
for i, word in enumerate(words):
    text_width = font.getlength(word[0])
    x = (width - text_width) / 2
    for j, char in enumerate(word[0].upper()):
        if j in word[1]:
            d.text((x, y), char, color2, font=font)
        else:
            d.text((x, y), char, color1, font=font)
        x += font.getlength(char)
    y += font.size
img.save(output)
