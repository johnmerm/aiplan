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
from robot import robot,angle_trunc
from math import pi,sqrt,exp, atan2,sin,cos

import random




# This is the function you have to write. The argument 'measurement' is a 
# single (x, y) point. This function will have to be called multiple
# times before you have enough information to accurately predict the
# next position. The OTHER variable that your function returns will be 
# passed back to your function the next time it is called. You can use
# this to keep track of important information over time.

def Gaussian(mu, sigma, x):
    # calculates the probability of x for 1-dim Gaussian with mean mu and var. sigma
    return exp(- ((mu - x) ** 2) / (sigma ** 2) / 2.0) / sqrt(2.0 * pi * (sigma ** 2))

def measurement_prob(p, measurement):
    # calculates how likely a measurement should be
    h_func = lambda x:(x[0],x[1])
    z = h_func(p)
    prob = 1
    for i in range(len(measurement)):
        prob *= Gaussian(measurement[i], measurement_noise, z[i])
    return prob

def avg(l):
    return sum(l)/len(l)


measurement_noise = 0.2

class ParticleFilter:
    def __init__(self):
        self.measurements = []
        self.filters = None
    
    def update(self,measurement):
        self.measurements.append(measurement)
        if len(self.measurements)==2:
            self.filters = self.initialize(self.measurements)
        elif len(self.measurements)>2:
            self.filters = self.run(self.measurements)
    
    def predict(self):
        fv = max(self.filters.items(),lambda v:v[1])
        return fv[0][0],fv[0][1]
    def run(self,filters,measurement):
        upd = lambda x:(x[0]+x[3]*cos(x[2]+x[4]),
                        x[1]+x[3]*sin(x[2]+x[4]),
                        x[2]+x[4],
                        x[3],
                        x[4])
        filters_2 ={upd(p) for p in filters.keys()} 
        mm = {p:measurement_prob(p,measurement) for p in filters_2}
        mm_sum = sum(mm.values())
        mm = {p:(v/mm_sum) for p,v in mm.items()}
        filters_3 = {p:v for (p,v) in mm.items() if v>random.random()}
        return filters_3
    
    def initialize(self,measurements):
        
        if not len(measurements)==3:
            return None
        
        dx=measurements[2][0]-measurements[1][0]
        dy=measurements[2][1]-measurements[1][1]
        
        s = sqrt(dx**2 + dy**2)
        a = atan2(dx,dy)
        
        
        dx2 = measurements[1][0]-measurements[0][0]
        dy2 = measurements[1][1]-measurements[0][1]
        s2 = sqrt(dx2**2 + dy2**2)
        a2 = atan2(dx,dy)
        
        s = (s+s2)/2
        da = a2 - a
        theta = a - da
        
        
        N = 1000 #samples per dimension
        
        x0 = measurements[0][0]
        y0 = measurements[0][1]
        filters = {}
        for i in range(N):
            xp = random.gauss(x0,measurement_noise)
            yp = random.gauss(y0,measurement_noise)
            thp = random.gauss(theta,2*measurement_noise)
            sp = random.gauss(s,measurement_noise)
            dap = random.gauss(da,2*measurement_noise)
            
            f = (xp,yp,thp,sp,dap)
            filters[f]=1./N
            
        filters = self.run(filters,measurements[1])
        filters = self.run(filters,measurements[2])
        return filters
                
            
                 
  
        
def estimate_next_pos(measurement, OTHER = None):
    #print(measurement)
    
    correct = (1.5,0.5,2*pi/34,2.1,4.3)
    if not OTHER:
        OTHER =predict(measurement)
        return measurement,OTHER
    else:
        est = OTHER.update(measurement)
        #print([correct[i]-est[i] for i in range(len(est))])
        xy_est = OTHER.predict()
        if not xy_est:
            xy_est = measurement
        return xy_est,OTHER
    
        
        
    
    
    
            
    
    
    
    
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
    while not localized and ctr <1000: 
        ctr += 1
        
        
        measurement = target_bot.sense()
        position_guess, OTHER = estimate_next_pos_fcn(measurement, OTHER)
        target_bot.move_in_circle()
        true_position = (target_bot.x, target_bot.y)
        error = distance_between(position_guess, true_position)
        #print(error)
        if error <= distance_tolerance:
            #print ("You got it right! It took you ", ctr, " steps to localize.")
            localized = True
        #if ctr == 100:
        #    print ("Sorry, it took you too many steps to localize the target.")
    
    return ctr

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
measurement_noise = .05 * test_target.distance
test_target.set_noise(0.0, 0.0, measurement_noise)


print(demo_grading(estimate_next_pos, test_target))
