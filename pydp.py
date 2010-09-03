#!/usr/bin/python3

import random

bywords=True
overlap=3
target=200

file='./alice.txt'

def nextbit(text, using):
    l=len(text)
    possible=set()
    for n in range(len(text)):
        if text[n]==using[0]:
            possible.add(n)
    for offset in range(1,len(using)):
        for index in possible.copy():
            if text[(index+offset)%l]!=using[offset]:
                possible.remove(index)
    return text[(random.choice(tuple(possible))+len(using))%l]

def dissociate(text, overlap, target):
    start=random.randrange(len(text)-overlap)
    dissociated=list(text[start:start+overlap])
    while len(dissociated)<target:
        dissociated.append(nextbit(text,dissociated[-overlap:]))
    return dissociated

with open(file) as opened:
    text=opened.read()

if bywords:
    print(' '.join(dissociate(text.split(),overlap,target)))
else:
    print(''.join(dissociate(text,overlap,target)))
