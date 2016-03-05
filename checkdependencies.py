#!/usr/bin/env python
# coding=utf-8

import os
import sys
import subprocess
import logging
import json
import urllib2
import argparse
from versionhelper import VersionHelper


class DependenciesChecker(object):

    log_file_path = "./checkdependencies.log"
    recipes_path = "./recipes"
    recipes = []
    recipes_to_install = []
    exit_code = 0
    logger = None
    cli_args = None

    def __init__(self):
        pass

    @staticmethod
    def get_gist(id):
        """

        :param id: Github Gist Id
        :return:
        """

        gist = json.load(urllib2.urlopen('https://api.github.com/gists/{}'.format(id)))
        #if 'files' in

    def log_init(self, log_type):
        """

        :param log_type: Type of log to recording. Example logging.NOTSET
        """
        log_formatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
        self.logger = logging.getLogger()
        file_handler = logging.FileHandler(self.log_file_path)
        file_handler.setFormatter(log_formatter)
        self.logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(log_formatter)
        self.logger.addHandler(console_handler)

        self.logger.setLevel(log_type)

    def cli_init(self):
        """
        Initialize CLI arguments
        """
        parser = argparse.ArgumentParser(description='Check dependencies by recipe.')
        parser.add_argument('action', choices=['get', 'install', 'check'], default='check', nargs=1, help='get: Download recipe from Gist; install: Trying to install newer package versions; check: Simple check')
        parser.add_argument('gist_id', nargs='*', help='Gist ID to download recipe')

        self.cli_args = parser.parse_args()

    def load_recipes(self):

        try:
            recipe_files = [pos_recipe for pos_recipe in os.listdir(self.recipes_path) if pos_recipe.endswith('.json')]
        except Exception as e:
            self.logger.critical("There is no one receipt file in receipt directory. So sad :'(")
            raise e

        try:
            for recipe_file in recipe_files:
                with open(os.path.join(self.recipes_path, recipe_file)) as recipe_file_path:
                    for recipe in json.load(recipe_file_path):
                        self.recipes.insert(0, recipe)
            self.logger.info("Recipes was loaded")
        except Exception as e:
            self.logger.critical("Recipe files is not valid JSON")
            raise e

    def check(self):
        """
        Dependency checking without installing required version
        """
        self.logger.info("Start check dependencies")
        for recipe in self.recipes:
            real_version = subprocess.Popen(recipe["command"], stdout=subprocess.PIPE, shell=True).stdout.read()
            if VersionHelper.version_compare(real_version, recipe["required"], recipe["comparison"]):
                self.logger.info("{} version is valid".format(recipe["name"]))
            else:
                self.recipes_to_install.insert(0, recipe)
                self.logger.error(
                    "{} version is outdated. Expected {} instead {}".format(recipe["name"], recipe["required"], real_version))
                exit_code = 1  # general Error

    def install(self):
        """
        Dependency checking without installing required version
        """
        for recipe in self.recipes_to_install:
            real_version = subprocess.Popen(recipe["command"], stdout=subprocess.PIPE, shell=True).stdout.read()
            if VersionHelper.version_compare(real_version, recipe["required"], recipe["comparison"]):
                self.logger.info("{} version is valid".format(recipe["name"]))
            else:
                self.recipes_to_install.insert(0, recipe)
                self.logger.error(
                    "{} version is outdated. Expected {} instead {}".format(recipe["name"], recipe["required"], real_version))
                exit_code = 1  # general Error

    def run(self):

        self.log_init(logging.NOTSET)
        self.cli_init()

        if self.cli_args.action == ['get']:
            if len(self.cli_args.gist_id) > 0:
                self.get_gist(self.cli_args.gist_id[0])
            else:
                self.logger.error('Gist id not defined')
        else:
            self.load_recipes()
            self.check()
            if self.cli_args.action == ['install']:
                print "install"
                self.install()

        sys.exit(self.exit_code)


d_checker = DependenciesChecker()
d_checker.run()