'''
Created on Feb 4, 2014

@author: giannis
'''
import unittest
from Strips import *

class Test(unittest.TestCase):
    def setUp(self):
        params=['?x1','?x2','?x3']
        literals = ['A','B','C']
        pos_preq = {'S ?x1 ?x2','R ?x3 ?x1'}
        neg_preq = set()
        
        pos_effects = {'S ?x2 ?x1','S ?x1 ?x3'}
        neg_effects = {'R ?x3 ?x1'}
        
        self.state={'S B B', 'S C B', 'S A C', 'R B B', 'R C B'}
        self.op1 = Operator(params, pos_preq, neg_preq, pos_effects, neg_effects, literals)
        
        pos_preq = {'S ?x3 ?x1','R ?x2 ?x2'}
        pos_effects = {'S ?x1 ?x3'} 
        neg_effects = {'S ?x3 ?x1'}
        
        self.op2 = Operator(params, pos_preq, neg_preq, pos_effects, neg_effects, literals)
        self.goal = {'S A A'}


    def testSubstitute(self):
        gp = substitute('S ?x1 ?x2',['?x1','?x2','?x3'],['A','B','C'])
        assert gp == 'S A B'

    def testApplicables(self):
        
        tgt1 = self.op1.applicable(self.state)
        tgt2 = self.op2.applicable(self.state)
        
        vals1 = {frozenset(v) for v in tgt1.values()}
        vals2 = {frozenset(v) for v in tgt2.values()}
        
        vals = vals1 | vals2
        
        print(len(vals))
        print(vals)
        
    def testCandidates(self):
        asub1 = self.op1.candidates(self.goal, set())
        asub2 = self.op2.candidates(self.goal, set())
        
        asub = asub1 | asub2
        print (len(asub))
        print(asub)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()