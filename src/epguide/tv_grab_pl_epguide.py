#!/usr/bin/python

from abstract_epguide import AbstractEpGuide
from common import Config
from configobj import ConfigObj
from copy import copy
from epguide import EpGuide
from formatters import XmltvOutput, FileOutput
from optparse import OptionParser, Option, OptionValueError, Values
from os.path import expanduser, normpath
from parsers import TelemanParser, GazetaParser
import datetime
import logging
import logging.config
import os
import shutil
import sys
import time


class TvGrabPlEpguide(AbstractEpGuide):
    """
    glowna petla aplikacji, odczytuje konfiguracje, uruchamia operacje
    """
    
    def __init__(self):
        AbstractEpGuide.__init__(self)

        self.tv_grab_options = None
        self.args = None
        self.parser = None
        self.output = None
        
        self.usage=""" Application, that can get You electronic TV guide in various formats
                       %prog [tv_grab_options] """

        
        self.cmdparser = OptionParser(usage=self.usage)
        #--help, --version, --capabilities, --description tv_grab_options for the grabber and it handles the --configure and --configure-api tv_grab_options by calling callbacks supplied by the grabber. Furthermore, it handles the --output option b
        
        self.cmdparser.add_option ("--description", dest="description", action="store_true", default=False, help="Print a description that identifies the grabber")
        self.cmdparser.add_option ("--capabilities", dest="capabilities", action="store_true", default=False, help="Print a list of all the capabilities supported by this grabber")
        
        #baseline
        self.cmdparser.add_option ("--quiet", dest="quiet", action="store_true", default=False, help="Suppress all progress information. Only error-messages are printed to stderr. ")
        self.cmdparser.add_option ("--output", dest="output", help="Redirect the xmltv output to the specified file. Otherwise output goes to stdout.")
        self.cmdparser.add_option ("--logfile", dest="logfile", help="Log to specified file.")
        self.cmdparser.add_option ("--days", dest="days", help="Supply data for X days. The default number of days is 'as many as possible' - it means 7 days.")
        
        #manualconfig
        self.cmdparser.add_option ("--configure", dest="configure", action="store_true", default=False, help="Allow the user to answer questions regarding the operation of the grabber. This can allow the user to specify which channels he wants to download data for.")
        self.cmdparser.add_option ("--config-file", dest="config_file", default=normpath(expanduser("~/.epguide/tv_grab_pl_epguide.ini")), help="The grabber shall read all configuration data from the specified file. If this parameter is combined with --configure, the configuration is written to the specified file.")
        self.cmdparser.add_option ("--log-level", dest="log_level", default=logging.INFO, help="Log level: ERROR = 40, WARN = 30, INFO = 20, DEBUG = 10")

    def print_description(self):
        print "Poland (epguide using teleman.pl or gazeta.pl)"
        return 0

    def print_capabilities(self):
        print "baseline"
        print "manualconfig"
        return 0
    
    def configure(self):
        print "Configure tv_grab_pl_epguide"
        tv_grab_config_obj = ConfigObj(self.tv_grab_options.config_file)
        epguide_config = Config()
        epguide_config.options = Values(epguide_config.cmdparser.defaults)
        self.setup(epguide_config)
        tv_grab_config_obj['timestamp'] = datetime.datetime.today()
        print
        channels = tv_grab_config_obj.get('channels', [])
        if isinstance(channels, basestring): #jeden kanal to String a nie List
            channels = [channels]
        print "Currently configured channels: " + ",".join(channels)

        channels = raw_input("Enter comma separated channels (for example: TVP-1,TVP-2,TVN,Polsat) or Enter to leave unchanged: ")
        if len(channels.strip()) > 0:
            tv_grab_config_obj['channels'] = channels.strip().split(',')
        else:
            print "Channels not changed" 
        print

        days = tv_grab_config_obj.get('days', 7)
        tv_grab_config_obj['days'] = days
        print "Currently configured number of days: " + str(days)
        days = raw_input("Enter for how many days EPG should be grabbed or Enter to leave unchanged: ")
        if len(days.strip()) > 0:
            tv_grab_config_obj['days'] = days.strip()
        else:
            print "Number of days not changed" 
        print

        # set default values for not yet set options
        if not tv_grab_config_obj.has_key('split-title'):
            tv_grab_config_obj['split-title'] = False 
        
        if not tv_grab_config_obj.has_key('add-original-title-to-title'):
            tv_grab_config_obj['add-original-title-to-title'] = False 
        
        if not tv_grab_config_obj.has_key('add-year-to-title'):
            tv_grab_config_obj['add-year-to-title'] = False
        
        if not tv_grab_config_obj.has_key('add-age-rating-to-title'):
            tv_grab_config_obj['add-age-rating-to-title'] = False
        
        if not tv_grab_config_obj.has_key('log-level'):
            tv_grab_config_obj['log-level'] = logging.INFO

        # write configuration to file (create directory if needed)
        directory = os.path.dirname(self.tv_grab_options.config_file)
        if not os.path.exists(directory):
            os.makedirs(directory)
           
        tv_grab_config_obj.write()
        print "Configuration file written to " + self.tv_grab_options.config_file

        return 0

    def get_logfile(self):
        if self.tv_grab_options.logfile:
            return self.tv_grab_options.logfile
        else:
            today = datetime.date.today()
            previousMonth =  today - datetime.timedelta(days=31)
            previousMonthSubDir = previousMonth.strftime("%Y-%m")
            log_dir_to_remove = os.path.join(os.path.normpath(os.path.expanduser("~/.epguide/log")), previousMonthSubDir)
            if os.path.exists(log_dir_to_remove):
                try:
                    shutil.rmtree(log_dir_to_remove)
                except Exception, e:
                    print e
            else:
                pass
                
            thisMonthSubDir = today.strftime("%Y-%m")
            default_log_filename = "tv_grab_pl_epguide-" + today.strftime('%Y%m%d-%H%M%S')+".log"
            default_log_path = os.path.join(os.path.join("~/.epguide/log", thisMonthSubDir), default_log_filename)
            path = normpath(expanduser(self.tv_grab_config_obj.get('logfile', default_log_path)))
            directory = os.path.dirname(path)
            if not os.path.exists(directory):
                os.makedirs(directory)
            return path 
        
    def get_log_level(self):
        if self.tv_grab_options.log_level:
            return self.tv_grab_options.log_level
        else:
            return self.tv_grab_config_obj.get('log_level', logging.INFO) 

    def get_days(self):
        if self.tv_grab_options.days:
            return self.tv_grab_options.days
        else:
            return self.tv_grab_config_obj.get('days', 7) 
        
        
    def normal_run(self):
        epguide_config = Config()
        epguide_config.options = Values(epguide_config.cmdparser.defaults)
        epguide_config.options.output = "xmltv"
        epguide_config.options.filename = self.tv_grab_options.output

        self.tv_grab_config_obj = ConfigObj(self.tv_grab_options.config_file)
        
        epguide_config.options.logfile = self.get_logfile()
        epguide_config.options.log_level = self.get_log_level()

        if epguide_config.options.logfile:
            directory = os.path.dirname(epguide_config.options.logfile)
            if not os.path.exists(directory):
                os.makedirs(directory)            
            root_logger= logging.getLogger()
            root_logger.setLevel(epguide_config.options.log_level)
            handler = logging.FileHandler(epguide_config.options.logfile, 'w', 'utf-8')
            handler.setFormatter = logging.Formatter(logging.BASIC_FORMAT, None) 
            root_logger.addHandler(handler)
        else:
            logging.basicConfig()

        self.log = logging.getLogger("tv_grab_pl_epguide")
        self.log.info("Starting tv_grab_pl_epguide")

        channels = self.tv_grab_config_obj.get('channels', None)
        if not channels:
            print "No channels found in configuration file. Please run with --configure option first."
            return -1
        else:
            if isinstance(channels, basestring): #jeden kanal to String a nie List
                epguide_config.options.channel_list = [channels]
            else:
                epguide_config.options.channel_list = channels
            self.log.info("channels:" + str(epguide_config.options.channel_list))
            
            epguide_config.options.get_days = self.get_days()
            self.log.info("days:" + epguide_config.options.get_days)

            epguide_config.options.split_title = self.tv_grab_config_obj['split-title']
            self.log.info("split_title:" + epguide_config.options.split_title)

            epguide_config.options.add_original_title_to_title = self.tv_grab_config_obj['add-original-title-to-title']
            self.log.info("add_original_title_to_title:" + epguide_config.options.add_original_title_to_title)

            epguide_config.options.add_year_to_title = self.tv_grab_config_obj['add-year-to-title']
            self.log.info("add_year_to_title:" + epguide_config.options.add_year_to_title)

            epguide_config.options.add_age_rating_to_title = self.tv_grab_config_obj['add-age-rating-to-title']
            self.log.info("add_age_rating_to_title:" + epguide_config.options.add_age_rating_to_title)
            
            epguide_config.default_parser = 'teleman'
            
            epguide_config.parser = {}
            epguide_config.parser['teleman'] = TelemanParser.TelemanParser(epguide_config.options, False)
            epguide_config.parser['gazeta'] = GazetaParser.GazetaParser(epguide_config.options, False)

            epguide_config.output = FileOutput.FileOutput(epguide_config.options.filename, XmltvOutput.XmltvOutput())
            
            epguide_config.date_from = datetime.datetime.today()
            self.log.info("date_from:" + str(epguide_config.date_from))

            epguide_config.date_to = datetime.datetime.today() + datetime.timedelta(days=int(epguide_config.options.get_days))
            self.log.info("date_to:" + str(epguide_config.date_to))
            
            epguide_config.get_guide = True

            self.setup(epguide_config)
            self.get_guide()
            return 0

    def run(self):
        self.tv_grab_options, self.args = self.cmdparser.parse_args(sys.argv)

        if (self.tv_grab_options.description):
            return self.print_description()
        elif (self.tv_grab_options.capabilities):
            return self.print_capabilities()
        elif (self.tv_grab_options.configure):
            return self.configure()
        else:
            return self.normal_run()


def RunTvGrabPlEpguide():
    grabber = TvGrabPlEpguide()
    return grabber.run()

if __name__ == '__main__':
    RunTvGrabPlEpguide()
    