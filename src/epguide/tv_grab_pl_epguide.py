#!/usr/bin/python

from common import Config
from epguide import EpGuide
import sys
import time
import datetime
from optparse import OptionParser, Option, OptionValueError, Values
from copy import copy
import time
import datetime
from optparse import OptionParser, Option, OptionValueError
from copy import copy

from parsers import TelemanParser 
from formatters import TxtOutput, XmltvOutput, FileOutput
from configobj import ConfigObj
from os.path import expanduser, normpath
import os
import logging

class TvGrabPlEpguide(object):
    """
    glowna petla aplikacji, odczytuje konfiguracje, uruchamia operacje
    """
    
    def __init__(self):
        self.options = None
        self.args = None
        self.parser = None
        self.output = None
        
        self.usage=""" Application, that can get You electronic TV guide in various formats
                       %prog [options] """

        
        self.cmdparser = OptionParser(usage=self.usage)
        #--help, --version, --capabilities, --description options for the grabber and it handles the --configure and --configure-api options by calling callbacks supplied by the grabber. Furthermore, it handles the --output option b

        
        self.cmdparser.add_option ("--description", dest="description", action="store_true", default=False, help="Print a description that identifies the grabber")
#        self.cmdparser.add_option ("--help", dest="split_title", action="store_true", default=False, help="split title into title, subtitle and episode num (if possible)")
#        self.cmdparser.add_option ("--version", dest="split_title", action="store_true", default=False, help="split title into title, subtitle and episode num (if possible)")

        self.cmdparser.add_option ("--capabilities", dest="capabilities", action="store_true", default=False, help="Print a list of all the capabilities supported by this grabber")
        #baseline
        self.cmdparser.add_option ("--quiet", dest="capabilities", action="store_true", default=False, help="Suppress all progress information. Only error-messages are printed to stderr. ")
        self.cmdparser.add_option ("--output", dest="output", help="Redirect the xmltv output to the specified file. Otherwise output goes to stdout.")
        self.cmdparser.add_option ("--logfile", dest="logfile", default=normpath(expanduser("~/.epguide/tv_grab_pl_epguide.log")), help="Log to specified file.")
        self.cmdparser.add_option ("--days", dest="days", default=7, help="Supply data for X days. The default number of days is 'as many as possible' - it means 1 day.")
        self.cmdparser.add_option ("--offset", dest="offset", default=0, help="Start with data for day today plus X days. The default is 0, today; 1 means start from tomorrow, etc.")
        #manualconfig
        self.cmdparser.add_option ("--configure", dest="configure", action="store_true", default=False, help="Allow the user to answer questions regarding the operation of the grabber. This can allow the user to specify which channels he wants to download data for.")
        self.cmdparser.add_option ("--config-file", dest="config_file", default=normpath(expanduser("~/.epguide/tv_grab_pl_epguide.ini")), help="The grabber shall read all configuration data from the specified file. If this parameter is combined with --configure, the configuration is written to the specified file.")
#        self.cmdparser.add_option ("--configure-api", dest="split_title", action="store_true", default=False, help="split title into title, subtitle and episode num (if possible)")

    def run(self):
        self.options, self.args = self.cmdparser.parse_args(sys.argv)

        if (self.options.description):
            print "Poland (epguide using teleman.pl)"
            return 0
        elif (self.options.capabilities):
            print "baseline"
            print "manualconfig"
            return 0
        elif (self.options.configure):
            print "Configure tv_grab_pl_epguide"
            configFile = ConfigObj(self.options.config_file)
            config = Config()
            config.options = Values(config.cmdparser.defaults)
            configFile['timestamp'] = datetime.datetime.today()
            print
            channels = configFile.get('channels', [])
            print "Currently configured channels: " + ",".join(channels)
            channels = raw_input("Enter comma separated channels (for example: TVP-1,TVP-2,TVN,Polsat) or Enter to leave unchanged: ")
            if len(channels.strip()) > 0:
                configFile['channels'] = channels.strip().split(',')
            else:
                print "Channels not changed" 
            print
            configFile['split-title'] = config.options.split_title 
            configFile['add-original-title-to-title'] = config.options.add_original_title_to_title 
            configFile['add-year-to-title'] = config.options.add_year_to_title
            configFile['add-age-rating-to-title'] = config.options.add_age_rating_to_title

            directory = os.path.dirname(self.options.config_file)
            if not os.path.exists(directory):
                os.mkdir(directory)
               
            configFile.write()
            print "Configuration file written to " + self.options.config_file
            return 0
        else:
            config = Config()
            config.options = Values(config.cmdparser.defaults)
            config.options.get_days = self.options.days
            config.options.output = "xmltv"
            config.options.filename = self.options.output
            config.options.logfile = normpath(expanduser("~/.epguide/tv_grab_pl_epguide.log")) #self.options.logfile
            directory = os.path.dirname(self.options.logfile)
            if not os.path.exists(directory):
                os.mkdir(directory)
            configFile = ConfigObj(self.options.config_file)
            
            if config.options.logfile:
                logging.basicConfig(filename=self.options.logfile,level=logging.DEBUG)
            else:
                logging.basicConfig()

            self.log = logging.getLogger("tv_grab_pl_epguide")
            self.log.info("xyz")
            channels = configFile.get('channels', None)
            if not channels:
                print "No channels found in configuration file. Please run with --configure option first."
                return -1
            else:
                if isinstance(channels, basestring): #jeden kanal to String a nie List
                    config.options.channel_list = [channels]
                else:
                    config.options.channel_list = channels
                config.options.split_title = configFile['split-title']
                config.options.add_original_title_to_title = configFile['add-original-title-to-title']
                config.options.add_year_to_title = configFile['add-year-to-title']
                config.options.add_age_rating_to_title = configFile['add-age-rating-to-title']
                
                config.parser = TelemanParser.TelemanParser(config.options, False)
    
                config.output = FileOutput.FileOutput(config.options.filename, XmltvOutput.XmltvOutput())
                config.date_from = datetime.datetime.today()
                config.date_to = datetime.datetime.today() + datetime.timedelta(days=int(config.options.get_days))
                config.get_guide = True
    
                epguide = EpGuide(config)
                epguide.Execute()
                return 0

def RunTvGrabPlEpguide():
    grabber = TvGrabPlEpguide()
    return grabber.run()

if __name__ == '__main__':
    RunTvGrabPlEpguide()
    