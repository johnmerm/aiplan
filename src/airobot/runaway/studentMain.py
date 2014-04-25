# ----------
# Background
# 
# A robotics company named Trax has created a line of small self-driving robots 
# designed to autonomously traverse desert environments in search of undiscovered
# water deposits.
#
# A Traxbot looks like a small tank. Each one is about half a meter long and drives
# on two continuous metal tracks. In order to maneuver itself, a Traxbot can do one
# of two things: it can drive in a straight line or it can turn. So to make a 
# right turn, A Traxbot will drive forward, stop, turn 90 degrees, then continue
# driving straight.
#
# This series of questions involves the recovery of a rogue Traxbot. This bot has 
# gotten lost somewhere in the desert and is now stuck driving in an almost-circle: it has
# been repeatedly driving forward by some step size, stopping, turning a certain 
# amount, and repeating this process... Luckily, the Traxbot is still sending all
# of its sensor data back to headquarters.
#
# In this project, we will start with a simple version of this problem and 
# gradually add complexity. By the end, you will have a fully articulated
# plan for recovering the lost Traxbot.
# 
# ----------
# Part One
#
# Let's start by thinking about circular motion (well, really it's polygon motion
# that is close to circular motion). Assume that Traxbot lives on 
# an (x, y) coordinate plane and (for now) is sending you PERFECTLY ACCURATE sensor 
# measurements. 
#
# With a few measurements you should be able to figure out the step size and the 
# turning angle that Traxbot is moving with.
# With these two pieces of information, you should be able to 
# write a function that can predict Traxbot's next location.
#
# You can use the robot class that is already written to make your life easier. 
# You should re-familiarize yourself with this class, since some of the details
# have changed. 
#
# ----------
# YOUR JOB
#
# Complete the estimate_next_pos function. You will probably want to use
# the OTHER variable to keep track of information about the runaway robot.
#
# ----------
# GRADING
# 
# We will make repeated calls to your estimate_next_pos function. After
# each call, we will compare your estimated position to the robot's true
# position. As soon as you are within 0.01 stepsizes of the true position,
# you will be marked correct and we will tell you how many steps it took
# before your function successfully located the target bot.

# These import steps give you access to libraries which you may (or may
# not) want to use.
from robot import *
from math import *
from matrix import *
import random
from pymongo.mongo_replica_set_client import OTHER


# This is the function you have to write. The argument 'measurement' is a 
# single (x, y) point. This function will have to be called multiple
# times before you have enough information to accurately predict the
# next position. The OTHER variable that your function returns will be 
# passed back to your function the next time it is called. You can use
# this to keep track of important information over time.
def estimate_next_pos_avg(measurement, OTHER = None):
    if not OTHER:
        OTHER={'idx':0,'measurement':measurement,'est_step':0,'est_diff_angle':0,'angle':0,'est_x':measurement[0],'est_y':measurement[1]}
        return measurement,OTHER
    else:
        old_measurement = OTHER['measurement']
        old_angle = OTHER['angle']
        
        idx = OTHER['idx']+1
        diff = (measurement[0]-old_measurement[0],measurement[1]-old_measurement[1])
        
        meas_step =distance_between(measurement, old_measurement)
        old_est_step = OTHER['est_step']
        est_step = (old_est_step*(idx-1)+meas_step)/idx
        
        meas_angle = atan2(measurement[1], measurement[0])
        old_angle = OTHER['angle']
        est_diff_angle = meas_angle - old_angle
        est_diff_angle = (est_diff_angle*(idx-1)+meas_angle)/idx
        
        est_angle = old_angle + est_diff_angle
        
        est_x = OTHER['est_x']+est_step*cos(est_angle)
        est_y = OTHER['est_y']+est_step*sin(est_angle)
        
        OTHER['idx'] = idx
        OTHER['est_x'] = est_x
        OTHER['est_y'] = est_y
        
        OTHER['angle'] = meas_angle
        OTHER['est_step'] = est_step
        OTHER['est_diff_angle'] = est_diff_angle
        OTHER['measurement']=measurement
        print(est_step,est_diff_angle,est_angle)
        return (est_x,est_y),OTHER
        
def estimate_next_pos_kalman(measurement, OTHER = None):
    """Estimate the next (x, y) position of the wandering Traxbot
    based on noisy (x, y) measurements."""

    # You must return xy_estimate (x, y), and OTHER (even if it is None) 
    # in this order for grading purposes.
    
    
    class KalmanFilter:
        def __init__(self,x,F,H,P,u,R,I):
            self.x = x 
            self.P = P
            self.u = u
            self.F = F
            self.H = H
            self.R = R
            self.I = I
        
        def update(self,ms):
            # measurement update
            Z = matrix([list(ms)]).transpose()
            y = Z- (self.H * self.x)
            S = self.H * self.P * self.H.transpose() + self.R
            K = self.P * self.H.transpose() * S.inverse()
            self.x = self.x + (K * y)
            self.P = (self.I - (K * self.H)) * self.P
            # prediction
            
            self.x = (self.F * self.x) + self.u
            self.P = self.F*self.P*self.F.transpose()
            
            return (self.x,self.P)
    
    #x = [x,y,dx,dy]   initial state (location and velocity)
    #F = [1. 0. 1. 0.] next state function
    #    [0. 1. 0. 1.]
    #    [0. 0. 1. 0.]
    #    [0. 0. 0. 1.]
    #H = [1. 0. 0. 0.] # measurement function
    #    [0. 1. 0. 0.]
    if not OTHER:
        x = matrix([[measurement[0]],[measurement[1]],[0.],[0.]]) 
        F = matrix([[1., 0.,1.,0.],[0.,1.,0.,1.],[0., 0.,1.,0.],[0.,0.,0.,1.]]) 
        H = matrix([[1., 0.,0.,0.],[0.,1.,0.,0.]])
        P = matrix([[1000. if i==j else 0 for j in range(x.dimx)] for i in range(x.dimx)]) # initial uncertainty
        u = matrix([[0. for j in range(x.dimx)] for i in range(x.dimx)]) # external motion
        
        measurement_uncertainty = 5.0
        I = matrix([[1.if i==j else 0. for j in range(x.dimx)] for i in range(x.dimx)]) # identity matrix
        R = matrix([[measurement_uncertainty if i==j else 0. for j in range(len(measurement))]for i in range(len(measurement))]) #measurement uncertainty
        OTHER = KalmanFilter(x, F, H, P, u, R, I)
        return measurement,OTHER
    else:
        OTHER.update(measurement)
        x= OTHER.x.value
        
        xy_estimate = (x[0][0],x[1][0])
        return xy_estimate,OTHER

def estimate_next_pos_ekf(measurement, OTHER = None):
    if not OTHER:
        class ExtendedKalmanFilter:
            def __init__(self,x,f,h,F,H,P,u,R,I):
                self.x = x 
                self.f = f
                self.h = h
                self.P = P
                self.u = u
                self.F = F
                self.H = H
                self.R = R
                self.I = I
            
            def update(self,ms):
                #predict
                F = self.F(self.x)
                x = self.f(self.x)
                P = F*self.P*F.transpose()
                
                #update model
                H = self.H(self.x)
                Z = matrix([list(ms)]).transpose()
                y = Z- self.h(ms)
                S = H*P*H.transpose()  + R
                K = P*H.transpose()*S.inverse()
                x = x + K*y
                P = (I-K*H)*P
                
                self.x = x
                self.P = P
                return (x,P)
        
        x = [measurement[0],measurement[1],0,0,0]
        
        f = lambda x: matrix([[x[0]+x[2]*cos(x[3]+x[4])],
                              [x[1]+x[2]*sin(x[3]+x[4])],
                              [x[2]+x[4]],
                              [x[3]],
                              [x[4]] 
                              ])
        F = lambda x: matrix([ [1, 0, -x[2]*sin(x[3]+x[4]), cos(x[3]+x[4]), -x[2]*sin(x[3]+x[4]) ],
                               [0, 1, x[2]*cos(x[3]+x[4]) , sin(x[3]+x[4]),  x[2]*cos(x[3]+x[4]) ],
                               [0, 0, 1 ,0 ,1],
                               [0, 0, 0, 1, 0],
                               [0, 0, 0, 0, 1]
                              ])
        h = lambda m: matrix([[m[0]],
                              [m[1]],
                              [atan2(m[1],m[0])]
                            ])
                               
        H = lambda x: matrix([[1,0,0,0,0],
                              [0,1,0,0,0],
                              [-x[1]/(x[0]**2+x[1]**2),x[0]/(x[0]**2+x[1]**2)]
                              ]) 
        I = matrix([[1. if i==j else 0 for j in range(5)]for i in range(5)])
        
        P = matrix([[1000. if i==j else 0 for j in range(5)]for i in range(5)])
        R = matrix([[5. if i==j else 0 for j in range(2)]for i in range(2)])
        
        u = matrix([[0] for i in range(5)])
        
        
        OTHER = ExtendedKalmanFilter(x, f, h, F, H, P, u, R, I)
        return measurement,OTHER
    else:
        (x,P) = OTHER.update(measurement)
        xy_estimate =(x[0],x[1])
        return xy_estimate,OTHER
    pass

def estimate_next_pos(measurement, OTHER = None):
    return estimate_next_pos_ekf(measurement, OTHER)
# A helper function you may find useful.
def distance_between(point1, point2):
    """Computes distance between point1 and point2. Points are (x, y) pairs."""
    x1, y1 = point1
    x2, y2 = point2
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

# This is here to give you a sense for how we will be running and grading
# your code. Note that the OTHER variable allows you to store any 
# information that you want. 
def demo_grading(estimate_next_pos_fcn, target_bot, OTHER = None):
    localized = False
    distance_tolerance = 0.01 * target_bot.distance
    ctr = 0
    # if you haven't localized the target bot, make a guess about the next
    # position, then we move the bot and compare your guess to the true
    # next position. When you are close enough, we stop checking.
    while not localized and ctr <= 10: 
        ctr += 1
        measurement = target_bot.sense()
        position_guess, OTHER = estimate_next_pos_fcn(measurement, OTHER)
        target_bot.move_in_circle()
        true_position = (target_bot.x, target_bot.y)
        error = distance_between(position_guess, true_position)
        
        if error <= distance_tolerance:
            print "You got it right! It took you ", ctr, " steps to localize."
            localized = True
        if ctr == 10:
            print "Sorry, it took you too many steps to localize the target."
    return localized

# This is a demo for what a strategy could look like. This one isn't very good.
def naive_next_pos(measurement, OTHER = None):
    """This strategy records the first reported position of the target and
    assumes that eventually the target bot will eventually return to that 
    position, so it always guesses that the first position will be the next."""
    if not OTHER: # this is the first measurement
        OTHER = measurement
    xy_estimate = OTHER 
    return xy_estimate, OTHER

# This is how we create a target bot. Check the robot.py file to understand
# How the robot class behaves.
# This is how we create a target bot. Check the robot.py file to understand
# How the robot class behaves.
test_target = robot(2.1, 4.3, 0.5, 2*pi / 34.0, 1.5)
measurement_noise = 0.05 * test_target.distance
test_target.set_noise(0.0, 0.0, measurement_noise)


demo_grading(estimate_next_pos, test_target)
