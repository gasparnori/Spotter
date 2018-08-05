import numpy as np
import math
import logging
import lib.geometry as geom

class KFilter:
    forget=0.3
    calibrating=False
    maxPredictions=1000   #if this amount of consecutive signal is missing, it sends out None
    predictionCounter=0

    #confidenceInterval=20 #we assume that there can't be more than this pixels difference between the measurements of two consecutive frame if the difference is bigger than this number, it sends out a None
    #confIntcoeff = 50
    def __init__(self, max_x, max_y, filter_dim, R, Q, initpoint=None, fps=190):

        self.max_x=max_x
        self.max_y=max_y
        self.num_variables=filter_dim
        self.log=self.log = logging.getLogger(__name__)

        self.RCalib=np.zeros(shape=(4, 100))
        self.QCalib=[]
        self.initFilter(R, Q)


    #initialize Fk, Hk, Pk, Rk, Qk and Kgain
    def initFilter(self, R, Q):
        self.updated_state = np.zeros(shape=(self.num_variables, 1))
        self.estimation_state = self.updated_state.copy()
        # Pk: transition covariance
        self.Pk = np.zeros(shape=(self.num_variables, self.num_variables))  # np.eye(num_variables, num_variables)
        self.estimationP = self.Pk.copy()
        # Rk: observation covariance
        # self.measurement_covariance = np.eye(4, 4)

        #if R is None: -----------------------------------------------------------------------
        self.Rk = np.eye(4, 4) * 10 # estimate of measurement variance, change to see effect
        #else:
        #    self.Rk=R
        # Q
        if Q is None:
            if self.num_variables == 4:
                self.Qk = np.matrix([[5, 0, 0, 0],
                                     [0, 5, 0, 0],
                                     [0, 0, 0.001, 0],
                                     [0, 0, 0, 0.001]])
            if self.num_variables == 6:
                self.Qk = np.matrix([[5, 0, 0, 0, 0, 0],
                                     [0, 5, 0, 0, 0, 0],
                                     [0, 0, 0.001, 0, 0, 0],
                                     [0, 0, 0, 0.001, 0, 0],
                                     [0, 0, 0, 0, 0.001, 0],
                                     [0, 0, 0, 0, 0, 0.001]])
        else:
            self.Qk=Q

        #self.Kgain = np.eye(self.num_variables, 2)
        #first step is estimation mode
        #if the measurement is missing, it creates an estimation branch
        self.estimationMode = True

    def start_filter(self, initpoint=None):
        #print "start filter"
        self.log.debug("kalman filter enabled")
        self.predictionCounter=0
        self.initFilter(self.Rk, self.Qk)
        #initializing the coordinates as a column matrix
        if initpoint is not None:
            initial_state = np.array([[initpoint[0]], [initpoint[1]], [0.005], [0.005], [-0.0001], [-0.0001]])
            self.updated_state[:, -1] = initial_state[:, 0]
            self.estimation_state[:, -1] = initial_state[:, 0]

    def calibrateQ(self, index, max_index):
        if index<max_index:
            self.calibrating=True
        else:
            self.calibrating=False
            self.Qk = np.mean(self.QCalib, axis=0)
            self.log.debug("observation calibration done")

    def calibrateSensor(self, x, y, index, max_index):
        # measurements in a fixed position: should determine the sensor error
        if index<max_index:
                self.RCalib[:, index] = [x, y]
        else:
            self.Rk = np.cov(self.RCalib[:, 0:])
            self.log.debug("sensor calibration done")

    # def expWeight(self, x):
    #     if abs(x) < self.confidenceInterval:
    #         y = 1
    #     else:
    #         y = 0.5 * np.exp(1 - (abs(x) / self.confIntcoeff))
    #     return (y)
    def addMeasurement(self, coordinates, dt):
        try:
            vx=(coordinates[0]-self.updated_state[0, 0])/dt
            vy=(coordinates[1]-self.updated_state[1, 0])/dt
            return np.asmatrix([[coordinates[0]], [coordinates[1]], [vx], [vy]])
        except Exception, e:
            print e
            return None

    def checkWithinFrame(self, x, y):
        xval = int(round(x)) if round(x) > 0 and round(x) < self.max_x else None
        yval = int(y) if round(y) > 0 and round(y) < self.max_y else None
        return (xval, yval) if (xval is not None and yval is not None) else None

    def iterateTracks(self, dt, coordinates, guessing_enabled=True, adaptive=False):
        try:
            # print "estimation mode before: ", self.estimationMode, "u before: ", self.updated_state[0:2, -1]
            # print "Qk:", self.Qk
            # print "Rk:", self.Rk
           # Hk:observation matrix
            Hk = np.eye(4, self.num_variables)  # not going to change
            retVal = None  # default return value
            #dt=17
            if self.num_variables == 4:
                Fk = np.array([[1, 0, dt, 0], [0, 1, 0, dt], [0, 0, 1, 0], [0, 0, 0, 1]])         # system dynamics (4x4 or 6x6)
            else:
                Fk = np.array([[1, 0, dt, 0, 0.5 * dt * dt, 0],
                                    [0, 1, 0, dt, 0, 0.5 * dt * dt],
                                    [0, 0, 1, 0, dt, 0],
                                    [0, 0, 0, 1, 0, dt],
                                    [0, 0, 0, 0, 1, 0],
                                    [0, 0, 0, 0, 0, 1]])

            missingPoint=True if coordinates is None else False
            # if the previous measurement was an estimation
            u= np.asmatrix(self.updated_state[:, -1].copy()).transpose()
            e= np.asmatrix(self.estimation_state[:, -1].copy()).transpose()
            m= self.addMeasurement(coordinates, dt) if coordinates is not None else None
            #m= np.asmatrix([[coordinates[0]], [coordinates[1]]]) if coordinates is not None else None
            # print "----------------------------------------------------------------------------------------------------"
            # print "estimation Mode:", self.estimationMode
            # print "e assigned: ", (e[0,0],e[1,0])
            # print "u assigned: ", (u[0,0],u[1,0])
            # print "m assigned: ", m

            if self.estimationMode:
                #if this one is an estimation too
                if coordinates is None:
                    # predicting from the last estimated
                    pred = Fk * e
                    cov = Fk * self.estimationP * Fk.transpose() + self.Qk
                else:
                   # print "returning from estimation mode to stable"
                    self.estimationMode=False
                    pred = Fk * u  # state matrix (4x1) or (6x1)
                    cov = Fk * self.Pk * Fk.transpose() + self.Qk  # A priori covariance matrix
            else:
                #print "staying in stable mode"
                pred = Fk * u  # state matrix (4x1) or (6x1)
                cov = Fk * self.Pk * Fk.transpose() + self.Qk  # A priori covariance matrix
                if not missingPoint and (geom.distance(coordinates, pred[0:2]) > 30):
                   print "outlier"
                   # missingPoint = True

            if missingPoint:
              #  print "missing point"
                last_stable= u[0:2,-1]
                if guessing_enabled and self.predictionCounter < self.maxPredictions:
                        self.estimationMode=True
                        diff=np.zeros(shape=(4,1))
                        self.predictionCounter=self.predictionCounter+1
                else:
                    print "return without update"
                    return None, None, last_stable
            else:
                #print "not missing"
                self.estimationMode = False #this refers to the next circle
                self.predictionCounter = 0
                diff = (m - Hk * pred)  # difference between prediction and measurement * mWeight

            #steps of both tracks
            # setting the matrices
            S = np.linalg.inv(Hk * cov * Hk.T + self.Rk)
            Kgain = cov * Hk.T * S  # *mWeight # Kalman gain
            # update
            updateval = pred + Kgain * diff

            #if the values are stable
            if not self.estimationMode:
                #print "stable measurement"
                self.updated_state[:, -1] = updateval.A1.copy()
                # A posteriori covariance matrix
                self.Pk = (np.eye(self.num_variables) - (Kgain * Hk)) * cov
                # estimation_state is updated in every iteration, while the updated one is not

                if adaptive:
                    self.log.debug("adaptive filtering...")
                    self.Qk = self.forget * self.Qk + (1 - self.forget) * Kgain * diff * diff.T * Kgain.T
                    res = m - (Hk * updateval)
                    self.Rk = self.forget * self.Rk + (1 - self.forget) * (res * res.T + (Hk * self.Pk * Hk.T))

            self.estimation_state[:, -1] = updateval.A1.copy()
            self.estimationP = self.Pk.copy()
            #if updated state wasn't changed, this shouldn't change either
            last_stable = self.updated_state[0:2, -1].copy()
            retVal = self.checkWithinFrame(updateval[0, 0], updateval[1, 0])

            # print self.calibrating
            if self.calibrating and not missingPoint:
                self.QCalib.append(Kgain * diff * diff.T * Kgain.T)

            print "estimationMode:", self.estimationMode,\
                "missing Point: ", missingPoint, \
                "u: ", (u[0,0],u[1,0]), "pred: ", (pred[0,0],pred[1,0]),\
                "updateval: ", (updateval[0,0], updateval[1][0]),\
                "coordinates: ", coordinates,\
                "last stable: ", (last_stable[0], last_stable[1])
            return self.estimationMode, retVal, last_stable
        except Exception,e:
            print e


    # def iterateRobustFilter(self, dt, coordinates,guessing_enabled=True, adaptive=False):
    #     #u = np.asmatrix(self.updated_state[:, -1]).transpose()         #state matrix (4x1) or (6x1)
    #     retVal = None  # default return value
    #     dt=30
    #     if self.num_variables == 4:
    #         Fk = np.array(
    #             [[1, 0, dt, 0], [0, 1, 0, dt], [0, 0, 1, 0], [0, 0, 0, 1]])  # system dynamics (4x4 or 6x6)
    #     else:
    #         Fk = np.array([[1, 0, dt, 0, 0.5 * dt * dt, 0],
    #                             [0, 1, 0, dt, 0, 0.5 * dt * dt],
    #                             [0, 0, 1, 0, dt, 0],
    #                             [0, 0, 0, 1, 0, dt],
    #                             [0, 0, 0, 0, 1, 0],
    #                             [0, 0, 0, 0, 0, 1]])
    #
    #     if coordinates is not None:
    #         self.estimationMode=False
    #         pred = Fk * np.asmatrix(self.updated_state[:, -1]).transpose()  # state matrix (4x1) or (6x1)
    #         cov = Fk * self.Pk * Fk.transpose() + self.Qk  # A priori covariance matrix
    #         self.predictionCounter=0
    #         m = np.asmatrix([[coordinates[0]], [coordinates[1]]])
    #         if geom.distance(m, pred[0:2])>30:
    #             print "outlier"
    #
    #         diff = (m - Hk * pred)  # difference between prediction and measurement * mWeight
    #
    #         # setting the matrices
    #         S = np.linalg.inv(Hk * cov * Hk.T + self.Rk)
    #         self.Kgain = cov * Hk.T * S# *mWeight # Kalman gain
    #         self.Pk = (np.eye(self.num_variables) - (self.Kgain * Hk)) * cov  # A posteriori covariance matrix
    #
    #         # update
    #         updateval = pred + self.Kgain * diff
    #
    #         # print self.calibrating
    #         if self.calibrating:
    #             self.QCalib.append(self.Kgain * diff * diff.T * self.Kgain.T)
    #
    #         # #adapting Rk and Qk
    #         if adaptive:
    #             #self.log.debug("adaptive filtering...")
    #             self.Qk = self.forget * self.Qk + (1 - self.forget) * self.Kgain * diff * diff.T * self.Kgain.T
    #             res = m - (Hk * updateval)
    #             self.Rk = self.forget * self.Rk + (1 - self.forget) * (res * res.T + (Hk * self.Pk * Hk.T))
    #
    #         #self.updated_state[:, :-1] = self.updated_state[:, 1:]
    #         self.updated_state[:, -1] = updateval.A1
    #         #just copies the values
    #         self.estimation_state=self.updated_state
    #         retVal=self.checkWithinFrame(updateval[0, 0], updateval[1, 0])
    #
    #     else:
    #         if not self.calibrating:
    #
    #             if guessing_enabled and self.predictionCounter<self.maxPredictions:
    #                 self.estimationMode=True
    #                 # #prediction step
    #                 pred = Fk * np.asmatrix(self.estimation_state[:, -1]).transpose()
    #                 cov = Fk * self.estimationP * Fk.transpose() + self.Qk
    #
    #                 #update the list with the prediction
    #                 self.estimation_state[:, :-1] = self.estimation_state[:, 1:]
    #                 self.estimation_state[:, -1] = pred.A1
    #                 self.predictionCounter=self.predictionCounter+1
    #
    #                 retVal=self.checkWithinFrame(pred[0,0], pred[1,0])
    #     return self.estimationMode, retVal

    def stop_filter(self):
        self.log.debug("filter stopped")
        self.filter=None
        self.updated_state=None
        self.estimation_state=None
        self.Pk=None
        self.estimationP=None

class doubleFilter:

    forget=0.3
    #calibrating=False
    maxPredictions=1000   #if this amount of consecutive signal is missing, it sends out None
    predictionCounter=0

    def createF(self, dt):
        F=np.eye(self.num_variables, self.num_variables)
        F[0:7, 7:] =(np.eye(7,7))*dt
        return F

    def firstOrderParams(self, coords1, coords2):
        x1 = coords1[0] if coords1 is not None else None
        y1 = coords1[1] if coords1 is not None else None
        x2 = coords2[0] if coords2 is not None else None
        y2 = coords2[1] if coords2 is not None else None
        middle_point = geom.middle_point([coords1, coords2]) if (coords1 is not None and coords2 is not None) else (None, None)
        if coords1 is not None and coords2 is not None:
            dx = (x2 - x1) * 1.0  # x2-x1
            dy = (y2 - y1) * 1.0  # y2-y1
            theta = int(math.fmod(math.degrees(math.atan2(dx, dy)) + 360, 360))  # math.atan2(x2-x1, y2-y1)
        else:
            theta=None
        return [x1, y1, x2, y2, middle_point[0], middle_point[1], theta]

    def secondOrderParams(self, dt, firstOrderParams):
        m = np.zeros(shape=(self.num_variables, 1))
        mask = np.zeros(shape=(self.num_variables, self.num_variables))
        #x1
        for i in range(0,7):
            if firstOrderParams[i] is not None:
                m[7+i,0]=(firstOrderParams[i]-self.updated_state[i,0])/dt
                m[i, 0] = firstOrderParams[i]
                mask[i,i]=1
                mask[7+i, 7+i] = 1
        return m, mask

    def __init__(self, max_x, max_y, initpoint=None):

        self.max_x=max_x
        self.max_y=max_y
        #x1, y1, x2, y2, combined_x, combined_y, orientation, vx1, vy1, vx, vy, vx2, vy2, angular velocity
        self.num_variables=14
        self.log=self.log = logging.getLogger(__name__)

       # self.RCalib=np.zeros(shape=(4, 100))
        #self.QCalib=[]
        self.initFilter()


        # initialize Fk, Hk, Pk, Rk, Qk and Kgain

    def initFilter(self):#, R, Q):
        self.updated_state = np.zeros(shape=(self.num_variables, 1))
        self.estimation_state = self.updated_state.copy()
        # Pk: transition covariance
        self.Pk = np.zeros(shape=(self.num_variables, self.num_variables))  # np.eye(num_variables, num_variables)
        self.estimationP = self.Pk.copy()
        # Rk: observation covariance
        self.Rk = np.eye(self.num_variables, self.num_variables) * 10  # estimate of measurement variance, change to see effect
        self.Qk = np.eye(self.num_variables, self.num_variables) * 0.001
        self.Qk[0:7, 0:7] = np.eye(7,7) * 5

        # first step is estimation mode
        # if the measurement is missing, it creates an estimation branch
        self.estimationMode = True

    def start_filter(self, initpoints1=None, initpoints2=None):
        #print "start filter"
        self.log.debug("kalman filter enabled for object")
        self.predictionCounter = 0
        self.initFilter()#self.Rk, self.Qk)
        # initializing the coordinates as a column matrix
        initial_state=np.ones(shape=(self.num_variables, 1))*0.0001
        initial_state[0:7, 0]=self.firstOrderParams(initpoints1, initpoints2)
        self.updated_state[:, -1] = initial_state[:, 0]
        self.estimation_state[:, -1] = initial_state[:, 0]

    def addMeasurement(self, coordinates1, coordinates2, dt):
        first=self.firstOrderParams(coordinates1, coordinates2)
        m, Hk=self.secondOrderParams(dt, first)
        return m, Hk

    def checkWithinFrame(self, x, y):
        xval = int(round(x)) if round(x) > 0 and round(x) < self.max_x else None
        yval = int(y) if round(y) > 0 and round(y) < self.max_y else None
        return (xval, yval) if (xval is not None and yval is not None) else None

    def iterateTracks(self, coords1, coords2, dt, guessing_enabled=True, adaptive=False):
            #print "estimation mode before: ", self.estimationMode, "u before: ", self.updated_state[0:2, -1]
            #print "Qk:", self.Qk
            #print "Rk:", self.Rk
            # Hk:observation matrix

            # dt=17

            Fk=self.createF(dt)
            last_stable=None

            missingPoint = True if (coords1 is None) or (coords2 is None) else False
            # if the previous measurement was an estimation
            u = np.asmatrix(self.updated_state[:, -1].copy()).transpose()
            e = np.asmatrix(self.estimation_state[:, -1].copy()).transpose()
            m, mask = self.addMeasurement(coords1, coords2, dt)
            Hk=np.eye(self.num_variables)

            if self.estimationMode:
                # if this one is an estimation too
                if missingPoint:
                    # predicting from the last estimated
                    pred = Fk * e
                    cov = Fk * self.estimationP * Fk.transpose() + self.Qk
                else:
                    # print "returning from estimation mode to stable"
                    self.estimationMode = False
                    pred = Fk * u  # state matrix (4x1) or (6x1)
                    cov = Fk * self.Pk * Fk.transpose() + self.Qk  # A priori covariance matrix
            else:
                # print "staying in stable mode"
                pred = Fk * u  # state matrix (4x1) or (6x1)
                cov = Fk * self.Pk * Fk.transpose() + self.Qk  # A priori covariance matrix
                #if not missingPoint and (geom.distance(coordinates, pred[0:2]) > 30):
                    #print "outlier"
                #    missingPoint = True

            if missingPoint:
                #  print "missing point"
              #  last_stable = u[0:2, -1]
                if guessing_enabled and self.predictionCounter < self.maxPredictions:
                    self.estimationMode = True
                    #diff = np.zeros(shape=(self.num_variables, 1))
                    self.predictionCounter = self.predictionCounter + 1
                else:
                   # print "return without update"
                    coords=coords1 if coords2 is None else coords2
                    return (coords, None, None, None, None)
            else:
                # print "not missing"
                self.estimationMode = False  # this refers to the next circle
                self.predictionCounter = 0
                #diff = (m - Hk * pred)  # difference between prediction and measurement * mWeight
            diff = mask * (m - Hk * pred) #* mask  # difference between prediction and measurement * mWeight
            # steps of both tracks
            # setting the matrices
            S = np.linalg.inv(Hk * cov * Hk.T + self.Rk)
            Kgain = cov * Hk.T * S  # *mWeight # Kalman gain
            # update
            updateval = pred + Kgain * diff

            # if the values are stable
            if not self.estimationMode:
                # print "stable measurement"
                self.updated_state[:, -1] = updateval.A1.copy()
                # A posteriori covariance matrix
                self.Pk = (np.eye(self.num_variables) - (Kgain * Hk)) * cov
                # estimation_state is updated in every iteration, while the updated one is not

                if adaptive and (coords1 is not None) and (coords2 is not None):
                    self.log.debug("adaptive filtering...")
                    self.Qk = self.forget * self.Qk + (1 - self.forget) * Kgain * diff * diff.T * Kgain.T
                    res = m - (Hk * updateval)
                    self.Rk = self.forget * self.Rk + (1 - self.forget) * (res * res.T + (Hk * self.Pk * Hk.T))

            self.estimation_state[:, -1] = updateval.A1.copy()
            self.estimationP = self.Pk.copy()
            # if updated state wasn't changed, this shouldn't change either
            #last_stable = self.updated_state[0:2, -1].copy()

            sp = None
            movdir = None

            if updateval[11, 0] is not None and updateval[12, 0] is not None:
                sp = math.sqrt((updateval[11, 0]) ** 2 + (updateval[12, 0]) ** 2)
                if updateval[11, 0]!= 0 and updateval[12, 0] != 0:
                    movdir = math.ceil(math.fmod(math.degrees(math.atan2(updateval[12, 0], updateval[11, 0])) + 180, 360))

            retVal = (self.checkWithinFrame(updateval[4, 0], updateval[5, 0]), updateval[6, 0], sp, movdir , updateval[13, 0])

            # print self.calibrating
            # if self.calibrating and not missingPoint:
            #     self.QCalib.append(Kgain * diff * diff.T * Kgain.T)

            return retVal

    def stop_filter(self):
        self.log.debug("filter stopped")
        self.filter = None
        self.updated_state = None
        self.estimation_state = None
        self.Pk = None
        self.estimationP = None
