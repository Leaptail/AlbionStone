import os

def generatenegdesc():
    with open('neg.txt','w') as f:
        for filename in os.listdir('MemoryItems/RoughStone/negative'):
            f.write('MemoryItems/RoughStone/negative/' + filename + '\n')