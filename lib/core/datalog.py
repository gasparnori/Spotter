import sys
import time
import datetime
import os
import logging
from lib import utilities as utils
from datetime import datetime
import json


class DataLogger:
    def __int__(self, defaultpath=None):
        self.path=defaultpath
    def start(self, path):
        self.zerotime=time.time()
        if path is None:
            self.destination = 'recordings/log' + utils.time_string() +'.txt'
        else:
            if not path.lower().endswith('txt'):
                self.destination=path+utils.time_string()+'.txt'
            else:
                self.destination=path
        with open(self.destination, 'w') as text_file:
            text_file.write("############### log started: "+ datetime.now().strftime("%H:%M:%S.%f")+'\r\n')
            text_file.write("############### the log data is saved in json format. The data structure is the following:\r\n")
            text_file.write("###############        time stamp,\r\n")
            text_file.write("###############        object_0: label, X, Y, speed, direction, linked LEDs (to object_0): label, position \r\n")
            text_file.write("###############        object_1: label, X, Y, speed, direction, linked LEDs (to object_0): label, position \r\n")


    def update(self, slots, objects):
        #print slots
        txt=json.dumps(objects)
        with open(self.destination, 'a') as text_file:
            text_file.write(txt+'\r\n')
           # text_file.write(','.join(objects))

    # helper code for reading back the log
    def read_log(path):
        loglist = []
        with open(path, 'r') as f:
            for line in f:
                if line.startswith('#'):
                    pass
                else:
                    line.strip('\r\n')
                    print line
                    loglist.append(json.loads(line))
        return loglist


