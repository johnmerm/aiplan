'''
Created on Feb 2, 2014

@author: giannis
'''


def neighbors(string,cols=3,rows=3):
    n = []
    pos = string.index('0')
    
    col = pos//rows;
    row = pos % rows;
    
    if col>0:
        newpos = (col-1)*rows+row
        ns = list(string)
        ns[pos] = ns[newpos]
        ns[newpos]='0'
        
        n.append(''.join(ns))
    
    if col<cols-1:
        newpos = (col+1)*rows+row
        ns = list(string)
        ns[pos] = ns[newpos]
        ns[newpos]='0'
        
        n.append(''.join(ns))
    
    if row>0:
        newpos = (col)*rows+(row-1)
        ns = list(string)
        ns[pos] = ns[newpos]
        ns[newpos]='0'
        
        n.append(''.join(ns))
    
    if row<rows-1:
        newpos = (col)*rows+(row+1)
        ns = list(string)
        ns[pos] = ns[newpos]
        ns[newpos]='0'
        
        n.append(''.join(ns))
        
    return n

def manhattan(string,cols=3,rows=3):
    d = 0
    for i in range(len(string)):
        c = int(string[i])
        ic = i//rows;
        ir = i % rows;
        
        cc = c//rows;
        cr = c % rows;
        
        d += (abs(cc-ic)+abs(cr-ir))
    return d

def reconstruct_path(came_from,node,start):
    p = []
    while True:
        p.append(node)
        if node == start:
            return reversed(p)
        elif node in came_from: 
            node = came_from[node]
        else:
            return reversed(p)

def astar(start,end,heuristic=lambda s:manhattan(s),dist=lambda c,n:1):
    closedset = set()
    openset = {start}
    came_from = {}
    
    g_score = {start:0}
    f_score = {start:heuristic(start)}
    
    while len(openset) > 0:
        current = min(openset,key = lambda o: f_score[o])
        if current == end:
            return reconstruct_path(came_from, current,start)
        
        openset.remove(current)
        closedset.add(current)
        for n in neighbors(current):
            if n in closedset:
                continue
            tentative_g = g_score[current]+dist(current,n)
            if (not n in openset or tentative_g<g_score[n]):
                came_from[n] = current
                g_score[n] = tentative_g
                f_score[n] = g_score[n] +heuristic(n)
                if not n in openset:
                    openset.add(n)
    return []


def test(start):
    end = "012345678"
    path = astar(start,end)
    print(len(path))

test("164870325")
        
    