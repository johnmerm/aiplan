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
        if node in came_from: 
            node = came_from[node]
        else:
            return list(reversed(p))

def validatePath(path,start,end):
    valid = (path[0] == start and path[-1]==end)
    if valid: 
        for i in range(1,len(path)):
            n = path[i]
            p = path[i-1]
            valid = valid and (n in neighbors(p))
    return valid

def astar(start,end,heuristic=lambda s:manhattan(s),dist=lambda c,n:1):
    depth = {start:0}
    closedset = set()
    openset = {start}
    came_from = {}
    
    g_score = {start:0}
    f_score = {start:heuristic(start)}
    
    while len(openset) > 0:
        current = min(openset,key = lambda o: f_score[o])
        if current == end:
            return came_from,depth
        
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
                    depth[n] = depth[current]+1
    return None



def breadth_first(start,d):
    depth = {start:0}
    openset = {start}
    sd = set()
    while len(openset)>0 :
        for s in list(openset):
            openset.remove(s)
            v = depth[s]
            if v == d:
                sd.add(s)
                continue
            ns = neighbors(s)
            for n in ns:
                if not n in depth:
                    openset.add(n)
                    depth[n] = v+1
    return sd,depth

def test(start):
    end = "012345678"
    came_from,depth = astar(start,end)
    
    path = reconstruct_path(came_from, end, start)
    print(depth[end],len(path),validatePath(path,start,end))

def testDepth(start):
    end = "012345678"
    sd,depth = breadth_first(start, end)
    
    print(len(sd))
    
test("164870325")
test("817456203")
#testDepth("012345678",27)


        
    