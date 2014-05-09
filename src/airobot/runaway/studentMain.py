# ----------
# Part Two
#
# Now we'll make the scenario a bit more realistic. Now Traxbot's
# sensor measurements are a bit noisy (though its motions are still
# completetly noise-free and it still moves in an almost-circle).
# You'll have to write a function that takes as input the next
# noisy (x, y) sensor measurement and outputs the best guess 
# for the robot's next position.
#
# ----------
# YOUR JOB
#
# Complete the function estimate_next_pos. You will be considered 
# correct if your estimate is within 0.01 stepsizes of Traxbot's next
# true position. 
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
from robot import *  # Check the robot.py tab to see how this works.
from math import *
from matrix import matrix # Check the matrix.py tab to see how this works.
import random

# This is the function you have to write. Note that measurement is a 
# single (x, y) point. This function will have to be called multiple
# times before you have enough information to accurately predict the
# next position. The OTHER variable that your function returns will be 
# passed back to your function the next time it is called. You can use
# this to keep track of important information over time.
class ExtendedKalman:
    ''' An extended Kalman Filter with state vars x,y,th,s,dth and observable x,y'''
    def __init__(self):
        self.measurement = None
        self.x = matrix([[0.] for i in range(5)])
        
        self.f = lambda x:matrix([
                                  [x[0]+x[3]*cos(x[2]+x[4])],
                                  [x[1]+x[3]*sin(x[2]+x[4])],
                                  [x[2]+x[4]],
                                  [x[3]],
                                  [x[4]]])
    
        self.h = lambda x:matrix([
                                  [x[0]],
                                  [x[1]] 
                                  ]) 
#         [ 1, 0, -s*sin(dt + t), cos(dt + t), -s*sin(dt + t)]
#         [ 0, 1,  s*cos(dt + t), sin(dt + t),  s*cos(dt + t)]
#         [ 0, 0,              1,           0,              1]
#         [ 0, 0,              0,           1,              0]
#         [ 0, 0,              0,           0,              1]
        self.F = lambda x:matrix([[1., 0.,-x[3]*sin(x[2]+x[4]), cos(x[2]+x[4]),-x[3]*sin(x[2]+x[4])],
                                  [0., 1., x[3]*cos(x[2]+x[4]), sin(x[2]+x[4]), x[3]*cos(x[2]+x[4])],
                                  [0.,0.,1.,0.,1.],
                                  [0.,0.,0.,1.,0.], #th = th+dth all others invariants , f is linear, F is const
                                  [0.,0.,0.,0.,1.]])
        
         
        self.H = lambda x:matrix([[1.,0.,0.,0.,0.],
                                  [0.,1.,0.,0.,0.]])
        
        
        self.P =matrix([[100.,0.,0.,0.,0.],
                        [0.,100.,0.,0.,0.],
                        [0.,0.,100.,0.,0.],
                        [0.,0.,0.,100.,0.],    #we are certain abouth initial th
                        [0.,0.,0.,0.,100.]])
         
        self.R = matrix([[15.,0.],[0.,15.]]) #set noise to 5
        self.I = matrix([[1 if i==j else 0. for j in range(5)] for i in range(5)])
    
    
        
    def update(self,measurement):
        
        #predict
        F = self.F(self.x)
        self.x = self.f(self.x)
        self.P = F*self.P*F.transpose()
        
        z = matrix([[measurement[i]] for i in range(len(measurement))])
        H = self.H(self.x)
        y = z- self.h(self.x)
        
        S = H*self.P*H.transpose() + self.R
        try:
            Si = S.inverse()
        except ValueError as v:
            print(S)
            raise v
        
        K = self.P*H.transpose()*Si
        self.x = self.x + K*y
        self.P = (self.I - K*H)*self.P
        
        return self.x,self.P

def estimate_next_pos(measurement, OTHER = None):
    #print(measurement)
    
    if not OTHER:
        OTHER =ExtendedKalman()
        return measurement,OTHER
    else:
        est,P_est = OTHER.update(measurement)
        next_xy_est = OTHER.h(OTHER.f(est))
        return next_xy_est,OTHER


def next_move(hunter_position, hunter_heading, target_measurement, max_distance, OTHER,init_wait_steps = 50):
    if not OTHER:
        OTHER = {'step':0,'ekf':ExtendedKalman()}
    
    step = OTHER['step']
    ekf = OTHER['ekf']
    
    
    est,P_est = ekf.update(target_measurement)
    if step < init_wait_steps: #for the first 20 steps, accumulate measurements and proceed with naive
        heading_to_target = get_heading(hunter_position, target_measurement)
        heading_difference = heading_to_target - hunter_heading
        turning =  heading_difference # turn towards the target
        distance = max_distance # full speed ahead!
    elif step == init_wait_steps:
        #build the trajectory estimation
        est_xy = ekf.h(est)
        min_dist = 65535
        est_tgt = est_xy
        
        period = ceil(2*pi/est[4])
        period = int(period)
        traj = []
        est_tgt = est
        min_dist = 65535
        
        for i in range(period):
            
            dist = distance_between(hunter_position, ekf.h(est_tgt))
            if dist<min_dist:
                min_dist = dist
                tgt = ekf.h(est_tgt) 
            traj.append([ekf.h(est_tgt),dist])
            est_tgt = ekf.f(est_tgt)
        
        eta = ceil(min_dist/max_distance)
        
        heading_to_target = get_heading(hunter_position, tgt)
        heading_difference = heading_to_target - hunter_heading
        turning =  heading_difference # turn towards the target
        distance = max_distance # full speed ahead!
        OTHER['tgt'] = tgt
        OTHER['eta'] = eta
    else:
        tgt = OTHER['tgt']
        eta = OTHER['eta']
        eta -=1
        
        if eta > 1:
            distance = max_distance # full speed ahead!  
        else:
            tgt = ekf.h(ekf.f(est))
            distance = distance_between(hunter_position, tgt) 
            
        heading_to_target = get_heading(hunter_position, tgt)
        heading_difference = heading_to_target - hunter_heading
        turning =  heading_difference # turn towards the target
        
        OTHER['eta'] = eta
    
    step +=1
    OTHER['step'] = step
         
    return turning, distance, OTHER
# A helper function you may find useful.
def distance_between(point1, point2):
    """Computes distance between point1 and point2. Points are (x, y) pairs."""
    x1, y1 = point1
    x2, y2 = point2
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def demo_grading(hunter_bot, target_bot, next_move_fcn, OTHER = None):
    """Returns True if your next_move_fcn successfully guides the hunter_bot
    to the target_bot. This function is here to help you understand how we 
    will grade your submission."""
    max_distance = 1.94 * target_bot.distance # 1.94 is an example. It will change.
    separation_tolerance = 0.02 * target_bot.distance # hunter must be within 0.02 step size to catch target
    caught = False
    ctr = 0

    # We will use your next_move_fcn until we catch the target or time expires.
    while not caught and ctr < 1000:

        # Check to see if the hunter has caught the target.
        hunter_position = (hunter_bot.x, hunter_bot.y)
        target_position = (target_bot.x, target_bot.y)
        separation = distance_between(hunter_position, target_position)
        if separation < separation_tolerance:
            print "You got it right! It took you ", ctr, " steps to catch the target."
            caught = True

        # The target broadcasts its noisy measurement
        target_measurement = target_bot.sense()

        # This is where YOUR function will be called.
        turning, distance, OTHER = next_move_fcn(hunter_position, hunter_bot.heading, target_measurement, max_distance, OTHER)
        
        # Don't try to move faster than allowed!
        if distance > max_distance:
            distance = max_distance

        # We move the hunter according to your instructions
        hunter_bot.move(turning, distance)

        # The target continues its (nearly) circular motion.
        target_bot.move_in_circle()

        ctr += 1            
        if ctr >= 1000:
            print "It took too many steps to catch the target."
    return caught



def angle_trunc(a):
    """This maps all angles to a domain of [-pi, pi]"""
    while a < 0.0:
        a += pi * 2
    return ((a + pi) % (pi * 2)) - pi

def get_heading(hunter_position, target_position):
    """Returns the angle, in radians, between the target and hunter positions"""
    hunter_x, hunter_y = hunter_position
    target_x, target_y = target_position
    heading = atan2(target_y - hunter_y, target_x - hunter_x)
    heading = angle_trunc(heading)
    return heading

def naive_next_move(hunter_position, hunter_heading, target_measurement, max_distance, OTHER):
    """This strategy always tries to steer the hunter directly towards where the target last
    said it was and then moves forwards at full speed. This strategy also keeps track of all 
    the target measurements, hunter positions, and hunter headings over time, but it doesn't 
    do anything with that information."""
    if not OTHER: # first time calling this function, set up my OTHER variables.
        measurements = [target_measurement]
        hunter_positions = [hunter_position]
        hunter_headings = [hunter_heading]
        OTHER = (measurements, hunter_positions, hunter_headings) # now I can keep track of history
    else: # not the first time, update my history
        OTHER[0].append(target_measurement)
        OTHER[1].append(hunter_position)
        OTHER[2].append(hunter_heading)
        measurements, hunter_positions, hunter_headings = OTHER # now I can always refer to these variables
    
    heading_to_target = get_heading(hunter_position, target_measurement)
    heading_difference = heading_to_target - hunter_heading
    turning =  heading_difference # turn towards the target
    distance = max_distance # full speed ahead!
    return turning, distance, OTHER

target = robot(0.0, 10.0, 0.0, 2*pi / 30, 1.5)
measurement_noise = .05*target.distance
target.set_noise(0.0, 0.0, measurement_noise)

hunter = robot(-10.0, -10.0, 0.0)

print demo_grading(hunter, target, next_move)
