#!/usr/bin/python

import time
import datetime
from optparse import OptionParser, Option, OptionValueError
from copy import copy

from parsers import TelemanParser 
from formatters import TxtOutput, XmltvOutput, FileOutput
from optparse import OptionParser, Option, OptionValueError, Values

def CheckDate (dummy, opt, value):
    try:
        return datetime.datetime.fromtimestamp(time.mktime(time.strptime(value, '%Y-%m-%d')))
    except:
        raise OptionValueError("option %s: invalid date value: %r" % (opt, value))


class AdditionalOptions(Option):
    """
    dodatkowe opcje dla parsera linii komend
    """    
    TYPES = Option.TYPES + ("date",)
    TYPE_CHECKER = copy(Option.TYPE_CHECKER)
    TYPE_CHECKER["date"] = CheckDate
             
class Config(object):
    """
    klasa konfiguracji aplikacji
    """
    def __init__(self):
        self.options = None
        self.args = None
        self.parser = None
        self.output = None
        self.get_guide = False
        self.get_today = False
        self.get_days = 0
        self.usage=""" Application, that can get You electronic TV guide in various formats
                       %prog [options] """

        
        self.cmdparser = OptionParser(usage=self.usage, option_class=AdditionalOptions)
        self.cmdparser.add_option ("-l", dest="list", action="store_true", default=False, help="list all channels and their numbers")        
        self.cmdparser.add_option ("-c", dest="channel_list",  help="input channel list (index from -l command) comma separated")
        self.cmdparser.add_option ("-d", type="date", dest="date", help="date you want the program from (format: YYYY-MM-DD)")
        self.cmdparser.add_option ("-f", dest="output", choices=["txt","xmltv"], default="txt", help="guide output format xmltv or txt")
        self.cmdparser.add_option ("-o", dest="filename",  help="store results to file (default to stdout)")
        self.cmdparser.add_option ("-p", dest="parser", choices=["teleman"], default="teleman", help="channel parser source from: teleman")
        self.cmdparser.add_option ("-t", dest="get_today", action="store_true", default=False, help="get guide for today")
        self.cmdparser.add_option ("-w", dest="get_week", action="store_true", default=False, help="get guide for whole week from today")
        self.cmdparser.add_option ("--days", dest="get_days", help="get guide for provided days from today")
        self.cmdparser.add_option ("--config", dest="use_config", help="use provided config")
        self.cmdparser.add_option ("--logfile", dest="logfile", help="log to specified file")
        self.cmdparser.add_option ("--licence", dest="licence", action="store_true", default=False, help="print licence")
        self.cmdparser.add_option ("--verbose", dest="verbose", action="store_true", default=False, help="verbose logging")
        self.cmdparser.add_option ("--split-title", dest="split_title", action="store_true", default=False, help="split title into title, subtitle and episode num (if possible)")
        self.cmdparser.add_option ("--add-original-title-to-title", action="store_true", dest="add_original_title_to_title", default=False, help="add original title to title")
        self.cmdparser.add_option ("--add-year-to-title", action="store_true",dest="add_year_to_title", default=False, help="add year to title")
        self.cmdparser.add_option ("--add-age-rating-to-title", type="int", dest="add_age_rating_to_title", default=100, help="add info about age rating to title (if age rating greater or equal than given)")
        self.cmdparser.add_option ("--debug-http", dest="debug_http", action="store_true", default=False, help="enable logs for http connection")


    def setDefaults(self):
        self.options = Values(epguide_config.cmdparser.defaults)
        self.parser = TelemanParser.TelemanParser(self.options, self.options.debug_http)
        self.output = FileOutput.FileOutput(self.options.filename, TxtOutput.TxtOutput())

    def ParseCommandLine(self, argv):
        """
        przetworzenie linii komend
        """
        self.options, self.args = self.cmdparser.parse_args(argv)

        # separacja listy kanalow
        if self.options.channel_list:
            self.options.channel_list = self.options.channel_list.split(',')

        # tworzenie parsera
        if self.options.parser == 'teleman':
            self.parser = TelemanParser.TelemanParser(self.options, self.options.debug_http)

        # tworzenie wyjscia
        if self.options.output == 'txt':
            self.output = FileOutput.FileOutput(self.options.filename, TxtOutput.TxtOutput())
        elif self.options.output == 'xmltv':
            self.output = FileOutput.FileOutput(self.options.filename, XmltvOutput.XmltvOutput())
        
        # daty poczatkowe i koncowe 
        if self.options.get_week == True:
            self.date_from = datetime.datetime.today()
            self.date_to = datetime.datetime.today() + datetime.timedelta(days=7)
            self.get_guide = True
        elif self.options.get_today == True:
            self.date_from = datetime.datetime.today()
            self.date_to = datetime.datetime.today() + datetime.timedelta(days=1)
            self.get_guide = True
        elif self.options.date is not None:
            self.date_from = self.options.date
            self.date_to = self.options.date + datetime.timedelta(days=1)
            self.get_guide = True
        elif self.options.get_days is not None:
            self.date_from = datetime.datetime.today()
            self.date_to = datetime.datetime.today() + datetime.timedelta(days=int(self.options.get_days))
            self.get_guide = True
            
        
    def ReadConfigFile(self):
        """
        odczytanie pliku konfiguracji
        """
        raise NotImplementedError
    
    def ProvideExec(self):
        """
        dostarczenie obiektow parsera i wyjscia
        """
        return self.parser, self.output
        
    
    
