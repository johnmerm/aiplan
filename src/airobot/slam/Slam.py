'''
Created on Apr 23, 2014

@author: grmsjac6
'''


from OnlineSlam import matrix

def slam(init,moves,Landmarks,measurements,measurement_factor=2,movement_factor =1):
    i = 0
    if init != None:
        O = {(i,i):1}
        j = {i:init}
    
    
    measurement = measurements.next()
    for (c, v) in measurement.items():
        O[(i, i)] = O.get((i, i), 0) + measurement_factor
        O[(c, c)] = O.get((c, c), 0) + measurement_factor
          
        O[(i, c)] = O.get((i, c), 0) - measurement_factor
        O[(c, i)] = O.get((c, i), 0) - measurement_factor
          
        j[i] = j.get(i, 0) - measurement_factor * v
        j[c] = j.get(c, 0) + measurement_factor * v
    
    
    for m in moves:
        c = i + 1
        
        O[(i, i)] = O.get((i, i), 0) + movement_factor
        O[(c, c)] = O.get((c, c), 0) + movement_factor
          
        O[(i, c)] = O.get((i, c), 0) - movement_factor
        O[(c, i)] = O.get((c, i), 0) - movement_factor
          
        j[i] = j.get(i, 0) - movement_factor * m
        j[c] = j.get(c, 0) + movement_factor * m
        
        measurement = measurements.next()
        i = c
        for (c, v) in measurement.items():
            O[(i, i)] = O.get((i, i), 0) + measurement_factor
            O[(c, c)] = O.get((c, c), 0) + measurement_factor
          
            O[(i, c)] = O.get((i, c), 0) - measurement_factor
            O[(c, i)] = O.get((c, i), 0) - measurement_factor
          
            j[i] = j.get(i, 0) - measurement_factor * v
            j[c] = j.get(c, 0) + measurement_factor * v

    labels = range(i+1)+Landmarks
    return labels,O,j




def online_slam(init,moves,Landmarks,measurements,measurement_factor=2,movement_factor =1):
    labels0 = [0]+Landmarks
    labels = [0,1]+Landmarks
    i = 0
    if init != None:
        O = {(i,i):1}
        j = {i:init}
    
    
    measurement = measurements.next()
    for (c, v) in measurement.items():
        O[(i, i)] = O.get((i, i), 0) + measurement_factor
        O[(c, c)] = O.get((c, c), 0) + measurement_factor
          
        O[(i, c)] = O.get((i, c), 0) - measurement_factor
        O[(c, i)] = O.get((c, i), 0) - measurement_factor
          
        j[i] = j.get(i, 0) - measurement_factor * v
        j[c] = j.get(c, 0) + measurement_factor * v
    
    
    for m in moves:
        c = i + 1
        
        O[(i, i)] = O.get((i, i), 0) + movement_factor
        O[(c, c)] = O.get((c, c), 0) + movement_factor
          
        O[(i, c)] = O.get((i, c), 0) - movement_factor
        O[(c, i)] = O.get((c, i), 0) - movement_factor
          
        j[i] = j.get(i, 0) - movement_factor * m
        j[c] = j.get(c, 0) + movement_factor * m
        
        measurement = measurements.next()
        i = c
        for (c, v) in measurement.items():
            O[(i, i)] = O.get((i, i), 0) + measurement_factor
            O[(c, c)] = O.get((c, c), 0) + measurement_factor
          
            O[(i, c)] = O.get((i, c), 0) - measurement_factor
            O[(c, i)] = O.get((c, i), 0) - measurement_factor
          
            j[i] = j.get(i, 0) - measurement_factor * v
            j[c] = j.get(c, 0) + measurement_factor * v
        
        B = [O.get((0,0),0)]
        C = [j.get(0,0)]
        A = [O.get(labels[a],0) for a in range(1,len(labels))]
        Oprime = [[O.get((labels[a],labels[b]),0) for b in range(1,len(labels))] for a in range(1,len(labels))]
        jPrime = [j.get(a,0) for a in range(1,len(labels))]
        
        OPrimeMat  =matrix(Oprime)
        AMat = matrix([A])
        BMat = matrix([B])
        CMat = matrix([C])
        JPrimeMat = matrix([jPrime])
        Onew = OPrimeMat - AMat.transpose()*BMat.inverse()*AMat
        j_new = JPrimeMat - (AMat.transpose()*BMat.inverse()*CMat).transpose()
        
        O = {(labels0[a],labels0[b]):Onew.value[a][b] for b in range(len(labels0)) for a in range(len(labels0))}
        j = {labels0[a]:j_new.value[0][a] for a in range(len(labels0))}
        
        i=0
    return labels,O,j

def solve_slam(labels,O,j):
    OMatrix = matrix( [[O.get((labels[a],labels[b]),0) for b in range(len(labels))] for a in range(len(labels))] )
    jMAtrix =  matrix([ [j.get(a,0)] for a in range(len(labels))])
    
    m = OMatrix.inverse()*jMAtrix
    return m

Landmarks = ['l0', 'l1']
init = 5
moves = iter([7, 2])
measurements = iter([{'l0':2}, {'l1':4}, {'l1':4}])

labels,O,j = slam(init, moves, Landmarks, measurements)

# for k in labels:
#     print(' '.join([str(O.get((k,l),0)) for l in labels]+['.',str(j.get(k,0))]))


m = solve_slam(labels, O, j)
print(m)


moves = iter([7, 2])
measurements = iter([{'l0':2}, {'l1':4}, {'l1':4}])
labels,O,j = online_slam(init, moves, Landmarks, measurements)
m = solve_slam(labels, O, j)
print(m)

    
    
