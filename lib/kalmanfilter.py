import numpy as np
import math


class KFilter:
    Observation_CoeffVal = 5
    num_variables = 6
    forget=0.3
    maxPredicitons=10    #if 10 consecutive signal is missing, it sends out None
    predictionCounter=0

    def __init__(self, max_x, max_y, initpoint=None):
        # for the filter
        self.measured_state = np.zeros(shape=(self.num_variables, 1))
        # self.predicted_state = []
        # a FIFO
        self.updated_state = np.zeros(shape=(self.num_variables, 100))

        self.measurement_hist = []  # should it save the entire trajectory?
        self.max_x=max_x
        self.max_y=max_y

    def start_filter(self, initpoint=None):

        print "start"
        deltaT = 0.5
        # Fk: transition matrix for only position and velocity
        # self.Fk =np.array( [[1, 0, deltaT, 0],[0, 1, 0, deltaT], [0, 0, 1, 0], [0, 0, 0, 1]])

        # Fk: transition matrix for acceleration, velocity and position
        self.Fk = np.matrix(((1, 0, deltaT, 0, 0.5 * deltaT * deltaT, 0),
                             (0, 1, 0, deltaT, 0, 0.5 * deltaT * deltaT),
                             (0, 0, 1, 0, deltaT, 0),
                             (0, 0, 0, 1, 0, deltaT),
                             (0, 0, 0, 0, 1, 0),
                             (0, 0, 0, 0, 0, 1)))

        # Hk:observation matrix
        self.Hk = np.eye(self.num_variables, self.num_variables)  # not going to change
        # Pk: transition covariance
        self.Pk = np.zeros(shape=(self.num_variables, self.num_variables))  # np.eye(num_variables, num_variables)
        # Rk: observation covariance
        # self.measurement_covariance = np.eye(4, 4)
        self.Rk = np.eye(self.num_variables, self.num_variables) * 15  # estimate of measurement variance, change to see effect
        # Q
        self.Qk = np.matrix([[0.5, 0, 0, 0, 0, 0],
                             [0, 0.5, 0, 0, 0, 0],
                             [0, 0, 0.0001, 0, 0, 0],
                             [0, 0, 0, 0.0001, 0, 0],
                             [0, 0, 0, 0, 0.0001, 0],
                             [0, 0, 0, 0, 0, 0.0001]])
        self.Kgain = np.eye(self.num_variables, self.num_variables)
        # for the filter
        self.measured_state = np.zeros(shape=(self.num_variables, 1))
        # self.predicted_state = []
        # a FIFO
        self.updated_state = np.zeros(shape=(self.num_variables, 100))

        #initializing the coordinates as a column matrix
        if initpoint is not None:
            initial_state = np.array([[initpoint[0]], [initpoint[1]], [0], [0], [0], [0]])
            self.measured_state[:, 0] = initial_state[:, 0]
            self.updated_state[:, -1] = initial_state[:, 0]

    def add_measurement(self, dt, coordinates):

        datax=coordinates[0]
        datay=coordinates[1]

        if dt > 0:
            vx = (datax - self.measured_state[0, 0]) / dt
            vy = (datay - self.measured_state[1, 0]) / dt
            ax = (vx - self.measured_state[2, 0]) / dt
            ay = (vy - self.measured_state[3, 0]) / dt
        else:
            vx = (self.measured_state[2, 0])
            vy = (self.measured_state[3, 0])
            ax = (self.measured_state[4, 0])
            ay = (self.measured_state[5, 0])
        self.measured_state = np.array([[datax], [datay], [vx], [vy], [ax], [ay]])
        return np.asmatrix(self.measured_state)

    def iterate_filter(self, dt, coordinates,guessing_enabled=True, adaptive=False):
        u = np.asmatrix(self.updated_state[:, -1]).transpose()

        HkT = self.Hk.transpose()
        I = np.eye(self.num_variables, self.num_variables)

        self.Fk = np.array([[1, 0, dt, 0, 0.5 * dt * dt, 0],
                            [0, 1, 0, dt, 0, 0.5 * dt * dt],
                            [0, 0, 1, 0, dt, 0],
                            [0, 0, 0, 1, 0, dt],
                            [0, 0, 0, 0, 1, 0],
                            [0, 0, 0, 0, 0, 1]])
        # #prediction step
        pred = self.Fk * u

        cov = self.Fk * self.Pk * self.Fk.transpose() + self.Qk

        if coordinates is not None:
            missingPoint = False
            m=self.add_measurement(dt, coordinates)
            self.predictionCounter =0   #resets the predictionCounter
        else:
            missingPoint=True
            #if position guessing is enabled and there were no 10 consecutive predictions
            if guessing_enabled and self.predictionCounter<self.maxPredicitons:
                #update the list with the prediction
                self.updated_state[:, :-1] = self.updated_state[:, 1:]
                self.updated_state[:, -1] = pred.A1
                self.predictionCounter=self.predictionCounter+1

                xpred=int(round(pred[0,0])) if round(pred[0,0])>0 and round(pred[0,0])<self.max_x else None
                ypred=int(round(pred[1,0])) if round(pred[1,0])>0 and round(pred[1,0])<self.max_y else None
                if xpred is not None and ypred is not None:
                    return (xpred, ypred)
                else:
                    return None
            else:
                return None


        # before update
        diff = m - self.Hk * pred
        print pred, cov
        #print cov
        self.Kgain = cov * HkT * np.linalg.inv(self.Hk * cov * HkT + self.Rk)
        # #adapting Rk and Qk
        if adaptive:
            self.Qk = self.forget * self.Qk +\
                      (1 - self.forget) * self.Kgain * diff * diff.transpose() * self.Kgain.transpose()

        # update
        updateval = pred + self.Kgain * diff
        self.Pk = (I - (self.Kgain * self.Hk)) * cov
        #print updateval

        if adaptive:
            residual = m - (self.Hk * updateval)
            self.Rk = self.forget * self.Rk + (1 - self.forget) * (residual * residual.T + (self.Hk * self.Pk * HkT))
        #print updateval

        self.updated_state[:, :-1] = self.updated_state[:, 1:]
        self.updated_state[:, -1] = updateval.A1
        xval = int(round(updateval[0,0])) if round(updateval[0,0]) > 0 and round(updateval[0,0]) < self.max_x else None
        yval = int(round(updateval[1,0])) if round(updateval[1,0]) > 0 and round(updateval[1,0]) < self.max_y else None
        if xval is not None and yval is not None:
            return (xval, yval)
        else:
            return None


    def stop_filter(self):
        print "stop"
        self.filter=None
        self.updated_state=None

    def updateObservationCoeffVal(self, value):
        # print "updated to: ", value
        self.Rk = np.eye(4, 4) * value
        self.filter.observation_covariance = self.Rk