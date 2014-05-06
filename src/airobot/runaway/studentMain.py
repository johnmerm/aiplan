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
    
    
    prob = Gaussian(p.x, p.measurement_noise, measurement[0])*Gaussian(p.y, p.measurement_noise, measurement[1])
    return prob


def avg(l):
    return sum(l)/len(l)
class predict:
    def __init__(self,measurement):
        self.measurements = [measurement]
        self.alphas = None
        
    
    def update(self,measurement):
        x_prev = self.measurements[-1][0]
        y_prev = self.measurements[-1][1]
        dx = measurement[0]-x_prev
        dy = measurement[1]-y_prev
        
        self.measurements.append(measurement)
            
        s = sqrt(dx**2+dy**2);
        a = atan2(dy,dx);
        if not self.alphas:
            self.steps = [s]
            self.alphas = [a]
            self.d_alphas = []
            self.thetas = []
            self.x0 = []
            self.y0 = []
            return s,0,0,0,0
        else:
            self.steps.append(s)
            a_prev = self.alphas[-1]
            while abs(a - a_prev)>pi:
                a += 2*pi
            self.alphas.append(a)
            da = a - a_prev
            theta = a - len(self.alphas)*da
            self.d_alphas.append(da)
            self.thetas.append(theta)
            
            
            
            s_avg = avg(self.steps)
            th_avg  =avg(self.thetas)
            da_avg = avg(self.d_alphas)
            
            dxs = sum([s_avg*cos(th_avg+i*da_avg) for i in range(1,len(self.measurements))])
            dys = sum([s_avg*sin(th_avg+i*da_avg) for i in range(1,len(self.measurements))])
            
            x0 = measurement[0]-dxs
            y0 = measurement[1]-dys
            
            self.x0.append(x0)
            self.y0.append(y0)
            
            return  s_avg,th_avg,da_avg,avg(self.x0),avg(self.y0)
            
    def predict(self):
        if len(self.thetas)<1:
            return None
        
        
        s_avg = avg(self.steps)
        th_avg  =avg(self.thetas)
        da_avg = avg(self.d_alphas)
        
        x0 = avg(self.x0)
        y0 = avg(self.y0)
        
        dxs = sum([s_avg*cos(th_avg+i*da_avg) for i in range(1,len(self.measurements)+1)])
        dys = sum([s_avg*sin(th_avg+i*da_avg) for i in range(1,len(self.measurements)+1)])
        
        return (x0+dxs,y0+dys)
        
        
            
    

  
def estimate_next_pos(measurement, OTHER = None):
    #print(measurement)
    
    correct = (1.5,0.5,2*pi/34,2.1,4.3)
    if not OTHER:
        OTHER =predict(measurement)
        return measurement,OTHER
    else:
        est = OTHER.update(measurement)
        print([correct[i]-est[i] for i in range(len(est))])
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
    while not localized and ctr <= 100: 
        ctr += 1
        
        
        measurement = target_bot.sense()
        position_guess, OTHER = estimate_next_pos_fcn(measurement, OTHER)
        target_bot.move_in_circle()
        true_position = (target_bot.x, target_bot.y)
        error = distance_between(position_guess, true_position)
        #print(error)
        if error <= distance_tolerance:
            print ("You got it right! It took you ", ctr, " steps to localize.")
            localized = True
        if ctr == 100:
            print ("Sorry, it took you too many steps to localize the target.")
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
measurement_noise = .05 * test_target.distance
test_target.set_noise(0.0, 0.0, measurement_noise)


demo_grading(estimate_next_pos, test_target)
