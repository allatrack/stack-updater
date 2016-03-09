# coding=utf-8

import time
import re
import os
import stat
import logging
import logging.handlers as handlers
from singleton import Singleton

class SizedTimedRotatingFileHandler(handlers.TimedRotatingFileHandler):
    """
    Handler for logging to a set of files, which switches from one file
    to the next when the current file reaches a certain size, or at certain
    timed intervals
    """
    def __init__(self, filename, mode='a', maxBytes=0, backupCount=0, encoding=None,
                 delay=0, when='h', interval=1, utc=False):
        # If rotation/rollover is wanted, it doesn't make sense to use another
        # mode. If for example 'w' were specified, then if there were multiple
        # runs of the calling application, the logs from previous runs would be
        # lost if the 'w' is respected, because the log file would be truncated
        # on each run.
        if maxBytes > 0:
            mode = 'a'
        handlers.TimedRotatingFileHandler.__init__(
            self, filename, when, interval, backupCount, encoding, delay, utc)
        self.maxBytes = maxBytes

    def shouldRollover(self, record):
        """
        Determine if rollover should occur.

        Basically, see if the supplied record would cause the file to exceed
        the size limit we have.
        """
        if self.stream is None:                 # delay was set...
            self.stream = self._open()
        if self.maxBytes > 0:                   # are we rolling over?
            msg = "%s\n" % self.format(record)
            self.stream.seek(0, 2)  #due to non-posix-compliant Windows feature
            if self.stream.tell() + len(msg) >= self.maxBytes:
                return 1
        t = int(time.time())
        if t >= self.rolloverAt:
            return 1
        return 0

class Logger(Singleton):

    __log_filename = 'updater.log'
    __logger = None

    def __init__(self):
        pass

    def init_logger(self, log_type, path):
        """

        :param log_type: Type of log to recording. Example logging.NOTSET
        """
        log_file_path = os.path.join(path, self.__log_filename)
        log_formatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
        self.__logger = logging.getLogger()

        file_handler = SizedTimedRotatingFileHandler(
            log_file_path, maxBytes=100, backupCount=5, when='s', interval=10, 
            # encoding='bz2',  # uncomment for bz2 compression
            )
        file_handler = logging.FileHandler(self.log_file_path)
        file_handler.setFormatter(log_formatter)
        self.__logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(log_formatter)
        self.__logger.addHandler(console_handler)

        self.__logger.setLevel(log_type)

    def __call__(self):
        return self.__logger