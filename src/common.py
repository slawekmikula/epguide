#!/usr/bin/python
#
# License: GPL
# Some common routines for TV program guide parsers

import datetime
from optparse import OptionParser, Option, OptionValueError
from copy import copy
from parser_wp import WpParser
from parser_cp import CpParser
from output_txt import TxtOutput
from output_xmltv import XmltvOutput

class AdditionalOptions(Option):
    """
    dodatkowe opcje dla parsera linii komend
    """
    def check_date (option, opt, value):
      try:
        return datetime.time.strptime (value, "%Y-%m-%d")
      except:
        raise OptionValueError("option %s: invalid date value: %r" % (opt, value))
    
    TYPES = Option.TYPES + ("date",)
    TYPE_CHECKER = copy(Option.TYPE_CHECKER)
    TYPE_CHECKER["date"] = check_date
    
usage="""
 Application, that can get You electronic TV guide in various formats
 
 %prog [options] """
         
class Config:
    """
    klasa konfiguracji aplikacji
    """
    def __init__(self):
        self.options = None
        self.args = None
        self.parser = None
        self.output = None
        self.get_guide = False
        
        self.cmdparser = OptionParser(usage=usage, option_class=AdditionalOptions)
        self.cmdparser.add_option ("-d", type="date", dest="date", help="date you want the program from (format: YYYY-MM-DD)")
        self.cmdparser.add_option ("-f", dest="output", choices=["txt","xmltv"], default="txt", help="guide output format")
        self.cmdparser.add_option ("-p", dest="parser", choices=["wp","cplus"], default="wp", help="channel parser source")
        self.cmdparser.add_option ("-l", dest="list", action="store_true", default=False, help="list all channels and their numbers")
        self.cmdparser.add_option ("-o", dest="filename",  help="store results to file (default to stdout)")
        self.cmdparser.add_option ("-c", dest="channel_list",  help="input channel list (numbers comma separated)")
        self.cmdparser.add_option ("-w", dest="get_week", action="store_true", default=False, help="get guide for whole week from today")
        self.cmdparser.add_option ("--config", dest="use_config", help="use provided config")
        self.cmdparser.add_option ("--licence", dest="licence", action="store_true", default=False, help="print licence")
        
         
    def ParseCommandLine(self, argv):
        """
        przetworzenie linii komend
        """
        self.options, self.args = self.cmdparser.parse_args(argv)
       
        # tworzenie parsera
        if self.options.parser == 'wp':
            self.parser = WpParser()
        elif self.options.parser == 'cplus':
            self.parser = CpParser()
       
        # tworzenie wyjscia
        if self.options.output == 'txt':
            self.output = TxtOutput()
        elif self.options.parser == 'xmltv':
            self.output = XmltvOutput()
        
        # daty poczatkowe i koncowe 
        if self.options.get_week == True:
            self.date_from = datetime.date.today()
            self.date_to = datetime.date.today() + datetime.timedelta(days=7)
            self.get_guide = True
        elif self.options.date is not None:
            self.date_from = self.options.date
            self.date_to = self.options.date
            self.get_guide = True
            print self.options.date
        
    def ReadConfigFile(self):
        """
        odczytanie pliku konfiguracji
        """
        # FIXME - odczytaj konfiguracje z pliku 
        raise NotImplementedError
    
    def ProvideExec(self):
        """
        dostarczenie obiektow parsera i wyjscia
        """
        return self.parser, self.output
        
    def PrintHelp(self):
        """
        wyswietlenie pomocy
        """
        print self.cmdparser.Help()
        
    def PrintLicence(self):
        """
        wyswietlenie licencji
        """
        raise NotImplementedError
    
    