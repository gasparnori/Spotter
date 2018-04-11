import sys
import time
import datetime
import os
import logging
from lib import utilities as utils
from datetime import datetime


class DataLogger:
    def __int__(self, defaultpath=None):
        self.path=defaultpath
    def start(self, path):
        self.zerotime=time.time()
        if path is None:
            self.destination = 'recordings/time' + utils.time_string() +'.txt'
        else:
            if not path.lower().endswith('txt'):
                self.destination=path+'.txt'
            else:
                self.destination=path
        with open(self.destination, 'w') as text_file:
            text_file.write("log started: "+ datetime.now().strftime("%H:%M:%S.%f")+'\r\n')

    def update(self, slots):
        with open(self.destination, 'a') as text_file:
            text_file.write(""+datetime.now().strftime("%H:%M:%S.%f")+'\r\n')

