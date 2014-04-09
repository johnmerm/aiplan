# --------------
# USER INSTRUCTIONS
#
# Write a function called stochastic_value that 
# takes no input and RETURNS two grids. The
# first grid, value, should contain the computed
# value of each cell as shown in the video. The
# second grid, policy, should contain the optimum
# policy for each cell.
#
# Stay tuned for a homework help video! This should
# be available by Thursday and will be visible
# in the course content tab.
#
# Good luck! Keep learning!
#
# --------------
# GRADING NOTES
#
# We will be calling your stochastic_value function
# with several different grids and different values
# of success_prob, collision_cost, and cost_step.
# In order to be marked correct, your function must
# RETURN (it does not have to print) two grids,
# value and policy.
#
# When grading your value grid, we will compare the
# value of each cell with the true value according
# to this model. If your answer for each cell
# is sufficiently close to the correct answer
# (within 0.001), you will be marked as correct.
#
# NOTE: Please do not modify the values of grid,
# success_prob, collision_cost, or cost_step inside
# your function. Doing so could result in your
# submission being inappropriately marked as incorrect.

# -------------
# GLOBAL VARIABLES
#
# You may modify these variables for testing
# purposes, but you should only modify them here.
# Do NOT modify them inside your stochastic_value
# function.

grid = [[0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 1, 1, 0]]
       
goal = [0, len(grid[0])-1] # Goal is in top right corner


delta = [[-1, 0 ], # go up
         [ 0, -1], # go left
         [ 1, 0 ], # go down
         [ 0, 1 ]] # go right

delta_name = ['^', '<', 'v', '>'] # Use these when creating your policy grid.

success_prob = 0.5                      
failure_prob = (1.0 - success_prob)/2.0 # Probability(stepping left) = prob(stepping right) = failure_prob
collision_cost = 100                    
cost_step = 1        
                     

############## INSERT/MODIFY YOUR CODE BELOW ##################
#
# You may modify the code below if you want, but remember that
# your function must...
#
# 1) ...be called stochastic_value().
# 2) ...NOT take any arguments.
# 3) ...return two grids: FIRST value and THEN policy.

def stochastic_value():
    def is_free(x):
        return 0<=x[0]<len(grid) and 0<=x[1]<len(grid[x[0]]) and grid[x[0]][x[1]] == 0

    open_set = [(goal[0],goal[1])]
    value_set = {(goal[0],goal[1]):0}
    policy_set = {(goal[0],goal[1]):'*'}
    while len(open_set) >0:
        for c in open_set:
            
            children = [(c[0]-d[0],c[1]-d[1],di) for (di,d) in enumerate(delta)]
            children = filter(is_free,children)
            for chi in children:
                ch = (chi[0],chi[1])
                di = chi[2]
                dis = [di+a for a in range(-1,2)]
                targets = [(ch[0]-delta[disi][0],ch[1]-delta[disi][1]) for disi in dis]
                
                
                ch_v = cost_step+ value_set.get(c,1000.)     
                
                if not ch in value_set or ch_v<value_set[ch]:
                    value_set[ch] = ch_v
                    policy_set[ch] = delta_name[di]
                    if not ch in open_set:
                        open_set.append(ch)
            open_set.remove(c)  
    
    
    
    value = [[value_set.get((x,y),1000) for y in range(len(grid[x]))] for x in range(len(grid))] 
    policy =[[policy_set.get((x,y),' ') for y in range(len(grid[x]))] for x in range(len(grid))] 
    return value,policy

v,p = stochastic_value()
for vi in v:print vi
for pi in p:print pi
