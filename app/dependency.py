# coding=utf-8

import os
import subprocess
import json
from helpers import VersionHelper
from logger import logger
from config import *


class Dependency(object):

    __recipes = []
    __recipes_to_install = []

    @property
    def __extract_order(json):
        try:
            # Also convert to int since update_time will be string.  When comparing
            # strings, "10" is smaller than "2".
            return int(json['page']['update_time'])
        except KeyError:
            return 0

    def __init__(self, base_path):
        """
        Load recipes from file
        """
        logger.info("Start loading recipes")
        self.__recipes_file_path = os.path.join(base_path, recipe_path())
        try:
            recipe_files = [pos_recipe for pos_recipe in sorted(os.listdir(self.__recipes_file_path)) if pos_recipe.endswith('.json')]
        except Exception as e:
            logger.critical("There is no one receipt file in receipt directory({}). So sad :'(".format(self.__recipes_file_path))
            raise e

        try:
            for recipe_file in recipe_files:
                recipes_from_file = json.load(open(os.path.join(self.__recipes_file_path, recipe_file)))
                recipes_from_file.sort(key = lambda k: k.get('order', 0), reverse = True)
                for recipe in recipes_from_file:
                    recipe['filename'] = os.path.splitext(recipe_file)[0]
                    self.__recipes.insert(0, recipe)
            logger.info("Recipes was loaded")
            print self.__recipes
        except Exception as e:
            logger.critical("Recipe files is not valid JSON")
            raise e

    def check(self):
        """
        Dependency checking without installing required version
        """
        exit_code = 0
        logger.info("Start check dependencies")
        for recipe in self.__recipes:
            real_version = subprocess.Popen(recipe["command"], stdout=subprocess.PIPE, shell=True).stdout.read()
            if VersionHelper.version_compare(real_version, recipe["required"], recipe["comparison"]):
                logger.info("{} version is valid".format(recipe["name"]))
            else:
                self.__recipes_to_install.insert(0, recipe)
                logger.error(
                    "{} version is outdated. Expected {} instead {}".format(recipe["name"], recipe["required"], real_version))
                exit_code = 1  # general Error
        return exit_code

    def install(self):
        """
        Dependency checking with installing required version
        """
        self.check()

        for recipe in self.__recipes_to_install:
            logger.info("Trying to update {}".format(recipe["name"]))
            cmd =  "sudo sh " + os.path.join(self.__recipes_file_path, recipe["filename"], recipe["installer"])
            logger.info("Execute {}".format(cmd))
            logger.log_command(cmd, self.__recipes_file_path)