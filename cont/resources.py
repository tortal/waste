#  -*- coding: utf-8 -*-
# python 2.7.5
# author: roy.nard@gmail.com
# os: win32

# Config name constants (to be used in config files such as config.ini)

#  Folder containing all graphics, fonts, audio, maps and other resources.
import os
import ConfigParser
from cont import debug

ASSETS_PKG = 'assets'
ASSETS_PATH = './' + ASSETS_PKG + '/'

#   Configuration files
# Names with this suffix will be treated as file paths
SUFFIX_DELIMITER = '_'
PATH_SUFFIX = SUFFIX_DELIMITER + 'path'


# Constants

TTF = 'ttf'
PNG = 'png'
INI = 'ini'

class Assets(object):
    """ This constructs an object that will contain all relevant resource files in the
    folder specified ASSETS_PATH.
    """

    def __init__(self):
        self.sections = set()
        self.config = {}

        # List all files in ASSETS_PATH

        cfgParser = ConfigParser.ConfigParser()
        cfgParser.read('./assets\\config.ini')

        for section in cfgParser.sections():
            for name, value in cfgParser.items(section):

                if name.endswith(PATH_SUFFIX):
                    filePath = os.path.join(ASSETS_PATH, value)
                    self._addConfig(section, name, filePath)

        debug.log(self.config)

    def _addConfig(self, section, name, value):
        try:
            self.config[section][name] = value
        except KeyError:
            self.config[section] = {name: value}

    def getConfig(self, section, key):
        return self.config[section][key]