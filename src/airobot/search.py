# ----------
# User Instructions:
# 
# Define a function, search() that takes no input
# and returns a list
# in the form of [optimal path length, x, y]. For
# the grid shown below, your function should output
# [11, 4, 5].
#
# If there is no valid path from the start point
# to the goal, your function should return the string
# 'fail'
# ----------

# Grid format:
#   0 = Navigable space
#   1 = Occupied space

grid = [[0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 1, 1, 1, 0],
        [0, 0, 0, 0, 1, 0]]

init = [0, 0]
goal = [len(grid)-1, len(grid[0])-1] # Make sure that the goal definition stays in the function.

delta = [[-1, 0 ], # go up
        [ 0, -1], # go left
        [ 1, 0 ], # go down
        [ 0, 1 ]] # go right

delta_name = ['^', '<', 'v', '>']

cost = 1
cost_step = 1


def search(grid,init,goal):
    # ----------------------------------------
    # insert code here and make sure it returns the appropriate result
    # ----------------------------------------
    
    
    openset = {tuple(init)}
    closedset = set()
    g_score = {tuple(init):0}
    path = "fail"
    while len(openset)>0:
        tocheck =  min(openset,key = lambda o: g_score[o])
        val = g_score[tocheck]
        
        if tocheck == tuple(goal):
            path = [val,goal[0],goal[1]]
            break
        
        children = set(filter(lambda x:x[0]>=0 and x[1]>=0 and 
                                       x[0]<len(grid) and x[1]<len(grid[0]) and 
                                       grid[x[0]][x[1]] == 0
                              ,{ (tocheck[0]+d[0],tocheck[1]+d[1]) for d in delta }))
        children = set(filter(lambda x:x not in closedset,children))
        for c in children:
            openset.add(c)
            g_score[c] = val+cost
        closedset.add(tocheck)
        openset.remove(tocheck)
        
    return path # you should RETURN your result


def search_expand():
    closed = [[0 for row in range(len(grid[0]))] for col in range(len(grid))]
    expand = [[-1 for row in range(len(grid[0]))] for col in range(len(grid))]
    closed[init[0]][init[1]] = 1

    x = init[0]
    y = init[1]
    g = 0

    open = [[g, x, y]]

    found = False  # flag that is set when search is complete
    resign = False # flag set if we can't find expand
    e_i = 0
    while not found and not resign:
        if len(open) == 0:
            resign = True
        else:
            open.sort()
            open.reverse()
            next = open.pop()
            x = next[1]
            y = next[2]
            g = next[0]
            
            expand[x][y] = e_i
            e_i += 1
            
            if x == goal[0] and y == goal[1]:
                found = True
            else:
                for i in range(len(delta)):
                    x2 = x + delta[i][0]
                    y2 = y + delta[i][1]
                    if x2 >= 0 and x2 < len(grid) and y2 >=0 and y2 < len(grid[0]):
                        if closed[x2][y2] == 0 and grid[x2][y2] == 0:
                            g2 = g + cost
                            open.append([g2, x2, y2])
                            closed[x2][y2] = 1
                            
    return expand #Leave this line for grading purposes!



def search_dir():
    closed = [[-1 for row in range(len(grid[0]))] for col in range(len(grid))]
    closed[init[0]][init[1]] = 0

    x = init[0]
    y = init[1]
    g = 0

    open = [[g, x, y]]
    came_from = {}
    found = False  # flag that is set when search is complet
    resign = False # flag set if we can't find expand

    while not found and not resign:
        if len(open) == 0:
            resign = True
            return 'fail'
        else:
            open.sort()
            open.reverse()
            next = open.pop()
            x = next[1]
            y = next[2]
            g = next[0]
            
            if x == goal[0] and y == goal[1]:
                found = True
            else:
                for i in range(len(delta)):
                    x2 = x + delta[i][0]
                    y2 = y + delta[i][1]
                    if x2 >= 0 and x2 < len(grid) and y2 >=0 and y2 < len(grid[0]):
                        if closed[x2][y2] == -1 and grid[x2][y2] == 0:
                            g2 = g + cost
                            open.append([g2, x2, y2])
                            closed[x2][y2] = g2
                            came_from[(x2,y2)] = (x,y)
    expand = [[' ' for row in range(len(grid[0]))] for col in range(len(grid))]
    s_node = goal
    expand[goal[0]][goal[1]] = '*'
    while s_node !=init and tuple(s_node) in came_from:
        c_node =came_from[tuple(s_node)]
        if c_node[0]-s_node[0] == 1:expand[c_node[0]][c_node[1]] ='^'
        elif c_node[0]-s_node[0] == -1:expand[c_node[0]][c_node[1]] ='v'
        elif c_node[1]-s_node[1] == 1:expand[c_node[0]][c_node[1]] ='<'
        elif c_node[1]-s_node[1] == -1:expand[c_node[0]][c_node[1]] ='>'
        s_node = [c_node[0],c_node[1]]
    
    for i in range(len(expand)):
        print(expand[i])
    return expand# make sure you return the shortest path.
# make sure you return the shortest path.



heuristic = [[9, 8, 7, 6, 5, 4],
            [8, 7, 6, 5, 4, 3],
            [7, 6, 5, 4, 3, 2],
            [6, 5, 4, 3, 2, 1],
            [5, 4, 3, 2, 1, 0]]


# ----------------------------------------
# modify code below
# ----------------------------------------

def search_astar():
    closed = [[0 for row in range(len(grid[0]))] for col in range(len(grid))]
    closed[init[0]][init[1]] = 1

    expand = [[-1 for row in range(len(grid[0]))] for col in range(len(grid))]
    action = [[-1 for row in range(len(grid[0]))] for col in range(len(grid))]


    x = init[0]
    y = init[1]
    g = 0

    open = [[g, x, y]]

    found = False  # flag that is set when search is complete
    resign = False # flag set if we can't find expand
    count = 0
    
    while not found and not resign:
        if len(open) == 0:
            resign = True
            return "Fail"
        else:
            open.sort()
            open.reverse()
            next = open.pop()
            x = next[1]
            y = next[2]
            g = next[0]
            expand[x][y] = count
            count += 1
            
            if x == goal[0] and y == goal[1]:
                found = True
            else:
                for i in range(len(delta)):
                    x2 = x + delta[i][0]
                    y2 = y + delta[i][1]
                    if x2 >= 0 and x2 < len(grid) and y2 >=0 and y2 < len(grid[0]):
                        if closed[x2][y2] == 0 and grid[x2][y2] == 0:
                            g2 = g + cost
                            h2 = heuristic[x2][y2]
                            open.append([g2+h2, x2, y2])
                            closed[x2][y2] = 1
    for i in range(len(expand)):
        print(expand[i])
    return expand #Leave this line for grading purposes!


grid = [[1, 1, 1, 0, 0, 0],
        [1, 1, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 1, 1],
        [1, 1, 1, 0, 1, 1]]
goal = [2, 0] # final position
init = [4, 3, 0] # first 2 elements are coordinates, third is direction
cost = [2, 1, 20] # the cost field has 3 values: right turn, no turn, left turn

forward = [[-1,  0], # go up
           [ 0, -1], # go left
           [ 1,  0], # go down
           [ 0,  1]] # do right
forward_name = ['up', 'left', 'down', 'right']

# the cost field has 3 values: right turn, no turn, left turn
action = [-1, 0, 1]
action_name = ['R', '#', 'L']

def compute_value():
    t_goal = (goal[0],goal[1])
    
    value_dict = {t_goal:0}
    policy_dict = {t_goal:'*'}
    open_set = [(goal[0],goal[1],f) for f in range(len(forward))] 
    while len(open_set)>0:
        for c in open_set:
            v = value_dict[(c[0],c[1])]
            
            for ai in range(len(action)):
                a = action[ai]
                a_name = action_name[ai]
                
                ch_o = (c[2]-a) % len(forward)
                f = forward[ch_o]
                ch_x = c[0]+f[0]
                ch_y = c[1]+f[1]
                 
                
                if 0<=ch_x<len(grid) and 0<=ch_y<len(grid[0]) and grid[ch_x][ch_y] == 0:
                    
                    ch = (ch_x,ch_y)
                    vv = v+cost[ai]
                    if not ch in value_dict or vv<value_dict[ch]:
                        value_dict[ch] = vv
                        policy_dict[ch] = a_name
                        open_set.append((ch_x,ch_y,ch_o)) 
                    
             
            open_set.remove(c) 
                        
    policy = [[policy_dict[(x,y)] if (x,y) in policy_dict else ' ' for y in range(len(grid[x])) ] for x in range(len(grid))]
    return policy #make sure your function returns a grid of values as demonstrated in the previous video.


v =  compute_value()
for i in range(len(v)):
    print(v[i])

