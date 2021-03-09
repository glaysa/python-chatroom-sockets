import random
import re

chars1 = ['a', 'k']
chars2 = ['k', 'h', 'l']

for a in chars1:
    if a not in chars2:
        chars1.remove(a)

print(chars1)