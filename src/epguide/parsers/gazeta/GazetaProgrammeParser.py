# -*- coding: utf-8 -*-
from epguide.parsers.AbstractParser import AbstractParser
from epguide.data_formats import Channel
from epguide.parsers.gazeta.GazetaData import GazetaEvent
from lxml import etree
import StringIO
import datetime
import logging
import time
import re
 
class GazetaProgrammeParser(AbstractParser):
    def __init__(self, parser_options):
        AbstractParser.__init__ (self, parser_options)
        self.parser_options = parser_options
        self.success = False
        self.category_classes_to_main_category = {'Telenowela':"Soap/Melodrama/Folkloric", 'Magazyn':"Magazines/Reports/Documentary", 
                                                  'Magazyn sportowy':"Magazines/Reports/Documentary", 'Magazyn poradnikowy':"Magazines/Reports/Documentary",
                                                   'Magazyn piłkarski':"Magazines/Reports/Documentary", 'Serial animowany':"Cartoons/Puppets", 
                                                   'Serial dla dzieci':"Children's/Youth Programmes", 'Skoki narciarskie':"Sports", 
                                                   'Program popularnonaukowy':"Education/Science/Factual", 'Rozrywka':"Show/Game Show",
                                                   'Reportaż':"Magazines/Reports/Documentary", 'Magazyn filmowy':"Magazines/Reports/Documentary", 
                                                   'Teleturniej muzyczny':"Show/Game Show", 'Serial obyczajowy':"Soap/Melodrama/Folkloric",
                                                   'Serial dokumentalny':"Magazines/Reports/Documentary", 'Magazyn kulinarny':"Cooking", 'Program publicystyczny':"Social/Political/Economics",
                                                   'Wiadomości':"News Magazine", 'Reality show':'Show/Game Show', 'Pogoda':"News/Weather Report", 
                                                   'Komedia':"Comedy", 'Serial grozy':"Detective/Thriller", 
                                                   'Film obyczajowy':"Movie/Drama", 'Horror':"Science Fiction/Fantasy/Horror", 
                                                   'Przerwa w emisji':"Special Characteristics", 'Kabaret i satyra':"", 'Transmisja':"News Magazine",
                                                   'Aktualności':"News Magazine", 'Program dla dzieci':"Children's/Youth Programmes", 
                                                   'Program redakcji katolickiej dla młodzieży':"Children's/Youth Programmes",
                                                   'Miniserial':"Series", 'Serial sensacyjny': "Movie/Drama", 'Serial kryminalny':"Movie/Drama"}
        
        self.log = logging.getLogger(__name__)

    def get_events(self, event_date, channel_id, buf):
        """
        parsuje stronę, zwraca liste elementow
        klasy Event
        """

        parser = etree.HTMLParser()
        tree = etree.parse(StringIO.StringIO(buf), parser)
        channel_name = self.get_texts(tree, ".//div[starts-with(@class,'station')]/a/span")
        programme_elements = tree.xpath(".//li[starts-with(@id,'program')]")

        channel = Channel(channel_id, channel_name, None)

        events = [self.create_event(event_element, channel, event_date) for event_element in programme_elements]

        updated_events = []
        prev_event = None
        add_days = 0
        for current_event in events:
            if current_event:
                if prev_event is not None:
                    # jesli przekraczamy kolejna dobe, robimy poprawke w dacie
                    if current_event.time_start < prev_event.time_start:
                        add_days = 1
                    current_event.time_start = current_event.time_start + datetime.timedelta(days=add_days)
                    current_event.time_end = current_event.time_start
                    prev_event.time_end = current_event.time_start
        
                updated_events.append(current_event)
                prev_event = current_event

        return updated_events
    
    def create_event(self, event_element, channel, event_date):
# <li class="even" id="program[4705370]">                
#     <div class="time">19:10</div>
#     <div class="desc">
#      <h2><a href="/program_tv/0,110740,8651580,,,4705370,Smerfy.html">Smerfy</a></h2>
#      <p>Serial animowany</p>             
#      <p>Gargamel podsłuchuje w lesie rozmowę Smerfów poszukujących jajek do tortu. Wyczarowuje wielkie jajko, które spełnia życzenia, gdy się go dotknie. Jajko trafia do wioski Smerfów.                 
#     </div>
#     <div class="duration">20 minut</div>    
#     <div class="runtime">20</div>
# </li>
        prog_id = re.search('program\[(\d*)\]', event_element.get("id")).group(1)
        if prog_id:
            title = self.get_texts(event_element, 'div[@class="desc"]/h2/a')
            self.log.debug("  title: '" + title + "'")
            url = self.get_attr(event_element, 'div[@class="desc"]/h2/a', "href")
            time_start_string = self.get_texts(event_element, 'div[@class="time"]')
            datetime_start_string = "%s %s" % (event_date.strftime("%Y-%m-%d"), time_start_string)            
            time_start_struct = time.strptime(datetime_start_string, '%Y-%m-%d %H:%M')
            time_start = datetime.datetime.fromtimestamp(time.mktime(time_start_struct))
    
            time_end = time_start #TODO
            category = self.get_texts(event_element, 'div[@class="desc"]/p[1]')
            summary = self.get_texts(event_element, 'div[@class="desc"]/p[2]')
                
            main_category = self.category_classes_to_main_category.get(category, "")
                
            self.log.debug("event_element: " + str(channel) + " " + str(time_start) 
                + " " + str(time_end) + " " + title
                + " " + " " + category + " " + url)
            event = GazetaEvent(
                               self.parser_options,
                               channel,
                               title,
                               main_category,
                               category,
                               summary,
                               time_start,
                               time_end,
                               url,
                               prog_id)
    
    
            return event
        else:
            return None