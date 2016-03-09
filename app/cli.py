# coding=utf-8

import sys
import argparse
from logger import logger
from downloader import Downloader
from dependency import Dependency


class Cli(object):

    __cli_args = None
    __base_path = "/"

    def __init__(self, base_path):
        """
        Initialize CLI arguments
        """
        parser = argparse.ArgumentParser(description='Check dependencies by recipe.')
        parser.add_argument('action', choices=['get', 'install', 'check'], default='check', nargs=1, help='get: Download recipe from Gist; \ninstall: Trying to install newer package versions; \ncheck: Simple check')
        parser.add_argument('gist_id', nargs='*', help='Gist ID to download recipe')

        self.__cli_args = parser.parse_args()

        self.__base_path = base_path

    def run(self):
        method = getattr(self, self.__cli_args.action[0])
        if not method:
            logger.error("Method {} not implemented".format(self.__cli_args.action[0]))
            raise NotImplementedError("Method {} not implemented".format(self.__cli_args.action[0]))
        method()

    def get(self):
        """
        Download recipe from Gist
        """
        if len(self.__cli_args.gist_id) > 0: #ID of Gist not empty
            recipe_downloader = Downloader(self.__base_path, self.__cli_args.gist_id[0])
            recipe_downloader.install_gist()
        else:
            logger.error('Gist id not defined')

    def check(self):
        """
        Check dependencies
        """
        checker = Dependency(self.__base_path)
        exit_code = checker.check()

        sys.exit(exit_code)

    def install(self):
        """
        Install dependencies
        """
        installer = Dependency(self.__base_path)
        exit_code = installer.install()

        sys.exit(exit_code)