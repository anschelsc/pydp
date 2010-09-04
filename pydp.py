#!/usr/bin/python3

import random

bywords=False
overlap=4
target=2000

file='./alice.txt'

def iterate(text):      #iterates "around the corner"
    for i in range(len(text)-overlap):
        yield i,tuple(text[i:i+overlap])
    for i in range(1,overlap):
        yield len(text)-overlap+i,tuple(text[-overlap+i:]+text[:i])

def buildchunkdic(chunks):      #chunks would normally be returned by iterate()
    chunkdic={}
    for chunk in chunks:
        if chunk[1] in chunkdic:
            chunkdic[chunk[1]].add(chunk[0])
        else:
            chunkdic[chunk[1]]={chunk[0]}
    return chunkdic

def nextbit(text, chunkdic, search):
    return text[(random.choice(tuple(chunkdic[search]))+overlap)%len(text)]

def dissociate(text, overlap, target):
    start=random.randrange(len(text)-overlap)
    dissociated=list(text[start:start+overlap])
    chunkdic=buildchunkdic(iterate(text))
    while len(dissociated)<target:
        dissociated.append(nextbit(text,chunkdic,tuple(dissociated[-overlap:])))
    return dissociated

with open(file) as opened:
    text=opened.read()

if bywords:
    print(' '.join(dissociate(text.split(),overlap,target)))
else:
    print(''.join(dissociate(text,overlap,target)))
