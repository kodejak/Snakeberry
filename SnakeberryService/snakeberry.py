## common.py
## This file is part of Snakeberry by Bruno Hautzenberger (http://the-engine.at)
## Dual-licensed under the MIT (http://www.opensource.org/licenses/mit-license.php)
## and the Beerware (http://en.wikipedia.org/wiki/Beerware) license.

import tornado.ioloop
import tornado.web, csv
import logging
from snakeberryJSON import *
from radio import *
from audioSystem import *
from services import *
from mplayerInterface import *
from configMgr import *

#Main loop
#Generates all service endpoints
#Author: Bruno Hautzenberger
#Edited: kodejak <mail at kodejak dot de>
if __name__ == "__main__":
    application = tornado.web.Application([
        (r"/", ListServices),
        (r"/radios", ListRadios),
        (r"/radio/play/(.*)", PlayRadio),
        (r"/radio/stop", StopRadio),
        (r"/radio/nowplaying", RadioNowPlaying),
        (r"/getvolume", GetVolume),
        (r"/setvolume/(.*)", SetVolume),
        (r"/getmac", GetMac),
    ])
    
    application.listen(8888)

    # Resume playing if needed and possible
    mplayer = None
    lastStationDesc = MyConfig().GetVar('LastStream', 'Description')
    lastStationUrl = MyConfig().GetVar('LastStream', 'Url')
    mustResume = MyConfig().GetVar('LastStream', 'MustResume')
    forceResume = MyConfig().GetVar('LastStream', 'ForceResume')

    if lastStationDesc != None and lastStationUrl != None and \
      (mustResume == 'true' or forceResume == 'true'):
        mplayer = MplayerProcess("Radio", lastStationDesc, lastStationUrl)   	

    if mplayer != None:
        Mplayer.play(mplayer)
        
    # Restore last volume
    lastVolume = MyConfig().GetVar('Common', 'LastVolume')
    try:
        if (lastVolume != None):
            subprocess.call(['sudo', 'amixer', 'set', 'PCM', '--', lastVolume]) #ROOT CALL
    except Exception, e:
        logging.exception(e)

    tornado.ioloop.IOLoop.instance().start()



