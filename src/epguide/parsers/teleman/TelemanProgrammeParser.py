# -*- coding: utf-8 -*-
from epguide.parsers.AbstractParser import AbstractParser
from epguide.data_formats import Channel
from epguide.parsers.teleman.TelemanData import TelemanEvent
from lxml import etree
import StringIO
import datetime
import logging
import time
 
class TelemanProgrammeParser(AbstractParser):
    def __init__(self, parser_options):
        AbstractParser.__init__ (self, parser_options)
        self.parser_options = parser_options
        self.category_classes_to_main_category = {'cat-roz':"Leisure hobbies", 'cat-ser':"Show/Game show", 'cat-fil':"Movie/Drama", 'cat-xxx':"News/Current affairs", 'cat-dzi':"Children's/Youth programmes", "cat-spo":"Sports"}
        self.success = False
        self.log = logging.getLogger(__name__)

    def get_events(self, event_date, channel_id, buf):
        """
        parsuje stronę, zwraca liste elementow
        klasy Event
        """

        parser = etree.HTMLParser()
        tree = etree.parse(StringIO.StringIO(buf), parser)
        channel_name = self.get_texts(tree, '//*[@class="stationTitle"]/h1')
        channel_icon_url = self.get_attr(tree, '//*[@class="stationTitle"]/img', "src")
        programmeElements = tree.xpath('//*[@id="stationItems"]/li')

        channel = Channel(channel_id, channel_name, channel_icon_url)

        events = [self.create_event(event_element, channel, event_date) for event_element in programmeElements]

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
#<li class="cat-ser with-photo" id="prog7532796">
#  <a href="/tv/Faceci-Do-Wziecia-Szkola-Rodzenia-41-988883">
#    <img width="100" height="63" class="photo" alt="zdjęcie" src="http://media.teleman.pl/photos/crop-100x63/Faceci-Do-Wziecia.jpeg">
#  </a>
#  <em>6:00</em>
#  <div class="detail">
#    <a href="/tv/Faceci-Do-Wziecia-Szkola-Rodzenia-41-988883">Faceci do wzięcia: Szkoła rodzenia (41)</a>
#    <p class="genre">serial komediowy</p>
#    <p>Dziennikarz Wiktor jest bałaganiarzem. Fotograf Roman to klasyczny pedant. Obaj, porzuceni przez żony, zamieszkują w jednym mieszkaniu.</p>
#  </div>
#</li>
        prog_id = event_element.get("id")
        if prog_id:
            title = self.get_texts(event_element, 'div[@class="detail"]/a')
            self.log.debug("  title: '" + title + "'")
            url = self.get_attr(event_element, 'div[@class="detail"]/a', "href")
    
            time_start_string = self.get_texts(event_element, 'em')
            datetime_start_string = "%s %s" % (event_date.strftime("%Y-%m-%d"), time_start_string)
            time_start_struct = time.strptime(datetime_start_string, '%Y-%m-%d %H:%M')
            time_start = datetime.datetime.fromtimestamp(time.mktime(time_start_struct))
    
            time_end = time_start #TODO
            category = self.get_texts(event_element, 'div[@class="detail"]/p[@class="genre"]')
            summary = self.get_texts(event_element, 'div[@class="detail"]/p[@class="genre"]')
            #http://media.teleman.pl/photos/crop-100x63/Barwy-Szczescia_1.jpeg
            photo_url = self.get_attr(event_element, 'a/img', "src")
            #http://media.teleman.pl/photos/470x265/Barwy-Szczescia_1.jpeg
            photo_url = photo_url.replace("crop-100x63", "470x265")
            
            class_attrs = event_element.get("class").split()
            main_category_class = next((c for c in class_attrs if c.startswith("cat-")), None)
            main_category = self.category_classes_to_main_category.get(main_category_class, "")
            self.log.debug("main_category_class:" + main_category_class + " main_category:" + main_category)
    
            self.log.debug("event_element: " + str(channel) + " " + str(time_start) 
                + " " + str(time_end) + " " + title
                + " " + " " + main_category + " " + category + " " + url)
            event = TelemanEvent(
                               self.parser_options,
                               channel,
                               title,
                               main_category,
                               category,
                               summary,
                               time_start,
                               time_end,
                               url,
                               None,
                               photo_url,
                               prog_id)
    
    
            return event
        else:
            return None

