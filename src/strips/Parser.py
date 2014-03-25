'''
Created on Feb 11, 2014

@author: giannis
'''


import re
from Strips import Action

class Statement:
    def __init__(self,word,children,depth):
        self.word = word
        self.children = children
        self.depth = depth
        
    def __str__(self):
        return (''.join(self.depth*['\t']))+self.word+'\n'+(''.join([str(c) for c in self.children]))



class Domain:
    def parseDomain(self,statement):
        allWords = statement.word.split(' ')
        assert allWords[0].lower() =='domain' and len(allWords)==2
        self.domain = allWords[1]
    
    def parseTypes(self,statement):
        allWords = statement.word.split(' ')
        assert allWords[0].lower() ==':types' and len(allWords)>1
        self.types = set(allWords[1:])
        
    @staticmethod
    def assignments(statement,noname=False):
        allWords = statement.word.split(' ')
        name = None
        if not noname:
            name = allWords[0]
        ret = []
        istype = False
        vals = []
        scan = allWords if noname else allWords[1:]
        for w in scan:
            
            if w != '-':
                if not istype:
                    vals.append(w)
                else:
                    ret.extend([(v,w) for v in vals])
                    vals = []
                    istype = not istype
            else:
                istype = not istype
        if noname:
            return ret
        else:
            return name,ret
        
                
    
    def parseConstants(self,statement):
        name,asg = self.assignments(statement)
        assert name == ':constants'
        self.constants = asg
        
    def parsePredicates(self,statement):
        assert statement.word.lower().startswith(':predicates')
        for stmt in statement.children:
            name,asg = self.assignments(stmt)
            self.predicates[name]=asg
    
    def parseAction(self,statement):
        allWords = statement.word.split(' ')
        assert allWords[0] == ':action'
        assert len(allWords) == len(statement.children)+2
        
        name = allWords[1]
        parameters = self.assignments(statement.children[0],True)
        neg_preq = []
        pos_preq = []
        
        _precondition = statement.children[1]
        _and = _precondition.children
         
        for preq in _and: #  = :precondition statement.children[1].children[0] = and
            if preq.word == 'not':
                neg_preq.append(preq.children[0].word )
            else:
                pos_preq.append(preq.word)
        
        neg_effect = []
        pos_effect = []
        
        _effect = statement.children[2]
        _and = _effect.children
        for effect in _and: # statement.children[2] = :effect statement.children[1].children[0] = and
        
            if effect.word == 'not':
                neg_effect.append(effect.children[0].word)
            else:
                pos_effect.append(effect.word)
        
        self.actions[name]=Action(parameters,pos_preq,neg_preq,pos_effect,neg_effect)
        
    
    def delegateParse(self,statement):
        if (statement.word.lower().startswith('domain')):
            self.parseDomain(statement)
        elif (statement.word.lower().startswith(':types')):
            self.parseTypes(statement)
        elif (statement.word.lower().startswith(':constants')):
            self.parseConstants(statement)
        elif (statement.word.lower().startswith(':predicates')):
            self.parsePredicates(statement)
        elif (statement.word.lower().startswith(':action')):
            self.parseAction(statement)
    
    def __init__(self,statement):
        assert statement.word.lower().startswith('define')
        self.types=set()
        self.constants={}
        self.predicates = {}
        self.actions={}
        for st in statement.children:
            self.delegateParse(st)      
        
class Problem:
    def delegateParse(self,statement):
        if (statement.word.lower().startswith('problem')):
            self.parseProblem(statement)
        elif (statement.word.lower().startswith(':domain')):
            self.parseDomain(statement)
        elif (statement.word.lower().startswith(':objects')):
            self.parseObjects(statement)
        elif (statement.word.lower().startswith(':init')):
            self.parseInit(statement)
        elif (statement.word.lower().startswith(':goal')):
            self.parseGoal(statement)
    
    def parseProblem(self,statement):
        allWords = statement.word.split(' ')
        assert allWords[0].lower() =='problem' and len(allWords)==2
        self.problem = allWords[1]
    def parseDomain(self,statement):
        allWords = statement.word.split(' ')
        assert allWords[0].lower() ==':domain' and len(allWords)==2
        self.domain = allWords[1]
    
    def parseObjects(self,statement):
        name,asg = Domain.assignments(statement)
        assert name == ':objects'
        self.objects = asg
    
    def parseInit(self,statement):
        predicates = {s.word for s in statement.children}
        self.state=predicates
    
    def parseGoal(self,statement):
        p_eff = []
        n_eff = []
        
        _and = statement.children[0]
        for s in _and.children:
            if s.word == 'not':
                n_eff.append(s.children[0].word)
            else:
                p_eff.append(s.word)
        self.goal=(p_eff,n_eff)
    
    def __init__(self,statement):
        assert statement.word.lower().startswith('define')
        self.objects={}
        for st in statement.children:
            self.delegateParse(st)      

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
    statement =  encode(root,dct,0)
    return statement
    



