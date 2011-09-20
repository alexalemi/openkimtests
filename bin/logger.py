"""
Holds the logger for the openkimtest project 
"""


import logging
import logging.handlers

import os.path
import openkimtests
openkimtest_dir = os.path.dirname(openkimtests.__file__)


LOG_FILENAME = os.path.join(openkimtest_dir,'logs','openkimlog.log')
WARN_FILENAME = os.path.join(openkimtest_dir,'logs','openkimlog.warning.log')


#create the logger
logger = logging.getLogger('openkimtests')
logger.setLevel(logging.DEBUG)

#create the file handler

fh = logging.handlers.RotatingFileHandler(
              LOG_FILENAME, maxBytes=200000, backupCount=5)
fh.setLevel(logging.DEBUG)


#create a second file handler
fh2 = logging.handlers.RotatingFileHandler(
              WARN_FILENAME, maxBytes=200000, backupCount=5)
fh2.setLevel(logging.WARNING)


#create the stream handler
ch = logging.StreamHandler()
ch.setLevel(logging.WARNING)

#create the formatter and attach
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
fh2.setFormatter(formatter)

#add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)
logger.addHandler(fh2)

logger.info('BEGINNING RUN')

