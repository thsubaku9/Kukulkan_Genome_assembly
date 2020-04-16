import random
Ntide = ['C','A','T','G']
ln = 200
st = ""
for i in range(0,ln):
    loc = random.randint(0,len(Ntide)-1)
    st+=Ntide[loc]


totalReads = 40
readLen = 50
genReads = list()

for i in range(0,totalReads):
    pos = random.randint(0,len(st)-1)
    if(pos + readLen < len(st)):
        genReads.append(st[pos:pos + readLen])
    else:
        tmp = ""
        tmp+= st[pos:] + st[:readLen -(len(st)-pos)]
        genReads.append(tmp)
