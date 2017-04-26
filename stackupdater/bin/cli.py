# coding=utf-8

import argparse
import sys

from stackupdater.src.lib import logger
from stackupdater.src.dependency import Dependency
from stackupdater.src.downloader import Downloader


class Cli(object):
    __cli_args = None
    __base_path = "/"

    def __init__(self, base_path):
        """
        Initialize CLI arguments
        """
        parser = argparse.ArgumentParser(
            description='Check dependencies by recipe.')
        parser.add_argument('action', choices=['get', 'install', 'check'],
                            default='check', nargs=1,
                            help='get: Download recipe from Gist; \ninstall: '
                                 'Trying to install newer package versions; '
                                 '\ncheck: Simple check')
        parser.add_argument('param', nargs='?',
                            help='Custom recipe directory or gist ID '
                                 'to download recipe')
        parser.add_argument("-v", "--verbose", action="store_true",
                            help="With this flag you can see on the display"
                                 "(not in the log file) "
                                 "triggered command output.")

        self.__cli_args = parser.parse_args()

        self.__base_path = base_path

    def run(self):
        method = getattr(self, self.__cli_args.action[0])
        if not method:
            logger.error(
                "Method {} not implemented".format(self.__cli_args.action[0]))
            raise NotImplementedError(
                "Method {} not implemented".format(self.__cli_args.action[0]))
        method()

    def get(self):
        """
        Download recipe from Gist
        """
        if len(self.__cli_args.param) > 0:  # ID of Gist not empty
            recipe_downloader = Downloader(
                self.__base_path, self.__cli_args.param)
            recipe_downloader.install_gist()
        else:
            logger.error('Gist id not defined')

    def check(self):
        """
        Check dependencies
        """
        checker = Dependency(self.__base_path, self.__cli_args.param)
        exit_code = checker.check()

        sys.exit(exit_code)

    def install(self):
        """
        Install dependencies
        """
        installer = Dependency(self.__base_path, self.__cli_args.param)
        exit_code = installer.install(self.__cli_args.verbose)

        sys.exit(exit_code)
