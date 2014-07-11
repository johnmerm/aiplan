import unittest

from screw import bra,ibra,breakTrans,composeTrans,composeScrew,breakScrew,exp,adj,log
from sympy import symbols,cos,sin
from numpy import  array,array_equal,allclose

import numpy
import math

class Test(unittest.TestCase):
    
     
    
    def testBraIBra(self):
        (a,b,c,d,e,f,g,h,i,j,k,l) = symbols('a b c d e f g h i j k l')
        
        w = array([[a],[b],[c]])
        W = array([[0,-c,b],
                   [c,0,-a],
                   [-b,a,0]])
        
        Wm = bra(w)
        wm = ibra(W)
        assert array_equal(Wm,W) and array_equal(wm,w)
        
        w = array([[a],[b],[c],[d],[e],[f]])
        W = array([[0,-c,b,d],
                   [c,0,-a,e],
                   [-b,a,0,f],
                   [0 ,0,0,0]])
        
        Wm = bra(w)
        wm = ibra(W)
        assert array_equal(Wm,W) and array_equal(wm,w)
        
        
        
    
    def testBreakComposeTrans(self):
        (a,b,c,d,e,f,g,h,i,j,k,l) = symbols('a b c d e f g h i j k l')
        Tm = array([[a,b,c,d],
                    [e,f,g,h],
                    [i,j,k,l],
                    [0,0,0,1]])
        
        Rm = array([[a,b,c],
                    [e,f,g],
                    [i,j,k]])
        pm = array([[d],
                    [h],
                    [l]])
        
        (R,p) = breakTrans(Tm)
        assert array_equal(R,Rm) and array_equal(p,pm)
        T = composeTrans(R, p)
        assert array_equal(T,Tm)
    
    def testBreakComposeScrew(self):
        (a,b,c,d,e,f,g,h,i,j,k,l) = symbols('a b c d e f g h i j k l')
        Sm = array([[a,b,c,d,e,f]]).T
        wm = array([[a,b,c]]).T
        um = array([[d,e,f]]).T
        
        S = composeScrew(wm,um)
        assert array_equal(S,Sm)
        
        (w,u) = breakScrew(Sm)
        assert array_equal(w,wm) and array_equal(u,um)
    
    def testAdj(self):
        #Rotation by z pi/5 and
        
        t = math.pi/5
        ct = math.cos(t)
        st = math.sin(t)
        
        R = array([[1,0,0],
                   [0,ct,-st],
                   [0,st,ct]
                   ])
        #translation
        p = array([[2,1,1]]).T
        
        A = array([
                   [ 1,   0,         0,         0,   0,   0],
                   [ 0,   0.80902,  -0.58779,   0,   0,   0],
                   [ 0,   0.58779,   0.80902,   0,   0,   0],
                   [ 0,  -0.22123,   1.39680,   1,   0,   0],
                   [ 1,  -1.17557,  -1.61803,   0,   0.80902,  -0.58779],
                   [-1,   1.61803,  -1.17557,   0,   0.58779,   0.80902]
                ])
        Am = adj(composeTrans(R, p))
        assert allclose(A,Am)
        
    
    def testExp(self):
        (w1,w2,w3,t) = symbols('w1 w2 w3 t')
        ct = cos(t)
        st = sin(t)
        
        w = array([[w1,w2,w3]]).T
        
        ex = array([[ 1.0 +(1-ct)*(-w2**2-w3**2),  w1*w2*(1-ct)-w3*st,     w1*w3*(1-ct)+w2*st],
                    [w1*w2*(1-ct)+w3*st,        1.0 +(1-ct)*(-w1**2-w3**2),     w2*w3*(1-ct)-w1*st],
                    [w1*w3*(1-ct)-w2*st, w2*w3*(1-ct)+w1*st,  1.0 +(1-ct)*(-w1**2-w2**2)] 
                     ])
        
        exm = exp(w,t)
        
        assert array_equal(ex,exm)
    
    def testLogTranslation(self):
        
        #translation
        p = array([[2,1,1]]).T
        
        T= composeTrans(numpy.eye(3),p)
        
        (w,u,theta,h) = log(T)
        assert array_equal(p,u) and array_equal(w,numpy.zeros((3,1))) and theta == 1
        Tm = exp(composeScrew(w, u),theta)
        
        assert array_equal(T, Tm)
    
    def testLogRotation(self):
        t = math.pi/5
        ct = math.cos(t)
        st = math.sin(t)
        
        R = array([[1,0,0],
                   [0,ct,-st],
                   [0,st,ct]
                   ])
        T= composeTrans(R,numpy.zeros((3,1)))
        
        (w,u,theta,h) = log(T)
        
        Tm = exp(composeScrew(w, u),theta)
        
        assert array_equal(T, Tm)
        
    def testLogRotTrans(self):
        t = math.pi/5
        ct = math.cos(t)
        st = math.sin(t)
        
        R = array([[1,0,0],
                   [0,ct,-st],
                   [0,st,ct]
                   ])
        we = array([[1,0,0]]).T
        
        Re = exp(we, t)
        
        assert array_equal(R, Re)
        
        p = array([[2,1,1]]).T
        
        T= composeTrans(R,p)
        
        (w,u,theta,h) = log(T)
        assert array_equal(we, w) and theta == t
        
        Tm = exp(composeScrew(w, u),theta)
        
        print(T==Tm)
        assert array_equal(T, Tm)
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()