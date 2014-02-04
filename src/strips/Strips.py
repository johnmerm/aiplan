'''
Created on Feb 4, 2014

@author: giannis
'''
import itertools


def substitute(prop,params,substitution):
    g_prop = prop
    for i in range(len(params)):
        p = params[i]
        l = substitution[i]
        g_prop = g_prop.replace(p,l)
    return g_prop

class Operator:
    def __init__(self,params,
                        pos_preq,neg_preq,
                        pos_effects,neg_effects,
                        literals):
        self.params = params
        self.literals = literals
        
        self.pos_preq = pos_preq
        self.neg_preq = neg_preq
        self.pos_effects = pos_effects
        self.neg_effects = neg_effects

    def applicable(self,state):
        substitutions = list(itertools.product(self.literals,repeat=len(self.params)))
        a_sub = {}
        for substitution in substitutions:
            gpp = {substitute(p,self.params,substitution) for p in self.pos_preq}
            gnp = {substitute(p,self.params,substitution) for p in self.neg_preq}
            
            check_pos = gpp<=state
            check_neg = len(gnp & self.neg_preq)==0
            applicable = (check_pos and check_neg)
            if applicable: 
                
                gpe = {substitute(p,self.params,substitution) for p in self.pos_effects}
                gne = {substitute(p,self.params,substitution) for p in self.neg_effects}
                target = state | gpe
                target = target -gne
                a_sub["".join(substitution)] = target
                
        
        
        return a_sub
    
    def candidates(self,pos_goal,neg_goal):
        substitutions = list(itertools.product(self.literals,repeat=len(self.params)))
        a_sub = set()
        for substitution in substitutions:
            gpe = {substitute(p,self.params,substitution) for p in self.pos_effects}
            gne = {substitute(p,self.params,substitution) for p in self.neg_effects}
             
            check_pos = gpe>=pos_goal
            check_neg = gne>=neg_goal
            applicable = (check_pos and check_neg)   
            if applicable: a_sub.add(substitution) 
        return a_sub
    