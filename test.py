import random
import re

chars = ['a', 'b', 'c', 'd', 'e']
valgt_chars = []


def generer_bokstav():
    valgt = chars.pop(random.choice(range(0, len(chars))))
    valgt_chars.append(valgt)
    return valgt


def replace_word(text):
    # return str(text).replace('replace', generer_bokstav(), 1)
    return re.sub('replace', generer_bokstav(), text, 1)


text = random.choice([
    "replace, replace, og replace valgt.",
    "replace er valgt."
])

arr = str(text).split()
# counter = arr.count('replace')
counter = 0
for _ in re.finditer('replace', text):
    counter += 1

print(f"Counter: {counter}")

while counter > 0:
    print(f"Iteration: {counter}")
    text = replace_word(text)
    print(text)
    counter -= 1

#for i in range(counter):
    #print(i)
    #text = replace_word(text)
    #print(text)

# print(text)
print(valgt_chars)

# m = re.search('hello', 'hello! world')
# print(m.group(0))

a = 'jog@'
a2 = a.rsplit('@', 1)[0]
l = a2[len(a2) - 1:]
a3 = str(a2 + l)

print(l)
print(a3)
