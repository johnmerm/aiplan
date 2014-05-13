'''
Created on May 13, 2014

@author: grmsjac6
'''
from random import randint


d_inputVals = [randint(0,1000) for i in range(10)]
d_inputPos = list(range(10))

def predicate(val,bit):
    return val & (1<<(bit-1));





numOfBits = 32
bitsPerBank = 1
banks = 1<<bitsPerBank;

markers = [0 for i in range(numOfBits-1)]
print(numOfBits,bitsPerBank,banks)

def sort_pass(inputVals,inputPos,pas,markers,myId):
    banks_before = 1<<(pas-1) if pas>0 else 0
    banks_after = 1<<pas 
    
    valid_markers = [markers[i] for i in range((1<<pas)-1)]
    
    left_idx = valid_markers[myId-1] if len(valid_markers)>myId-1 else 0
    right_idx = valid_markers[myId] if len(valid_markers)>myId-1 else len(inputVals)
    
    
    outputVals = list(inputVals)
    outputPos = list(inputPos)
    for i in range(left_idx,right_idx):
        if predicate(inputVals[i], numOfBits-pas-1):
            pass
        else:
            pass
    
        
        
    
    