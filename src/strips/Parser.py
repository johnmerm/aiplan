'''
Created on Feb 11, 2014

@author: giannis
'''


import re

class Statement:
    def __init__(self,word,children,depth):
        self.word = word
        self.children = children
        self.depth = depth
        
    def __str__(self):
        return (''.join(self.depth*['\t']))+self.word+'\n'+(''.join([str(c) for c in self.children]))

p = re.compile("\)|\(")
comments = re.compile(';.*\n')
baseStatement = re.compile('\(([^\)|\(]+)\)')
words = re.compile('\S+')     
asig = re.compile('(:\S+)([^:]*)')


def encodeDict(root,dct,depth):
    noc = dct[root]
    retdct = {}
    assigs = re.findall(asig,noc)
    if len(assigs) ==0:
        allWords = re.findall(words, noc)
        if len(allWords) == 1:
            return {allWords[0]:None}
        else:
            key = allWords[0]
            values = []
            for a in allWords[1:]:
                if a.startswith('_stmt'):
                    ref = int(a[5:-1])
                    values.append(encodeDict(ref, dct, depth+1))
                else:
                    values.append(a)
            
            return {key:values}
    else:
        for assig_key,assig_val in assigs:
            assig_val = assig_val.strip()
            if len(assig_val) == 0:
                return {assig_key:None}
            else:
                key = assig_key
                values = []
                allWords = re.findall(words, assig_val)
                for a in allWords:
                    if a.startswith('_stmt'):
                        ref = int(a[5:-1])
                        values.append(encodeDict(ref, dct, depth+1))
                    else:
                        values.append(a)
                retdct[key]=values
        
    return retdct
    

def encode(root,dct,depth=0):
    noc = dct[root]
    allWords = re.findall(words, noc)
    
    wds = []
    st_ref = []
    
    
    for a in allWords:
        if a.startswith(':'):
            key = a
        if a.startswith('_stmt'):
            ref = int(a[5:-1])
            st_ref.append(ref)
        else:
            wds.append(a)
    
    word = " ".join(wds)
    children = [encode(r,dct,depth+1) for r in st_ref]
    return Statement(word,children,depth)

def parse(string):
    noc = re.sub(comments, '', string)
    allBase = re.findall(baseStatement, noc)
    cnt = 0
    dct = {}
    while len(allBase)>0:
        for a in allBase:
            cnt +=1
            dct[cnt]=a
            noc = noc.replace('('+a+')',' _stmt'+str(cnt)+'_ ')
        allBase = re.findall(baseStatement, noc)
    
    
    allWords = re.findall(words, noc)
    root = int(allWords[0][5:-1])
    return root,encodeDict(root,dct,0)
    


f = open('domain.txt')           
s = ''.join(list(f))
r,stat = parse(s)
print(r,stat)  
