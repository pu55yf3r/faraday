from __future__ import absolute_import
# Faraday Penetration Test IDE
# Copyright (C) 2016  Infobyte LLC (http://www.infobytesec.com/)
# See the file 'doc/LICENSE' for the license information

import ConfigParser
import logging
import json
import os, shutil
import errno

from config import globals as CONSTANTS

DEBUG = True
LOGGING_LEVEL = logging.DEBUG

FARADAY_BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
REQUIREMENTS_FILE = os.path.join(FARADAY_BASE, 'requirements_server.txt')
DEFAULT_CONFIG_FILE = os.path.join(FARADAY_BASE, 'server/default.ini')
VERSION_FILE = os.path.join(FARADAY_BASE, CONSTANTS.CONST_VERSION_FILE)
WEB_CONFIG_FILE = os.path.join(FARADAY_BASE, 'server/www/config/config.json')
LOCAL_CONFIG_FILE = os.path.expanduser(
    os.path.join(CONSTANTS.CONST_FARADAY_HOME_PATH, 'config/server.ini'))

CONFIG_FILES = [ DEFAULT_CONFIG_FILE, LOCAL_CONFIG_FILE ]
WS_BLACKLIST = CONSTANTS.CONST_BLACKDBS


def copy_default_config_to_local():
    if not os.path.exists(LOCAL_CONFIG_FILE):
        # Create directory if it doesn't exist
        try:
            os.makedirs(os.path.dirname(LOCAL_CONFIG_FILE))
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        # Copy default config file into faraday local config
        shutil.copyfile(DEFAULT_CONFIG_FILE, LOCAL_CONFIG_FILE)

        print("[!] Local Faraday-Server configuration created in %s" % LOCAL_CONFIG_FILE)

def parse_and_bind_configuration():
    """Load configuration from files declared in this module and put them
    on this module's namespace for convenient access"""

    __parser = ConfigParser.SafeConfigParser()
    __parser.read(CONFIG_FILES)

    class ConfigSection(object):
        def __init__(self, name, parser):
            self.__name = name
            self.__parser = parser

        def __getattr__(self, option_name):
            return self.__parser.get(self.__name, option_name)

    for section in __parser.sections():
        globals()[section] = ConfigSection(section, __parser)

def __get_version():
    try:
        version = open(VERSION_FILE, 'r').read().strip()
    except:
        version = ''
    return version

def gen_web_config():
    doc = {
        'ver': __get_version(),
        'lic_db': CONSTANTS.CONST_LICENSES_DB
    }
    if os.path.isfile(WEB_CONFIG_FILE):
        os.remove(WEB_CONFIG_FILE)
    with open(WEB_CONFIG_FILE, "w") as doc_file:
        json.dump(doc, doc_file)

copy_default_config_to_local()
parse_and_bind_configuration()
gen_web_config()

