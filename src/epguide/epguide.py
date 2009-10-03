import datetime
import sys

licence = '''
 EpGuide - Application, that can get You electronic TV guide in various formats
 Copyright (C) 2009 Slawek Mikula <slawek.mikula@gmail.com>

 This program is free software; you can redistribute it and/or
 modify it under the terms of the GNU General Public License
 as published by the Free Software Foundation; either version 2
 of the License, or (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program; if not, write to the Free Software
 Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
'''

authors = '''
Slawek Mikula <slawek.mikula@gmail.com>

'''

class EpGuide(object):
    """
    glowna klasa aplikacji
    """
    def __init__(self, config):
        
        self.config = config
        self.parser, self.output = self.config.ProvideExec()
        
    def Execute(self):
        """
        glowna petla wykonywania zadan
        """
        if self.config.options.licence:
            self.PrintLicence()
        elif self.config.options.list:
            self.GetChannelList()
        elif self.config.get_guide: 
            self.GetGuide()
        else:    
            self.PrintHelp()

    def GetChannelList(self):
        """
        pobiera liste kanalow
        """
        
        self.parser.Init()
        self.output.Init()
        channel_list = self.parser.GetChannelList()
        self.output.SaveChannelList(channel_list)
        self.parser.Finish()
        self.output.Finish()        
    
    def GetGuide(self):
        """
        pobiera dane programu telewizyjnego
        """

        if self.config.options.channel_list is None or len(self.config.options.channel_list) == 0:
            print "Brak wybranej listy kanalow - opcja -c !"
            sys.exit()

        self.parser.Init()
        self.output.Init()

        day = self.config.date_from
        for iter in range((self.config.date_to - self.config.date_from).days):
            
            for channel in self.config.options.channel_list:
                guide = self.parser.GetGuide(day, channel)
                self.output.SaveGuide(day, guide)
                
            day += datetime.timedelta(days=1)

        self.output.SaveGuideChannels()
        self.output.Finish()
        self.parser.Finish()
    
    def PrintHelp(self):
        """
        wyswietlenie pomocy
        """
        print self.config.cmdparser.print_help()

    def PrintLicence(self):
        """
        wyswietlenie licencji
        """
        print licence
