# -*- coding: utf-8 -*-
from abstract_epguide import AbstractEpGuide
import logging

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

class EpGuide(AbstractEpGuide):
    """
    glowna klasa aplikacji
    """
    def __init__(self, config):
        AbstractEpGuide.__init__(self)
        
        self.setup(config)

        if self.config.options.logfile:
            logging.basicConfig(filename=self.config.options.logfile,level=logging.DEBUG)
        else:
            logging.basicConfig()
        self.log = logging.getLogger("epguide")
        if self.config.options.verbose or self.config.options.logfile:
            self.log.setLevel(logging.DEBUG)
        else:
            self.log.setLevel(logging.CRITICAL)
        
    def Execute(self):
        """
        glowna petla wykonywania zadan
        """
        if self.config.options.licence:
            self.PrintLicence()
        elif self.config.options.list:
            self.get_channels()
        elif self.config.get_guide: 
            self.get_guide()
        else:    
            self.PrintHelp()

    
    
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
