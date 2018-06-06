import numpy as np
import math
import logging
import geometry as geom

class KFilter:
    Observation_CoeffVal = 15
    num_variables = 4
    forget=0.001
    #QcalibIndex=0
    calibrating=False
    maxPredictions=50    #if this amount of consecutive signal is missing, it sends out None
    predictionCounter=0
    confidenceInterval=50 #we assume that there can't be more than this pixels difference between the measurements of two consecutive frame if the difference is bigger than this number, it sends out a None

    def __init__(self, max_x, max_y, filter_dim, R, Q, initpoint=None, fps=190):
        # for the filter
        #self.measured_state = np.zeros(shape=(self.num_variables, 1))
        self.measured_state = np.zeros(shape=(2, 1))
        self.num_variables=filter_dim
        # self.predicted_state = []
        # a FIFO
        self.updated_state = np.zeros(shape=(self.num_variables, 100))
        self.RCalib=np.zeros(shape=(2, 100))
        self.QCalib=[]

        #self.measurement_hist = []  # should it save the entire trajectory?
        self.updated_hist=[]
        self.max_x=max_x
        self.max_y=max_y
        self.initFilter(R, Q)
        self.log=self.log = logging.getLogger(__name__)
        self.missingPoint=False
        self.defaultT=1.0/fps

    #initialize Fk, Hk, Pk, Rk, Qk and Kgain
    def initFilter(self, R, Q):
        # Hk:observation matrix
        self.Hk = np.eye(2, self.num_variables)  # not going to change
        # Pk: transition covariance
        self.Pk = np.zeros(shape=(self.num_variables, self.num_variables))  # np.eye(num_variables, num_variables)
        # Rk: observation covariance
        # self.measurement_covariance = np.eye(4, 4)
        if R is None:
            self.Rk = np.eye(2, 2) * 0.5 # estimate of measurement variance, change to see effect
        else:
            self.Rk=R
        # Q
        if Q is None:
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
        else:
            self.Qk=Q

        self.Kgain = np.eye(self.num_variables, 2)

    def start_filter(self, initpoint=None):
        self.log.debug("kalman filter enabled")
        #initializing the matrices
        #self.initFilter()
        # for the filter
        self.measured_state = np.zeros(shape=(2, 1))
        # self.predicted_state = []
        # a FIFO
        self.updated_state = np.zeros(shape=(self.num_variables, 100))
        self.predictionCounter=0

        #initializing the coordinates as a column matrix
        if initpoint is not None:
            initial_state = np.array([[initpoint[0]], [initpoint[1]], [0.0001], [0.0001], [0.0001], [0.0001]])
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
            self.calibrating=True
            #self.QcalibIndex=index
            #self.iterate_filter(t,(x,y), False, False, True)
            #print index
        else:
            self.calibrating=False
            self.Qk = np.mean(self.QCalib, axis=0)
            self.log.debug("observation calibration done")
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
             #   print index
                self.RCalib[:, index] = [x, y]#, vx, vy, ax, ay]
        else:
            self.Rk = np.cov(self.RCalib[:, 0:])
            self.log.debug("sensor calibration done")

    def iterate_filter(self, dt, coordinates,guessing_enabled=True, adaptive=False):#, calibrating=False):

        prevMissingPoint=self.missingPoint  #saves the previous missing point
        u = np.asmatrix(self.updated_state[:, -1]).transpose()

       # print dt, coordinates
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
            m=self.add_measurement(dt, coordinates)
            #if the measured point is an outlier and the previous measurement is not missing
            if geom.distance(m, pred[0:2]) > self.confidenceInterval and not self.missingPoint:
                #print self.Fk
                #print "coordinates:%s u: %s, pred:%s dt:", coordinates, u[0:2], pred[0:2], dt
                #print "outliers!!!!!!!!!!!!!"
                self.missingPoint = True
            else:
                #print self.Fk
                #print "coordinates:%s u: %s, pred:%s dt:", coordinates, u[0:2], pred[0:2], dt
                self.predictionCounter =0   #resets the predictionCounter
                self.missingPoint = False

        else:
            self.missingPoint=True
        if self.missingPoint:
            if not self.calibrating:
                #if position guessing is enabled and there were no 10 consecutive predictions
                if guessing_enabled and self.predictionCounter<self.maxPredictions:
                    #update the list with the prediction
                    self.updated_state[:, :-1] = self.updated_state[:, 1:]
                    self.updated_state[:, -1] = pred.A1
                    self.predictionCounter=self.predictionCounter+1

                    xpred=int(round(pred[0,0])) if round(pred[0,0])>0 and round(pred[0,0])<self.max_x else None
                    ypred=int(round(pred[1,0])) if round(pred[1,0])>0 and round(pred[1,0])<self.max_y else None

                    if xpred is not None and ypred is not None:
                        self.log.debug("predicting missing value")
                       # print 'Missing value nr. ', self.predictionCounter, '. Predicted: ', (pred[0,0],  pred[1,0]), 'updated: ', (xpred, ypred)
                        return (xpred, ypred)
                    else:
                        return None
                else:
                    return None
            else:
                return None

        # before update
        diff = m - self.Hk * pred

        #print self.calibrating
        if self.calibrating:
            self.QCalib.append(self.Kgain*diff*diff.T*self.Kgain.T)
        # update
        updateval = pred + self.Kgain * diff

        # #adapting Rk and Qk
        if adaptive:
            self.log.debug("adaptive filtering...")
            self.Qk = self.forget * self.Qk +\
                      (1 - self.forget) * self.Kgain * diff * diff.transpose() * self.Kgain.transpose()
            residual = m - (self.Hk * updateval)
            self.Rk = self.forget * self.Rk + (1 - self.forget) * (residual * residual.T + (self.Hk * self.Pk * self.Hk.T))

        self.updated_state[:, :-1] = self.updated_state[:, 1:]
        self.updated_state[:, -1] = updateval.A1

        xval = int(round(updateval[0,0])) if round(updateval[0,0]) > 0 and round(updateval[0,0]) < self.max_x else None
        yval = int(round(updateval[1,0])) if round(updateval[1,0]) > 0 and round(updateval[1,0]) < self.max_y else None

        if xval is not None and yval is not None:
           # print 'Measured: ', (m[0,0], m[1,0]), 'Predicted: ', (pred[0,0],  pred[1,0]), 'updated: ', (xval, yval)
            return (xval, yval)
        else:
            return None

    def stop_filter(self):
        self.log.debug("filter stopped")
        self.filter=None
        self.updated_state=None

    #def updateObservationCoeffVal(self, value):
        # print "updated to: ", value
     #   self.Rk = np.eye(4, 4) * value
     #   self.filter.observation_covariance = self.Rk

   # def resetFilter(self):
   #     self.measurement_hist=[]
