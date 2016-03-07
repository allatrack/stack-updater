# coding=utf-8

import os
import sys
import subprocess
import json
from helpers.version import VersionHelper
from logger import Logger
from config import *


class Dependency(object):

    __recipes = []
    __recipes_to_install = []
    __recipes_file_path

    def __init__(self, base_path):
        """
        Load recipes from file
        """

        self.__recipes_file_path = os.path.join(base_path, recipe_path())

        try:
            recipe_files = [pos_recipe for pos_recipe in os.listdir(self.__recipes_file_path) if pos_recipe.endswith('.json')]
        except Exception as e:
            Logger().critical("There is no one receipt file in receipt directory. So sad :'(")
            raise e

        try:
            for recipe_file in recipe_files:
                with open(os.path.join(self.__recipes_file_path, recipe_file)) as recipe_file_path:
                    for recipe in json.load(recipe_file_path):
                        self.__recipes.insert(0, recipe)
            Logger().info("Recipes was loaded")
        except Exception as e:
            Logger().critical("Recipe files is not valid JSON")
            raise e

    def check(self):
        """
        Dependency checking without installing required version
        """
        exit_code = 0
        Logger().info("Start check dependencies")
        for recipe in self.__recipes:
            real_version = subprocess.Popen(recipe["command"], stdout=subprocess.PIPE, shell=True).stdout.read()
            if VersionHelper.version_compare(real_version, recipe["required"], recipe["comparison"]):
                Logger().info("{} version is valid".format(recipe["name"]))
            else:
                self.__recipes_to_install.insert(0, recipe)
                Logger().error(
                    "{} version is outdated. Expected {} instead {}".format(recipe["name"], recipe["required"], real_version))
                exit_code = 1  # general Error
        return exit_code

    def install(self):
        """
        Dependency checking with installing required version
        """
        self.check()

        for recipe in self.__recipes_to_install:
            return True