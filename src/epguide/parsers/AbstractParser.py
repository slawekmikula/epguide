# -*- coding: utf-8 -*-
from lxml import etree
import logging

class AbstractParser(object):
    def __init__(self, dummy):
        self.build_text_list = etree.XPath("//text()")
        self.log = logging.getLogger(__name__)
    
    def get_texts(self, tree, path):
        description_elements = tree.xpath(path, smart_strings=False)

        if(not description_elements):
            text = ""
        else:
            text = etree.tostring(description_elements[0], method="text", encoding=unicode)
        
        return text.strip()
                    
    def get_attr(self, tree, path, attr_name):
        description_elements = tree.xpath(path, smart_strings=False)

        if(not description_elements):
            text = ""
        else:
            text = description_elements[0].get(attr_name)
        
        if text is None:
            return ""
        else:        
            return text.strip()
                    
