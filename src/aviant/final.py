import math
import numpy as np
from plot import plot, plot_trajectory, plot_covariance_2d

class PID:
    def __init__(self):
        Kp_xy = 1.5  # xy proportional
        Kd_xy = 1.5  # xy differential

        self.Kp = np.array([[1, 1,0.5]]).T
        self.Kd = np.array([[1, 1,1]]).T

        self.err_prev = np.zeros((3, 1))


    def compute_control_command(self, t, dt, state, state_desired):
        """
        :param t: time since simulation start
        :param dt: time since last call to measurement_callback
        :param state: State - current quadrotor position and velocity computed from noisy measurements
        :param state_desired: State - desired quadrotor position and velocity
        :return - xyz velocity control signal represented as 3x1 numpy array
        """
        err_p = state_desired-state
        err_d = err_p - self.err_prev

        self.err_prev = err_p

        u = np.array([[self.Kp[i]*err_p[i]+self.Kd[i]*err_d[i]*dt] for i in range(3) ])
        return u


class Pose2D:
    def __init__(self, rotation, translation):
        self.rotation = rotation
        self.translation = translation

    def inv(self):
        """
        inversion of this Pose2D object

        :return - inverse of self
        """
        inv_rotation = self.rotation.transpose()
        inv_translation = -np.dot(inv_rotation, self.translation)

        return Pose2D(inv_rotation, inv_translation)

    def yaw(self):
        from math import atan2
        return atan2(self.rotation[1,0], self.rotation[0,0])

    def __mul__(self, other):
        """
        multiplication of two Pose2D objects, e.g.:
            a = Pose2D(...) # = self
            b = Pose2D(...) # = other
            c = a * b       # = return value

        :param other - Pose2D right hand side
        :return - product of self and other
        """
        return Pose2D(np.dot(self.rotation, other.rotation), np.dot(self.rotation, other.translation) + self.translation)


#EKF Helper methods
#@staticmethod
def rotation(yaw):
    """
    create 2D rotation matrix from given angle
    """
    s_yaw = math.sin(yaw)
    c_yaw = math.cos(yaw)

    return np.array([
        [c_yaw, -s_yaw],
        [s_yaw,  c_yaw]
    ])

#@staticmethod
def normalizeYaw(y):
    """
    normalizes the given angle to the interval [-pi, +pi]
    """
    while(y > math.pi):
        y -= 2 * math.pi
    while(y < -math.pi):
        y += 2 * math.pi
    return y

#@staticmethod
def predictState(dt, x, u_linear_velocity, u_yaw_velocity):
    """
    predicts the next state using the current state and
    the control inputs local linear velocity and yaw velocity
    """
    x_p = np.zeros((3, 1))
    x_p[0:2] = x[0:2] + dt * np.dot(rotation(x[2]), u_linear_velocity)
    x_p[2]   = x[2]   + dt * u_yaw_velocity
    x_p[2]   = normalizeYaw(x_p[2])

    return x_p

#@staticmethod
def calculatePredictStateJacobian(dt, x, u_linear_velocity, u_yaw_velocity):
    """
    calculates the 3x3 Jacobian matrix for the predictState(...) function
    """
    s_yaw = math.sin(x[2])
    c_yaw = math.cos(x[2])

    dRotation_dYaw = np.array([
        [-s_yaw, -c_yaw],
        [ c_yaw, -s_yaw]
    ])
    F = np.identity(3)
    F[0:2, 2] = dt * np.dot(dRotation_dYaw, u_linear_velocity)[0:2,0]

    return F

#@staticmethod
def predictCovariance(sigma, F, Q):
    """
    predicts the next state covariance given the current covariance,
    the Jacobian of the predictState(...) function F and the process noise Q
    """
    return np.dot(F, np.dot(sigma, F.T)) + Q

#@staticmethod
def calculateKalmanGain(sigma_p, H, R):
    """
    calculates the Kalman gain
    """
    return np.dot(np.dot(sigma_p, H.T), np.linalg.inv(np.dot(H, np.dot(sigma_p, H.T)) + R))

#@staticmethod
def correctState(K, x_predicted, z, z_predicted):
    """
    corrects the current state prediction using Kalman gain, the measurement and the predicted measurement

    :param K - Kalman gain
    :param x_predicted - predicted state 3x1 vector
    :param z - measurement 3x1 vector
    :param z_predicted - predicted measurement 3x1 vector
    :return corrected state as 3x1 vector
    """


    x_predicted += np.dot(K,(z-z_predicted))
    return x_predicted

#@staticmethod
def correctCovariance(sigma_p, K, H):
    """
    corrects the sate covariance matrix using Kalman gain and the Jacobian matrix of the predictMeasurement(...) function
    """
    return np.dot(np.identity(3) - np.dot(K, H), sigma_p)

#@staticmethod
def predictMeasurement(x, marker_position_world, marker_yaw_world):
    """
    predicts a marker measurement given the current state and the marker position and orientation in world coordinates
    """
    z_predicted = Pose2D(rotation(x[2]), x[0:2]).inv() * Pose2D(rotation(marker_yaw_world), marker_position_world);

    return np.array([[z_predicted.translation[0], z_predicted.translation[1], z_predicted.yaw()]]).T

#@staticmethod
def calculatePredictMeasurementJacobian( x, marker_position_world, marker_yaw_world):
    """
    calculates the 3x3 Jacobian matrix of the predictMeasurement(...) function using the current state and
    the marker position and orientation in world coordinates

    :param x - current state 3x1 vector
    :param marker_position_world - x and y position of the marker in world coordinates 2x1 vector
    :param marker_yaw_world - orientation of the marker in world coordinates
    :return - 3x3 Jacobian matrix of the predictMeasurement(...) function
    """

    # TODO: implement computation of H
    x_t = x[0]
    y_t = x[1]
    psi = x[2]
    x_m = marker_position_world[0]
    y_m = marker_position_world[1]

    dx = x_t-x_m
    dy = y_t-y_m

    H = np.array([[-math.cos(psi),-math.sin(psi),math.sin(psi)*dx-math.cos(psi)*dy],
                  [math.sin(psi),-math.cos(psi),math.cos(psi)*dx+math.sin(psi)*dy],
                  [0,0,-1]])
    return H



def dist(a,b):
    d = a-b
    return math.sqrt(d[0, 0]**2+d[1, 0]**2)


class EKF:
    def __init__(self):
        #Init EKF
        pos_noise_std = 0.005
        yaw_noise_std = 0.005
        self.Q = np.array([
            [pos_noise_std*pos_noise_std,0,0],
            [0,pos_noise_std*pos_noise_std,0],
            [0,0,yaw_noise_std*yaw_noise_std]
        ])

        #measurement noise
        z_pos_noise_std = 0.005
        z_yaw_noise_std = 0.03
        self.R = np.array([
            [z_pos_noise_std*z_pos_noise_std,0,0],
            [0,z_pos_noise_std*z_pos_noise_std,0],
            [0,0,z_yaw_noise_std*z_yaw_noise_std]
        ])

        # state vector [x, y, yaw] in world coordinates
        self.x = np.zeros((3,1))

        # 3x3 state covariance matrix
        self.sigma = 0.01 * np.identity(3)

class UserCode:
    def __init__(self):
        self.ekf = EKF()
        self.pid = PID()

        self.next_marker = 0;
    def get_markers(self):
        """
        place up to 30 markers in the world
        """
        
        markers = [
        [2,0],
        [4,0],
        [5,0],
        [4,2],
        [2,4],
        [4,3],
        [5,3],
        [4,6],
        [7,5],
        [8,5],

        [4,6],
        
        [5,7],
        
        [4,9],
        [6,8],
        [8,8],

        [10,9],
        [11,11],
        [9,11],
        [6,11],
        [11,13],
        
        [10,13]]
        return markers

    def state_callback(self, t, dt, linear_velocity, yaw_velocity):
        """
        called when a new odometry measurement arrives approx. 200Hz

        :param t - simulation time
        :param dt - time difference this last invocation
        :param linear_velocity - x and y velocity in local quadrotor coordinate frame (independent of roll and pitch)
        :param yaw_velocity - velocity around quadrotor z axis (independent of roll and pitch)

        :return tuple containing linear x and y velocity control commands in local quadrotor coordinate frame (independet of roll and pitch), and yaw velocity
        """

        #EKF
        ekf = self.ekf
        ekf.x = predictState(dt, ekf.x, linear_velocity, yaw_velocity)

        F = calculatePredictStateJacobian(dt, ekf.x, linear_velocity, yaw_velocity)
        ekf.sigma = predictCovariance(ekf.sigma, F, ekf.Q)

        pred_x =ekf.x
        markers = self.get_markers()
        next_idx = self.next_marker % len(markers)
        tgt_x = np.array([markers[next_idx]+[0]]).T
        
        #TODO: calculate errors and feed to PID
        u = self.pid.compute_control_command(t, dt, pred_x, tgt_x)
        u_lv = u[0:2]
        u_yaw = u[2]
        return (u_lv,u_yaw)

    def measurement_callback(self,
                             marker_position_world, marker_yaw_world,
                             marker_position_relative, marker_yaw_relative):
        """
        called when a new marker measurement arrives max 30Hz, marker measurements are only available if the quadrotor is
        sufficiently close to a marker

        :param marker_position_world - x and y position of the marker in world coordinates 2x1 vector
        :param marker_yaw_world - orientation of the marker in world coordinates
        :param marker_position_relative - x and y position of the marker relative to the quadrotor 2x1 vector
        :param marker_yaw_relative - orientation of the marker relative to the quadrotor
        """
#EKF
        ekf = self.ekf
        z = np.array([[marker_position_relative[0], marker_position_relative[1], marker_yaw_relative]]).T
        z_predicted = predictMeasurement(ekf.x, marker_position_world, marker_yaw_world)

        H = calculatePredictMeasurementJacobian(ekf.x, marker_position_world, marker_yaw_world)
        K = calculateKalmanGain(ekf.sigma, H, ekf.R)

        ekf.x = correctState(K, ekf.x, z, z_predicted)
        ekf.sigma = correctCovariance(ekf.sigma, K, H)

        markers = self.get_markers()
        next_idx = self.next_marker % len(markers)
        tgt_marker = np.array([markers[next_idx]+[0]]).T
        
        if dist(tgt_marker[0:2],marker_position_world) <0.01:
            self.next_marker += 1

