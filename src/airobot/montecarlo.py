colors = [['red', 'green', 'green', 'red' , 'red'],
          ['red', 'red', 'green', 'red', 'red'],
          ['red', 'red', 'green', 'green', 'red'],
          ['red', 'red', 'red', 'red', 'red']]

measurements = ['green', 'green', 'green' ,'green', 'green']


motions = [[0,0],[0,1],[1,0],[1,0],[0,1]]

sensor_right = 0.7

p_move = 0.8



#DO NOT USE IMPORT
#ENTER CODE BELOW HERE
#ANY CODE ABOVE WILL CAUSE
#HOMEWORK TO BE GRADED
#INCORRECT


def show(p):
    for i in range(len(colors)):
        print(p[i])


def normalize(p):
    ps = sum([sum(p[i]) for i in range(len(p))])
    q = [[p[i][j]/ps for j in range(len(p[i])) ] for i in range(len(p))]
    return q

def sense(p,m):
    q = [[(sensor_right if colors[i][j] == m else (1-sensor_right))*p[i][j] for j in range(len(p[i])) ] for i in range(len(p))]
    return normalize(q);
    
    
    
def move(p,m):
    q = [[ p_move*(p[(i-m[0]) % len(p)] [(j-m[1]) % len(p[i])]) + (1-p_move)*p[i][j]  for j in range(len(p[i])) ] for i in range(len(p))]   
    return normalize(q)



p = [[1.0/(len(colors)*len(colors[0])) for j in range(len(colors[0]))] for i in range(len(colors))]

for i in range(len(measurements)):
    p = move(p,motions[i])
    p = sense(p,measurements[i])
    
    #Your probability array must be printed 
#with the following code.

show(p)