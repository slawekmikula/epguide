# -*- coding: utf-8 -*-
import datetime
import sys
import logging
import textwrap
'''
Created on 27-10-2013

@author: Damian
'''

class AbstractEpGuide(object):
    '''
    Szkielet aplikacji pobierającej EPG.
    Konkretne implementacje (TvGrabPlEpguide oraz EpGuide) pozwalają na różne sposoby uruchamiania (różny zestaw parametrów).
    '''


    def __init__(self):
        self.log = logging.getLogger(__name__)

    def setup(self, config):
        self.config = config
        self.parser, self.default_parser, self.output = self.config.ProvideExec()

    def get_channels(self):
        """
        pobiera liste kanalow
        """
        self.log.info("Rozpoczęcie pobierania listy kanałów")
        self.log.info("Parser init")
        self.parser[self.default_parser].Init()

        self.log.info("Wyjście init")
        self.output.Init()

        self.log.info("Pobieram listę kanałów")
        channel_list = self.parser[self.default_parser].get_channels()
        
        self.log.info("Zapisuję liste kanałów")
        self.output.SaveChannelList(channel_list)

        self.log.info("Parser zamknięcie")
        self.parser[self.default_parser].Finish()

        self.log.info("Wyjście zamknięcie")
        self.output.Finish()        

    def get_guide(self):
        """
        pobiera dane programu telewizyjnego
        """        
        if self.config.options.channel_list is None or len(self.config.options.channel_list) == 0:
            print "Brak wybranej listy kanalow - opcja -c !"
            sys.exit()
        
        self.log.info(u"Wyjście init")
        self.output.Init()
        
        self.log.info(u"Parsers init")
        for parserItem in self.parser.values():
            parserItem.Init()
        
        day = self.config.date_from
        self.log.info(u"Pobieranie programu od dnia: %s do dnia %s" % (self.config.date_from, self.config.date_to))
        for d in range((self.config.date_to - self.config.date_from).days):
            self.log.info(u"Pobieranie programu dla dnia: %s" % (day))
            for channel in self.config.options.channel_list:
                if '|' in channel:
                    parserName = channel.split('|')[0]
                    channelName = channel.split('|')[1]                    
                else:                    
                    parserName = self.default_parser
                    channelName = channel
                    
                prsr = self.parser[parserName]
                self.log.info(u"Pobieranie programu na dzień %s dla kanału: %s. Parser: %s" % (day, channelName, parserName))
                guide = prsr.get_guide(day, channelName)

                if len(guide) == 0:
                    msg = u"Brak programu dla tego dnia"
                else:
                    msg = u"\nProgram %s na dzień: %s\n" % (guide[0].get_channel_name(), day.strftime("%Y-%m-%d"))
                    msg += "--------------------------------------------\n\n"
                    for item in guide:
                        msg += u" %s %s %s | %s | %s | %s\n" % (item.time_start.strftime("%H:%M"), item.time_end and item.time_end.strftime("%H:%M") or '',
                            item.get_title(), item.get_episode_num() or '', (item.get_subtitle() or ''), item.main_category)
                        msg += textwrap.fill (item.get_description(), 79, initial_indent=13*" ", subsequent_indent=13*" ") + "\n"

                self.log.debug(msg)
                self.log.info(u"Zapisywanie programu")
                self.output.SaveGuide(day, guide)
                
            day += datetime.timedelta(days=1)

        self.log.info(u"Zapisywanie listy kanałów dla listy programów")
        self.output.SaveGuideChannels()

        self.log.info(u"Wyjście zamykanie")
        self.output.Finish()

        self.log.info(u"Parser zamykanie")
        for parserItem in self.parser.values():
            parserItem.Finish()
