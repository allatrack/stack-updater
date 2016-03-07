#!/usr/bin/env python
# coding=utf-8

import os
from app.cli import Cli
from app.logger import Logger
from app.config import *

base_path = os.path.dirname(os.path.realpath(__file__))

Logger().init_logger(logging.NOTSET, os.path.join(base_path, log_path()))

cli = Cli()
cli.run(base_path)