## radio.py
## This file is part of Snakeberry by Bruno Hautzenberger (http://the-engine.at)
## Dual-licensed under the MIT (http://www.opensource.org/licenses/mit-license.php)
## and the Beerware (http://en.wikipedia.org/wiki/Beerware) license.
##
## JSONP Support by: mail at kodejak dot de

import tornado.web, csv
from snakeberryJSON import *
from common import *
from mplayerInterface import *
from configMgr import *

#Representing a radio station
#Author: Bruno Hautzenberger
class Radio:
    def __init__(self, radioId, displayName, streamUrl):
        self.RadioId = radioId
        self.DisplayName = displayName
        self.StreamUrl = streamUrl
      
#Representing a list of radio stations
#Author: Bruno Hautzenberger  
class Radios:
    def __init__(self):
        self.Radios = []
        self.loadRadios()
        
    def loadRadios(self): 
        with open('/home/pi/snakeberry/radio.csv', 'rb') as csvfile:
            radioreader = csv.reader(csvfile, delimiter=';', quotechar='\"')
            
            count = 0
            for row in radioreader:
                self.Radios.append(Radio(str(count), row[0], row[1]))
                count = count + 1

#Webservice requesthandler to recieve list radio stations
#Author: Bruno Hautzenberger  
class ListRadios(tornado.web.RequestHandler):
    def get(self):
        rObject = None
        errNum = errNumOk
        errMsg = errMsgOk
        callbackFunc = self.get_argument('callback', None)
        
        try:
            radios = Radios()
            rObject = radios
        except Exception, err:
            errMsg = str(err)
            errNum = errNumListRadioStationsFailed
            
        if callbackFunc == None:
            self.write(SnakeberryJSON().encode(Response(errNum, errMsg, rObject)))
        else:
            self.write(callbackFunc +'('+ SnakeberryJSON().encode(Response(errNum, errMsg, rObject)) +')')


#Webservice requesthandler to play radio station with given id
#Author: Bruno Hautzenberger
#Edited: kodejak <mail at kodejak dot de>
class PlayRadio(tornado.web.RequestHandler):
    def get(self, radioId):
        rObject = None
        errNum = errNumOk
        errMsg = errMsgOk
        callbackFunc = self.get_argument('callback', None)
        
        try:
            streamUrl = None
            description = None
            for radio in Radios().Radios:
                if(radio.RadioId == radioId):
                    streamUrl = radio.StreamUrl
                    description = radio.DisplayName
                    break
                
            if(streamUrl == None):
                errNum = errNumRadioStationIdDoesNotExist
                errMsg = errMsgRadioStationIdDoesNotExist
            else:
                mplayer = MplayerProcess("Radio", description, streamUrl)
                Mplayer.play(mplayer)
                # remember radio station properties
                MyConfig().SetVar('LastStream', 'Description', description)
                MyConfig().SetVar('LastStream', 'Url', streamUrl)
                MyConfig().SetVar('LastStream', 'MustResume', 'true')
        except Exception, err:
            errMsg = str(err)
            errNum = errNumPlayRadioStationFailed
            
        if callbackFunc == None:
            self.write(SnakeberryJSON().encode(Response(errNum, errMsg, rObject)))
        else:
            self.write(callbackFunc +'('+ SnakeberryJSON().encode(Response(errNum, errMsg, rObject)) +')')

#Webservice requesthandler to stop radio
#Author: Bruno Hautzenberger
#Edited: kodejak <mail at kodejak dot de>
class StopRadio(tornado.web.RequestHandler):
    def get(self):
        rObject = None
        errNum = errNumOk
        errMsg = errMsgOk
        callbackFunc = self.get_argument('callback', None)
        
        try:
            Mplayer.stop()
            # remember that the radio station was stopped
            MyConfig().SetVar('LastStream', 'MustResume', 'false')
        except Exception, err:
            errMsg = str(err)
            errNum = errNumStopRadioStationFailed
            
        if callbackFunc == None:
            self.write(SnakeberryJSON().encode(Response(errNum, errMsg, rObject)))
        else:
            self.write(callbackFunc +'('+ SnakeberryJSON().encode(Response(errNum, errMsg, rObject)) +')')

#Webservice requesthandler to recieve what information about what the radio is playing
#Author: Bruno Hautzenberger         
class RadioNowPlaying(tornado.web.RequestHandler):
    def get(self):
        rObject = None
        errNum = errNumOk
        errMsg = errMsgOk
        callbackFunc = self.get_argument('callback', None)
        
        try:
            rObject = Mplayer.currentProcess
            if(rObject == None):
                rObject = MplayerProcess("Radio", "---", "")
        except Exception, err:
            errMsg = str(err)
            errNum = errNumStopRadioStationFailed
            
        if callbackFunc == None:
            self.write(SnakeberryJSON().encode(Response(errNum, errMsg, rObject)))
        else:
            self.write(callbackFunc +'('+ SnakeberryJSON().encode(Response(errNum, errMsg, rObject)) +')')
