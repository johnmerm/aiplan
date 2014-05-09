from math import *
import random

class matrix:
    
    def __init__(self, value):
        self.value = value
        self.dimx  = len(value)
        self.dimy  = len(value[0])
        if value == [[]]:
            self.dimx = 0
    
    def __getitem__(self,n):
        if (self.dimx ==1):
            return self.value[0][n]
        elif (self.dimy ==1):
            return self.value[n][0]
        else:
            return self.value[n]
    
    def zero(self, dimx, dimy):
        # check if valid dimensions
        if dimx < 1 or dimy < 1:
            raise ValueError, "Invalid size of matrix"
        else:
            self.dimx  = dimx
            self.dimy  = dimy
            self.value = [[0 for row in range(dimy)] for col in range(dimx)]

    def identity(self, dim):
        # check if valid dimension
        if dim < 1:
            raise ValueError, "Invalid size of matrix"
        else:
            self.dimx  = dim
            self.dimy  = dim
            self.value = [[0 for row in range(dim)] for col in range(dim)]
            for i in range(dim):
                self.value[i][i] = 1

    def show(self):
        for i in range(self.dimx):
            print self.value[i]
        print ' '


    def __add__(self, other):
        # check if correct dimensions
        if self.dimx != other.dimx or self.dimx != other.dimx:
            raise ValueError, "Matrices must be of equal dimension to add"
        else:
            # add if correct dimensions
            res = matrix([[]])
            res.zero(self.dimx, self.dimy)
            for i in range(self.dimx):
                for j in range(self.dimy):
                    res.value[i][j] = self.value[i][j] + other.value[i][j]
            return res

    def __sub__(self, other):
        # check if correct dimensions
        if self.dimx != other.dimx or self.dimx != other.dimx:
            raise ValueError, "Matrices must be of equal dimension to subtract"
        else:
            # subtract if correct dimensions
            res = matrix([[]])
            res.zero(self.dimx, self.dimy)
            for i in range(self.dimx):
                for j in range(self.dimy):
                    res.value[i][j] = self.value[i][j] - other.value[i][j]
            return res

    def __mul__(self, other):
        # check if correct dimensions
        if self.dimy != other.dimx:
            raise ValueError, "Matrices must be m*n and n*p to multiply"
        else:
            # multiply if correct dimensions
            res = matrix([[]])
            res.zero(self.dimx, other.dimy)
            for i in range(self.dimx):
                for j in range(other.dimy):
                    for k in range(self.dimy):
                        res.value[i][j] += self.value[i][k] * other.value[k][j]
        return res

    def transpose(self):
        # compute transpose
        res = matrix([[]])
        res.zero(self.dimy, self.dimx)
        for i in range(self.dimx):
            for j in range(self.dimy):
                res.value[j][i] = self.value[i][j]
        return res


    def Cholesky(self, ztol= 1.0e-5):
        # Computes the upper triangular Cholesky factorization of  
        # a positive definite matrix.
        # This code is based on http://adorio-research.org/wordpress/?p=4560
        res = matrix([[]])
        res.zero(self.dimx, self.dimx)

        for i in range(self.dimx):
            S = sum([(res.value[k][i])**2 for k in range(i)])
            d = self.value[i][i] - S
            if abs(d) < ztol:
                res.value[i][i] = 0.0
            else: 
                if d < 0.0:
                    raise ValueError, "Matrix not positive-definite"
                res.value[i][i] = sqrt(d)
            for j in range(i+1, self.dimx):
                S = sum([res.value[k][i] * res.value[k][j] for k in range(i)])
                if abs(S) < ztol:
                    S = 0.0
                res.value[i][j] = (self.value[i][j] - S)/res.value[i][i]
        return res 
 
    def CholeskyInverse(self):
    # Computes inverse of matrix given its Cholesky upper Triangular
    # decomposition of matrix.
        # This code is based on http://adorio-research.org/wordpress/?p=4560

        res = matrix([[]])
        res.zero(self.dimx, self.dimx)

    # Backward step for inverse.
        for j in reversed(range(self.dimx)):
            tjj = self.value[j][j]
            S = sum([self.value[j][k]*res.value[j][k] for k in range(j+1, self.dimx)])
            res.value[j][j] = 1.0/ tjj**2 - S/ tjj
        for i in reversed(range(j)):
                res.value[j][i] = res.value[i][j] = -sum([self.value[i][k]*res.value[k][j] for k in range(i+1,self.dimx)])/self.value[i][i]
        return res
    

    def inverse(self):
        try:
            aux = self.Cholesky()
            res = aux.CholeskyInverse()
        except ValueError:
            res = invertMatrix(self)
        return res

    def __repr__(self):
        return repr(self.value)
    
    
    def __neg__(self):
        value = [[-self.value[i][j] for j in range(self.dimy)] for i in range(self.dimx)]
        return matrix(value)
    def __len__(self):
        if self.dimx == self.dimy or self.dimy == 1:
            return self.dimx 
        elif (self.dimx == 1):
            return self.dimy
        else:
            return (self.dimx,self.dimy)
    


S = matrix([[-508.62686317011776, -1343.0506079993277],[-1343.050607999328, -3165.606134252321]])

def addMultipleOfRowOfSquareMatrix(m, sourceRow, k, targetRow):
    # add k * sourceRow to targetRow of matrix m
    n = len(m)
    rowOperator = matrix([[1 if i==j  else 0 for j in range(n)]for i in range(n)])
    rowOperator[targetRow][sourceRow] = k
    return rowOperator* m


def multiplyRowOfSquareMatrix(m, row, k):
    n = len(m)
    rowOperator = matrix([[1 if i==j  else 0 for j in range(n)]for i in range(n)])
    rowOperator[row][row] = k
    return rowOperator* m

def invertMatrix(m):
    n = len(m)
    assert(len(m) == len(m[0]))
    inverse = matrix([[1 if i==j  else 0 for j in range(n)]for i in range(n)]) # this will BECOME the inverse eventually
    for col in range(n):
        # 1. make the diagonal contain a 1
        diagonalRow = col
#         assert(m[diagonalRow][col] != 0) # @TODO: actually, we could swap rows
#                                          # here, or if no other row has a 0 in
#                                          # this column, then we have a singular
#                                          # (non-invertible) matrix.  Let's not
#                                          # worry about that for now.  :-)
        k = 1/m[diagonalRow][col]
        
        m = multiplyRowOfSquareMatrix(m, diagonalRow, k)
        inverse = multiplyRowOfSquareMatrix(inverse, diagonalRow, k)
        # 2. use the 1 on the diagonal to make everything else
        #    in this column a 0
        sourceRow = diagonalRow
        for targetRow in xrange(n):
            if (sourceRow != targetRow):
                k = -m[targetRow][col]
                m = addMultipleOfRowOfSquareMatrix(m, sourceRow, k, targetRow)
                inverse = addMultipleOfRowOfSquareMatrix(inverse, sourceRow,
                                                         k, targetRow)
    # that's it!
    return inverse

print S.inverse()