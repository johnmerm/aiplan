'''
Created on Jul 10, 2014

@author: grmsjac6
'''


import numpy as np
import sympy as sp
from sympy import  sqrt,cos,sin,pi

w = np.array([[1/sp.sqrt(2),1/sp.sqrt(2),0]]).T

bra =lambda x:np.array([
                        [0,-x[[2]],x[[1]] ],
                        [x[[2]],0,-x[[0]] ],
                        [-x[[1]],x[[0]],0 ]
                        ])
bra4 =lambda (x,y) : np.array([
                               [0,-x[[2]],x[[1]], y[[0]] ],
                               [x[[2]],0,-x[[0]],y[[1]] ],
                               [-x[[1]],x[[0]],0,y[[2]] ],
                               [0,0,0,0]
                               ])

exp = lambda(w,theta) : np.eye(3)+sin(theta)*bra(w)+(1-cos(theta))*bra(w)*bra(w)

exp4 = lambda(w,u,theta) : np.eye(4)+sin(theta)*bra4((w,u))+(1-cos(theta))*bra4((w,u))*bra4((w,u))