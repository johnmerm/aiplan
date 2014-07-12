import numpy as np
import sympy as sp
from sympy import  cos,sin,sqrt,cot,pi,acos
import math


def bra(x):
    if x.shape[1] != 1:
        raise RuntimeError('Not a vec:'+str(x.shape))
    elif x.shape[0] == 3:
        #cannot check length since we use symbols 
        #if (np.linalg.norm(x)-1) > 1e-0.5:
        #    raise RuntimeError(str(x)+" has length of "+str(np.linalg.norm(x))+" !=1 ")
        return np.array([
                        [0, -x[2][0], x[1][0] ],
                        [x[2][0], 0, -x[0][0] ],
                        [-x[1][0], x[0][0], 0 ]
                        ])
    elif x.shape[0]==6:
        w = np.array([x[i] for i in range(3)])
        u = np.array([x[i] for i in range(3,6)])
        return np.array([[0, -w[2][0], w[1][0], u[0][0] ],
                     [w[2][0], 0, -w[0][0], u[1][0] ],
                     [-w[1][0], w[0][0], 0, u[2][0] ],
                     [0, 0, 0, 0]
                    ])
    else:
        raise RuntimeError('invalid vec dimension:'+str(x.shape))

def ibra(W):
    if W.shape[0]==3 and W.shape[1]==3:
        w = np.array([[W[2][1]],
                      [W[0][2]],
                      [W[1][0]]
                      ])
        return w
    elif W.shape[0]==4 and W.shape[1]==4:
        w = np.array([[W[2][1]],
                      [W[0][2]],
                      [W[1][0]],
                      [W[0][3]],
                      [W[1][3]],
                      [W[2][3]],
                      ])
        return w
    else:
        raise RuntimeError('Invalid bra shape:'+str(W.shape))
    
def breakTrans(T):
    if not (T.shape[0]==4 and T.shape[1]==4):
        raise RuntimeError('Invalid transformation matrix shape:'+str(T.shape))
    else:
        R = np.array([[T[i][j] for j in range(3)] for i in range(3)])
        p = np.array([ [T[j][3]] for j in range(3)])
        return (R,p)
    
def composeTrans(R,p):
    T = [[0 for j in range(4)] for i in range(4)]
    for i in range(3):
        for j in range(3):
            T[i][j] = R[i][j]
        T[i][3] = p[i][0]
    T[3][3] = 1
    return np.array(T)

def composeScrew(w,u):
    assert w.shape[0]==3 and w.shape[1]==1 and u.shape[0]==3 and u.shape[1]==1
    S = np.array([[w[0][0]],
                  [w[1][0]],
                  [w[2][0]],
                  [u[0][0]],
                  [u[1][0]],
                  [u[2][0]],
                  ])
    return S

def breakScrew(S):
    assert S.shape[0]==6 and S.shape[1]==1
    w = np.array([
                  [S[0][0]],
                  [S[1][0]],
                  [S[2][0]],
                ])
    u = np.array([
                  [S[3][0]],
                  [S[4][0]],
                  [S[5][0]],
                ])
    return (w,u)

def adj(T):
    R,p = breakTrans(T)
    
    P = bra(p)
    PR = np.dot(P,R)
    
    A = np.zeros((6,6))
    for i in range(3):
        for j in range(3):
            A[i][j] = R[i][j]
            A[i+3][j+3] = R[i][j]
            A[i+3][j] = PR[i][j]
    return A
        


def exp(x,theta) : 
    if x.shape[0]==3 and x.shape[1]==1:
        W = bra(x)
        I = np.eye(W.shape[0])
        W2 = np.dot(W,W)
        
        return I + sin(theta)*W + (1-cos(theta))*W2
    elif x.shape[0]==6 and x.shape[1]==1:
        (w,u) = breakScrew(x)
        
        W = bra(w)
        I = np.eye(W.shape[0])
        W2 = np.dot(W,W)
        
        wth = I + sin(theta)*W + (1-cos(theta))*W2
        
        uth_1 = theta*I 
        uth_2 = (1-cos(theta))*W 
        uth_3 = (theta-sin(theta))*W2
        
        uth = np.dot(uth_1+uth_2+uth_3,u)
        
        E = np.concatenate((wth,uth),axis=1)
        E = np.concatenate((E,np.array([[0,0,0,1]])),axis=0)
        
        return E
        

def log(T):
    (R,p) = breakTrans(T)
    if np.array_equiv(R, np.eye(3)):
        w = np.zeros((3,1))
        theta = 1
        u = p
        
    else:
        tr = R.trace()
        if tr == -1:
            theta = -math.pi
            w = np.array([[ sqrt((R[i][i]+1)/2) for i in range(3)]]).T
            W = bra(w)
        else:
            theta = acos((tr-1)/2)
            W = (1/(2*sin(theta)))*(R-R.T)
            w = ibra(W)
        
        W2 = np.dot(W,W)
        G1 = 1./theta*np.eye(3)
        G2 = 0.5*W
        G3 = (1./theta-cot(theta/2)/2)*W2
        G = G1+G2+G3
        # This corrrects the bug!!!!!
        G = G.T
        u = np.dot(G,p)
    
    h = np.dot(w.T,u)
    return (w,u,theta,h)
          
            
        
        
        
