#!/usr/bin/python

import time
import datetime
from optparse import OptionParser, Option, OptionValueError
from copy import copy

from parsers import WpParser
from formatters import TxtOutput, XmltvOutput

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
        self.usage=""" Application, that can get You electronic TV guide in various formats
                       %prog [options] """

        
        self.cmdparser = OptionParser(usage=self.usage, option_class=AdditionalOptions)
        self.cmdparser.add_option ("-d", type="date", dest="date", help="date you want the program from (format: YYYY-MM-DD)")
        self.cmdparser.add_option ("-f", dest="output", choices=["txt","xmltv"], default="txt", help="guide output format")
        self.cmdparser.add_option ("-p", dest="parser", choices=["wp"], default="wp", help="channel parser source")
        self.cmdparser.add_option ("-l", dest="list", action="store_true", default=False, help="list all channels and their numbers")
        self.cmdparser.add_option ("-o", dest="filename",  help="store results to file (default to stdout)")
        self.cmdparser.add_option ("-c", dest="channel_list",  help="input channel list (numbers comma separated)")
        self.cmdparser.add_option ("-w", dest="get_week", action="store_true", default=False, help="get guide for whole week from today")
        self.cmdparser.add_option ("--config", dest="use_config", help="use provided config")
        self.cmdparser.add_option ("--licence", dest="licence", action="store_true", default=False, help="print licence")
        self.cmdparser.add_option ("-t", dest="get_today", action="store_true", default=False, help="get guide for today")

    def ParseCommandLine(self, argv):
        """
        przetworzenie linii komend
        """
        self.options, self.args = self.cmdparser.parse_args(argv)

        # separacja listy kanalow
        if self.options.channel_list:
            self.options.channel_list = self.options.channel_list.split(',')

        # tworzenie parsera
        if self.options.parser == 'wp':
            self.parser = WpParser.WpParser()

        # tworzenie wyjscia
        if self.options.output == 'txt':
            self.output = TxtOutput.TxtOutput(self)
        elif self.options.output == 'xmltv':
            self.output = XmltvOutput.XmltvOutput(self)
        
        # daty poczatkowe i koncowe 
        if self.options.get_week == True:
            self.date_from = datetime.date.today()
            self.date_to = datetime.date.today() + datetime.timedelta(days=7)
            self.get_guide = True
        elif self.options.get_today == True:
            self.date_from = datetime.date.today()
            self.date_to = datetime.date.today() + datetime.timedelta(days=1)
            self.get_guide = True
        elif self.options.date is not None:
            self.date_from = self.options.date
            self.date_to = self.options.date + datetime.timedelta(days=1)
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
        
    
    