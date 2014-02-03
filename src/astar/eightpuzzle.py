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
    visited = {start}
    valid = (path[0] == start and path[-1]==end)
    for i in range(1,len(path)):
        if not valid : return False 
        n = path[i]
        p = path[i-1]
        valid = valid and (not n in visited) and (n in neighbors(p))
        visited.add(n)
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
        #currents = [c for c in openset if f_score[c] == f_score[current]]
        currents=[current]
        for current in currents:
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



def breadth_first(start,d,candidates=None):
    depth = 0;
    visited=set()
    openset = {start}
    while depth<=d:
        expand = {n for p in openset for n in neighbors(p)  if not n in visited}
        visited.update(openset)
        openset = expand
        
        found=set()
        if candidates!=None:
            found = openset.intersection(candidates)
            
        depth += 1
        print(depth,len(openset)," ".join(found))
    return openset

def test(start):
    end = "012345678"
    came_from,depth = astar(start,end)
    
    path = reconstruct_path(came_from, end, start)
    print(len(path))
    print(path)
    
    
def testManhattan():
    seq22 = ['164870325', '164807325', '164827305', '164827350', '164820357', '164802357', '104862357', '140862357', '142860357', '142867350', '142867305', '142807365', '142087365', '142387065', '142387605', '142307685', '142370685', '142375680', '142375608', '142305678', '102345678', '012345678']
    seq24 = ['164870325', '164875320', '164875302', '164805372', '164085372', '164385072', '164385702', '164305782', '104365782', '014365782', '314065782', '314605782', '314650782', '314652780', '314652708', '314652078', '314052678', '014352678', '104352678', '140352678', '142350678', '142305678', '102345678', '012345678']
    m22 = [manhattan(s) for s in seq22]
    m24 = [manhattan(s) for s in seq24]
    
    print (m22)
    print (m24)
    
test("164870325")
#test("817456203")
#sd = breadth_first("012345678",27,{"164870325","817456203"})
#print(len(sd))


#testManhattan()


        
    