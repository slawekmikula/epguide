# -*- coding: utf-8 -*-
from lxml import etree
import StringIO
import re
from epguide.data_formats import ParentalRating
from epguide.parsers.gazeta.GazetaData import GazetaEventDetails
from epguide.parsers.AbstractParser import AbstractParser
 
class GazetaProgrammeDetailsParser(AbstractParser):
                    
    def get_details(self, buf):
        """
        parsuje stronę szczegolow, zwraca element GazetaEventDetails
        """

        parser = etree.HTMLParser()
        tree = etree.parse(StringIO.StringIO(buf), parser)

        primary_title = self.get_texts(tree, "//div[@class='head']/h1/span")      
        description = "\nOpis: " + self.get_texts(tree, "//div[@class='content']/div[@class='txt']/p") 
        
        ycgd = self.get_texts(tree, "//div[@class='head']/small").split(',')
        if (len(ycgd) == 4):
            genre = ycgd[0].strip()
            country = ycgd[1].strip()
            year = ycgd[2].strip()
            duration = ycgd[3].strip()
        else:
            genre = ""
            country = ""
            year = ""
            duration = ""
        
        photo_url = self.get_attr(tree, "//div[@class='body']/div[@class='im']/img", "src")
        pg_desc = self.get_attr(tree, "//div[@class='head']/h1", "class")
        if pg_desc is None:
            min_age = 0
        else:
            ageregexp = re.compile('od(\d*)',re.DOTALL)
            m = ageregexp.search(pg_desc)
            if m is None: 
                min_age = 0
            else:
                if m.group(1) is None:
                    min_age = 0
                else:
                    min_age = int(m.group(1))

        pg = ParentalRating(pg_desc, min_age)                
        
        # FIXME - do wykorzystania pozniej
        crew_titles = tree.xpath("//div[@class='content']/dl/dt")
        crew_content =  tree.xpath("//div[@class='content']/dl/dd")        
        crew = dict(zip(crew_titles,crew_content))
        
        return GazetaEventDetails(primary_title, description, year, country, genre, duration, photo_url, pg, crew)
    
