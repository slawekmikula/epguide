# -*- coding: utf-8 -*-
from epguide.data_formats import Imdb, ParentalRating
from lxml import etree
import StringIO
import re
import logging
from epguide.parsers.teleman.TelemanData import TelemanEventDetails

class AbstractTelemanParser(object):
    def __init__(self, dummy):
        self.build_text_list = etree.XPath("//text()")
        self.log = logging.getLogger(__name__)
    
    def get_texts(self, tree, path):
        description_elements = tree.xpath(path, smart_strings=False)
        #print(description_elements)
        if(not description_elements):
            text = ""
        else:
            text = etree.tostring(description_elements[0], method="text", encoding=unicode)
        #print(text)        
        return text.strip()
                    
    def get_attr(self, tree, path, attr_name):
        description_elements = tree.xpath(path, smart_strings=False)
        #print(description_elements)
        if(not description_elements):
            text = ""
        else:
            text = description_elements[0].get(attr_name)
        #print(text)        
        return text.strip()
                    
