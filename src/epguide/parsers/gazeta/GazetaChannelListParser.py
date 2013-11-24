# -*- coding: utf-8 -*-
from epguide.parsers.AbstractParser import AbstractParser
from epguide.data_formats import Channel
from lxml import etree
import StringIO
import logging
import re
 
class GazetaChannelListParser(AbstractParser):
    """
    dostarcza informacji o liscie obslugiwanych stacji przez gazeta.pl 
    """
    def __init__(self):
        AbstractParser.__init__ (self, None)
        self.success = False
        self.log = logging.getLogger(__name__)

    def get_channels(self, buf):
        """
        parsuje stronę, zwraca liste elementow klasy Channel
        """
        parser = etree.HTMLParser()
        tree = etree.parse(StringIO.StringIO(buf), parser)
                
        channel_elements = tree.xpath(".//li[starts-with(@class,'station')]")       
        channel_list = [self._create_channel(channel_element) for channel_element in channel_elements]        

        return channel_list
    
    def _create_channel(self, channel_element):
        """
        tworzy z elementu HTML obiekt kanalu
        """
# <li class="station station[431]">
#     <a href="0,110298,8700474,,,,,431,Polsat News.html">
#         <span>
#             Polsat News
#         </span>
#     </a>
#     <small class="favorite"></small> 
# </li>
        m = re.search('station station\[(\d{1,3})\]', channel_element.get("class"))
        prog_id = m.group(1) 
        name = self.get_texts(channel_element, './/span')
        
        return Channel(prog_id, name, None)