import logging
import os
from utils.functions import removeFiles

class BaseLogger:
    def __init__(self,className, remove = False):
        FORMAT = '%(asctime)s [%(levelname)s] [%(module)s."%(filename)s".%(funcName)s]: %(message)s'
        DATE_FORMAT = '%d/%m/%Y %H:%M:%S'
        LOGFILE_NAME = 'neural.log'
        if remove:
            removeFiles(LOGFILE_NAME)

        logging.basicConfig(level=logging.INFO, 
                            format = FORMAT, 
                            filename = LOGFILE_NAME,
                            filemode = 'a',
                            datefmt = DATE_FORMAT)
        self.logger = logging.getLogger(className)