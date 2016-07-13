# coding=utf-8

import json
import os
import urllib2

from config import *
from lib import logger
from lib.wrappers import silent_remove


class Downloader(object):

    __recipes_path = "./recipes"
    __gist_id = 0

    def __init__(self, base_path, gist_id, recipe_path=''):
        self.__recipes_path = recipe_path or os.path.join(
            base_path, default_recipe_path())
        self.__gist_id = gist_id

    @staticmethod
    def get_gist_files_path(gist, file_ending):
        return [gist['files'][filename]["raw_url"] for filename in
                gist['files'] if filename.endswith(file_ending)]

    def install_gist(self):

        logger.info("Trying to get Gist")
        gist = json.load(urllib2.urlopen(
            'https://api.github.com/gists/{}'.format(self.__gist_id)))
        try:
            # first json file for config
            config_file = self.get_gist_files_path(gist, '.json')[0]
            bash_files = self.get_gist_files_path(gist, '.sh')
        except Exception as e:
            logger.critical(
                "This is invalid gist_id or something else went wrong")
            raise e

        logger.info("Trying to save recipe files")
        try:
            bash_dir = os.path.join(self.__recipes_path, os.path.splitext(
                os.path.basename(config_file))[0])
            if not os.path.exists(bash_dir):
                os.makedirs(bash_dir)
            config_file_path = os.path.join(
                self.__recipes_path, os.path.basename(config_file))
            silent_remove(config_file_path)
            with open(config_file_path, "wb") as local_file:
                local_file.write(urllib2.urlopen(config_file).read())
            for bash_file in bash_files:
                bash_file_path = os.path.join(
                    bash_dir, os.path.basename(bash_file))
                silent_remove(bash_file_path)
                with open(bash_file_path, "wb") as local_file:
                    local_file.write(urllib2.urlopen(bash_file).read())
            logger.info("Recipe files was saved successfully")
        except Exception as e:
            logger.critical("Something went wrong with the internet. "
                            "Internet dies[SCREAMING]. Run, quickly run away")
            raise e
