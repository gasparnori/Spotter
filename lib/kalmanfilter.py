import numpy as np
import math

class KFilter:
    Observation_CoeffVal = 15
    num_variables = 6
    forget=0.3
    maxPredicitons=7    #if 10 consecutive signal is missing, it sends out None
    predictionCounter=0

    def __init__(self, max_x, max_y, initpoint=None):
        # for the filter
        #self.measured_state = np.zeros(shape=(self.num_variables, 1))
        self.measured_state = np.zeros(shape=(2, 1))
        # self.predicted_state = []
        # a FIFO
        self.updated_state = np.zeros(shape=(self.num_variables, 100))
        self.RCalib=np.zeros(shape=(2, 100))
        self.QCalib=[]

        self.measurement_hist = []  # should it save the entire trajectory?
        self.max_x=max_x
        self.max_y=max_y

    #initialize Fk, Hk, Pk, Rk, Qk and Kgain
    def initFilter(self):
        # Hk:observation matrix
        self.Hk = np.eye(2, self.num_variables)  # not going to change
        # Pk: transition covariance
        self.Pk = np.zeros(shape=(self.num_variables, self.num_variables))  # np.eye(num_variables, num_variables)
        # Rk: observation covariance
        # self.measurement_covariance = np.eye(4, 4)
        self.Rk = np.eye(2, 2) * 20  # estimate of measurement variance, change to see effect
        # Q
        if self.num_variables == 4:
            self.Qk = np.matrix([[0.3, 0, 0, 0],
                                 [0, 0.3, 0, 0],
                                 [0, 0, 0.001, 0],
                                 [0, 0, 0, 0.001]])
        if self.num_variables == 6:
            self.Qk = np.matrix([[0.3, 0, 0, 0, 0, 0],
                                 [0, 0.3, 0, 0, 0, 0],
                                 [0, 0, 0.001, 0, 0, 0],
                                 [0, 0, 0, 0.001, 0, 0],
                                 [0, 0, 0, 0, 0.001, 0],
                                 [0, 0, 0, 0, 0, 0.001]])

        self.Kgain = np.eye(self.num_variables, 2)

    def start_filter(self, initpoint=None):
       # print "start"
        #initializing the matrices
        self.initFilter()
        # for the filter
        self.measured_state = np.zeros(shape=(2, 1))
        # self.predicted_state = []
        # a FIFO
        self.updated_state = np.zeros(shape=(self.num_variables, 100))

        #initializing the coordinates as a column matrix
        if initpoint is not None:
            initial_state = np.array([[initpoint[0]], [initpoint[1]], [0.001], [0.001], [0.001], [0.001]])
            self.measured_state[:, 0] = initial_state[0:2, 0]
            self.updated_state[:, -1] = initial_state[:, 0]

    def add_measurement(self, dt, coordinates):

        datax=coordinates[0]
        datay=coordinates[1]

        # if dt > 0:
        #     vx = (datax - self.measured_state[0, 0]) / dt
        #     vy = (datay - self.measured_state[1, 0]) / dt
        #     ax = (vx - self.measured_state[2, 0]) / dt
        #     ay = (vy - self.measured_state[3, 0]) / dt
        # else:
        #     vx = (self.measured_state[2, 0])
        #     vy = (self.measured_state[3, 0])
        #     ax = (self.measured_state[4, 0])
        #     ay = (self.measured_state[5, 0])
        self.measured_state = np.array([[datax], [datay]])#, [vx], [vy], [ax], [ay]])
        return np.asmatrix(self.measured_state)
    def calibrateQ(self, x,y,t,index, max_index):
        if index<max_index:
            self.iterate_filter(t,(x,y), False, False, True)
            print index
        else:
            self.Qk = np.mean(self.QCalib, axis=0)
            print self.Qk
        print "calibrating Measurement"
    def calibrateSensor(self, x, y, t, index, max_index):
        # measurements in a fixed position: should determine the sensor error
        if index<max_index:
            # if index > 0:
            #     vx = (x - self.RCalib[0, index - 1]) / t  # px/usec
            #     vy = (y - self.RCalib[1, index - 1]) / t  # px/usec
            # else:
            #     #if it's the first element, the vector is initialized
            #     self.RCalib=np.zeros(shape=(self.num_variables, max_index))  # saves 100 points in the same location
            #     vx = 0
            #     vy = 0
            #
            # if self.num_variables == 4:
            #     self.RCalib[:, index] = [x, y, vx, vy]
            #
            # if self.num_variables == 6:
            #     if index > 1:
            #         ax = (vx - self.RCalib[2, index - 1]) / t  # px/usec^2
            #         ay = (vy - self.RCalib[3, index - 1]) / t  # px/usec^2
            #     else:
            #         ax = 0
            #         ay = 0
                print index
                self.RCalib[:, index] = [x, y]#, vx, vy, ax, ay]
        else:
            self.Rk = np.cov(self.RCalib[:, 0:])
            print "calibration finished", self.Rk

    def iterate_filter(self, dt, coordinates,guessing_enabled=True, adaptive=False, calibrating=False):
        u = np.asmatrix(self.updated_state[:, -1]).transpose()

        if self.num_variables == 4:
            self.Fk = np.array([[1, 0, dt, 0], [0, 1, 0, dt], [0, 0, 1, 0], [0, 0, 0, 1]])
        else:
            self.Fk = np.array([[1, 0, dt, 0, 0.5 * dt * dt, 0],
                                [0, 1, 0, dt, 0, 0.5 * dt * dt],
                                [0, 0, 1, 0, dt, 0],
                                [0, 0, 0, 1, 0, dt],
                                [0, 0, 0, 0, 1, 0],
                                [0, 0, 0, 0, 0, 1]])
        # #prediction step
        pred = self.Fk * u
        cov = self.Fk * self.Pk * self.Fk.transpose() + self.Qk
        #setting the matrices
        S=self.Hk * cov * self.Hk.T + self.Rk

        self.Kgain = cov * self.Hk.T * np.linalg.inv(S)
        self.Pk = cov - (self.Kgain *S*self.Kgain.T)

        if coordinates is not None:
            missingPoint = False
            m=self.add_measurement(dt, coordinates)
            self.predictionCounter =0   #resets the predictionCounter
        else:
            if not calibrating:
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
            else:
                return None

        # before update
        diff = m - self.Hk * pred
        if calibrating:
            self.QCalib.append(self.Kgain*diff*diff.T*self.Kgain.T)
        # update
        updateval = pred + self.Kgain * diff

        # #adapting Rk and Qk
        if adaptive:
            self.Qk = self.forget * self.Qk +\
                      (1 - self.forget) * self.Kgain * diff * diff.transpose() * self.Kgain.transpose()
            residual = m - (self.Hk * updateval)
            self.Rk = self.forget * self.Rk + (1 - self.forget) * (residual * residual.T + (self.Hk * self.Pk * self.Hk.T))

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