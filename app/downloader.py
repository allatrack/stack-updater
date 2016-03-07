#!/usr/bin/env python
# coding=utf-8

import os
import json
import urllib2
from logger import Logger
from app.config import *


class Downloader(object):

    __recipes_path = "./recipes"
    __gist_id = 0

    def __init__(self, base_path, id):
        self.__recipes_path = os.path.join(base_path, recipe_path())
        self.__gist_id = id

    def install_gist(self):
        """

        :param id: Github Gist Id
        :return:
        """

        gist = json.load(urllib2.urlopen('https://api.github.com/gists/{}'.format(self.__gist_id)))