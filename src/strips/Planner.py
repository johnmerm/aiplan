'''
Created on Feb 12, 2014

@author: giannis
'''
from Parser import *
from Strips import Action
from timeit import itertools


def ground(predicate,params,candidate):
    assert len(params) == len(candidate)
    
    
    ground = predicate
    for i in range(len(params)):
        r = params[i][0]
        l = candidate[i]
        ground = ground.replace(r,l)
    
    return ground
        
def expand(domain,problem,state):
    ret = []
    for (ac_name,action) in domain.actions.items():
        parameters = action.params
        applicable_list = []
        for (p,t) in parameters:
            objects = [po for po,to in problem.objects if to==t] + [po for po,to in domain.constants if to == t]
            applicable_list.append(objects)
        candidates = list(itertools.product(*applicable_list))
        
        for candidate in candidates:
            gpp = {ground(p,action.params,candidate) for p in action.pos_preq}
            gnp = {ground(p,action.params,candidate) for p in action.neg_preq}
            
            check_pos = gpp<=state
            check_neg = len(gnp & state)==0
            applicable = (check_pos and check_neg)
            if applicable:
                gpe = {ground(p,action.params,candidate) for p in action.pos_effects}
                gne = {ground(p,action.params,candidate) for p in action.neg_effects}
                
                n_state = state | gpe -gne
                ret.append((ac_name,candidate,n_state))
    return ret

def graphplan(domain,problem,steps = None):
    actions = set()
    state = problem.state
    p_goal = set(problem.goal[0])
    n_goal = set(problem.goal[1])
    
    check_pos = p_goal <=state
    check_neg = len(n_goal & state)==0
    
    print('p0:'+str(len(state)))
    i=1
    while (not (check_pos and check_neg)) and (steps == None or i<=steps):
        ret = expand(domain, problem, state)
        n_actions = {(r[0],r[1]) for r in ret}
        
        n_state = set.union(*[r[2] for r in ret])
        if n_state == state and actions ==n_actions:
            break
        else:
            state=n_state
            actions = n_actions
            
        print('A'+str(i)+':'+str(len(actions)))
        print('P'+str(i)+':'+str(len(state)))
        
        print(sorted(state))
        check_pos = p_goal <=state
        check_neg = len(n_goal & state)==0
        i +=1
        

f = open('problem.txt')           
s = ''.join(list(f))
stat = parse(s)
problem = Problem(stat)

f = open('domain.txt')           
s = ''.join(list(f))
stat = parse(s)
domain = Domain(stat)

graphplan(domain, problem)
                
        