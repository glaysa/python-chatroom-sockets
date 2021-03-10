import random
import re

chars1 = ['a', 'b']
chars2 = ['a', 'b', 'c', 'd', 'e']


def test():
    global chars1, chars2

    for i in range(2):

        print(f"Suggested Action: {chars1}")

        print(f"List of suggestions: {chars2}")

        suggest_action = random.choice(chars2)
        print(f"Action suggested: {suggest_action}")

        c = [x for x in chars2 if x != suggest_action]
        print(f"New list of suggestion: {c}")

        ch2 = random.choice(c)
        print(f"New action to suggest: {ch2}\n")

test()
