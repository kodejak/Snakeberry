# ----------------------------------------------------------------------------
# File:     configMgr.py
# Author:   kodejak <mail at kodejak dot de>
# License:  MIT <http://opensource.org/licenses/MIT>
#
# Simple config file management using "ConfigParser". The returned values are
# always strings.
# ----------------------------------------------------------------------------

import ConfigParser
import os.path
import logging

class MyConfig():
    filename = '/home/pi/snakeberry/snakeberry.cfg'

    # Create default config file
    def CreateConfig(self):
        try:
            config = ConfigParser.RawConfigParser()
            config.add_section('LastStream')
            config.add_section('Common')
            config.set('LastStream', 'Description', '')
            config.set('LastStream', 'Url', '')
            # indicates resuming if previously was playing
            config.set('LastStream', 'MustResume', 'false')
            # indicates resuming should be forced
            config.set('LastStream', 'ForceResume', 'false')
            # last volume
            config.set('Common', 'LastVolume', '')
            config.set('Common', 'CacheSize', '512')
            with open(self.filename, 'w+') as configfile:
                config.write(configfile)
        except Exception, e:
            logging.exception(e)

    # Set config file variable
    def SetVar(self, section, name, value):
        if os.path.exists(self.filename):
            pass
        else:
            self.CreateConfig()

        try:
            config = ConfigParser.SafeConfigParser()
            config.read(self.filename)
            config.set(section, name, str(value))

            with open(self.filename, 'w') as configfile:
                config.write(configfile)
        except Exception, e:
            logging.exception(e)

    # Get config file variable
    def GetVar(self, section, name):
        try:
            config = ConfigParser.RawConfigParser()
            config.read(self.filename)
            retVal = config.get(section, name)
            if len(retVal) > 0:
                return retVal
            else:
                return None
        except Exception, e:
            return None
