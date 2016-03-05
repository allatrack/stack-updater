#!/usr/bin/env python

import os
import sys
import subprocess
import logging
import json
from distutils.version import LooseVersion, StrictVersion

def version_compare(v1, v2, op=None):
    _map = {
        '<': [-1],
        'lt': [-1],
        '<=': [-1, 0],
        'le': [-1, 0],
        '>': [1],
        'gt': [1],
        '>=': [1, 0],
        'ge': [1, 0],
        '==': [0],
        'eq': [0],
        '!=': [-1, 1],
        'ne': [-1, 1],
        '<>': [-1, 1]
    }
    v1 = LooseVersion(v1)
    v2 = LooseVersion(v2)
    result = cmp(v1, v2)
    if op:
        assert op in _map.keys()
        return result in _map[op]
    return result

# Initialize loging
logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
logger = logging.getLogger()
logFilePath = "./checkdependencies.log"
fileHandler = logging.FileHandler(logFilePath)
fileHandler.setFormatter(logFormatter)
logger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
logger.addHandler(consoleHandler)

# All logs are recording
logger.setLevel(logging.NOTSET)

logger.info("Start check dependencies")

# Load receipt files
receipesPath = "./receipes"
try:
    receipeFiles = [posReceipe for posReceipe in os.listdir(receipesPath) if posReceipe.endswith('.json')]
except Exception as e:
    logger.critical("There is no one receipt file in receipt directory. So sad :'(")
    raise e

# Load all receipts
receipes = []
try:
    for receipeFile in receipeFiles:
	with open(os.path.join(receipesPath, receipeFile)) as receipeFilePath:
	    for receipe in json.load(receipeFilePath):
	        receipes.insert(0, receipe)
    logger.info("Receipes was loaded")
except Exception as e:
    logger.critical("Receipe files is not valid JSON")
    raise e

exitCode = 0;
for receipe in receipes:
    realVersion = subprocess.Popen(receipe["command"], stdout=subprocess.PIPE, shell=True).stdout.read()
    if version_compare(realVersion, receipe["required"], receipe["comparsion"]):
        logger.info("{} version is valid".format(receipe["name"]))
    else:
        logger.error("{} version is outdated. Expected {} instead {}".format(receipe["name"], receipe["required"], realVersion))
        exitCode = 1 #general Error

sys.exit(exitCode)
