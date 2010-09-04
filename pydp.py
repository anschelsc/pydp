#!/usr/bin/python3

import random
import optparse
import sys

parser=optparse.OptionParser(usage='usage: %prog [options] [sourcefile]',version='%prog 1.0')
parser.add_option('-w','--words',action='store_true',dest='bywords',default=False,help='Overlap by words')
parser.add_option('-c','--characters',action='store_false',dest='bywords',help='Overlap by characters [default]')
parser.add_option('-o','--overlap',type='int',metavar='N',dest='overlap',default=4,help='Use N characters/words of overlap [default: 4]')
parser.add_option('-l','--length',type='int',metavar='N',dest='target',default=2000,help='Output N characters/words [default: 2000]')
options,args=parser.parse_args()
if len(args)>1:
    parser.error('%prog takes one or zero filenames. To use more files, pipe from cat.')

bywords=options.bywords
overlap=options.overlap
target=options.target

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

if len(args):
    with open(args[0]) as opened:
        text=opened.read()
else:
    text=sys.stdin.read()

if bywords:
    print(' '.join(dissociate(text.split(),overlap,target)))
else:
    print(''.join(dissociate(text,overlap,target)))
