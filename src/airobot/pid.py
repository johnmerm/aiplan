# -----------
# User Instructions
#
# Define a function smooth that takes a path as its input
# (with optional parameters for weight_data, weight_smooth)
# and returns a smooth path.
#
# Smoothing should be implemented by iteratively updating
# each entry in newpath until some desired level of accuracy
# is reached. The update should be done according to the
# gradient descent equations given in the previous video:
#
# If your function isn't submitting it is possible that the
# runtime is too long. Try sacrificing accuracy for speed.
# -----------


from math import *

# Don't modify path inside your function.
path = [[0, 0],
        [0, 1],
        [0, 2],
        [1, 2],
        [2, 2],
        [3, 2],
        [4, 2],
        [4, 3],
        [4, 4]]

# ------------------------------------------------
# smooth coordinates
#

def smooth(path, weight_data = 0.5, weight_smooth = 0.1):

    # Make a deep copy of path into newpath
    newpath = [[0 for col in range(len(path[0]))] for row in range(len(path))]
    for i in range(len(path)):
        for j in range(len(path[0])):
            newpath[i][j] = path[i][j]


    #### ENTER CODE BELOW THIS LINE ###
    change = 1
    while change>0.00000001:
        #newpath2 = [ [path[i][j] if i==0 or i ==len(path)-1 else 
        #           newpath[i][j] +weight_data*(path[i][j]-newpath[i][j]) for j in range(len(path[i]))] for i in range(len(path))]
        
        #newpath2 = [ [path[i][j] if i==0 or i ==len(path)-1 else 
        #           newpath2[i][j] +weight_smooth*(newpath2[i+1][j]+newpath2[i-1][j]-2*newpath2[i][j]) for j in range(len(path[i]))] for i in range(len(path))]
        #change = sum([ sum([abs(newpath2[i][j]-newpath[i][j]) for j in range(len(path[i]))]) for i in range(len(path)) ])
        #newpath = newpath2
        change = 0
        for i in range(1,len(path)-1):
            for j in range(len(path[i])):
                aux = newpath[i][j]
                newpath[i][j] = newpath[i][j] +weight_data*(path[i][j]-newpath[i][j])
                newpath[i][j] = newpath[i][j] + weight_smooth*(newpath[i+1][j]+newpath[i-1][j]-2*newpath[i][j])
                change += abs(newpath[i][j]-aux)
    return newpath # Leave this line for the grader!

# feel free to leave this and the following lines if you want to print.
newpath = smooth(path)

# thank you - EnTerr - for posting this on our discussion forum
for i in range(len(path)):
    print '['+ ', '.join('%.3f'%x for x in path[i]) +'] -> ['+ ', '.join('%.3f'%x for x in newpath[i]) +']'





