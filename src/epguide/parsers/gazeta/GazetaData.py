# -*- coding: utf-8 -*-
# 
# plik definiujacy obiekty przechowujace dane wychodzące z GazetaParser
import re
import logging
from epguide.util import to_string
from epguide.data_formats import Event

class GazetaEvent(Event):
    """
    wydarzenie (program w telewizji), zawiera dane zakodowane w unicode
    """
    def __init__(self, parser_options, channel, title, main_category, category,
        desc, time_start, time_end=None, url=None, prog_id=None):

        self.episode_regexp = re.compile(r'(?P<title>.+)\((?P<odc>.+)\)')
        self.subtitle_regexp = re.compile(r'(?P<title>.+):(?P<subtitle>.+)')
        self.secondary_title_regexp = re.compile(r'(odc.)?(?P<odc>.+):(?P<subtitle>.+)')
        self.log = logging.getLogger(__name__)

        # from summary
        self.parser_options = parser_options        
        self.channel = channel
        self._title = title
        self.main_category = main_category
        self.category = category
        self.desc = desc
        self.time_start = time_start
        self.time_end = time_end
        self.url = url
        self.prog_id = prog_id
        
        # from details
        self.calculated_title = title
        self.calculated_subtitle = None
        self.calculated_episode_num = None
        self.calculated_description = desc
        
        self.details = None
        self.icon_url = None
        
        self._recalculate()
    
        
    def get_channel_id(self):
        return self.channel.id

    def get_channel_name(self):
        return self.channel.name

    def get_channel_icon_url(self):
        return None

    def get_title(self):
        return self.calculated_title

    def get_subtitle(self):
        return self.calculated_subtitle

    def get_episode_num(self):
        return self.calculated_episode_num

    def get_filename(self):
        result = self.get_title() 
        if self.get_episode_num():
            result = result + " (" + self.get_episode_num()+")"
        if self.get_subtitle():
            result = result + " " + self.get_subtitle()
        return result

    def __hash__(self):
        return self.channel.channel_id + str(self.time_start)

    def __cmp__(self, other):
        return (self.get_channel_id() + str(self.time_start)) - (other.get_channel_id() + str(other.time_start))

    def __str__(self):
        return "GazetaEvent(channel_id:" + to_string(self.get_channel_id()) + \
            ", channel_name:" + to_string(self.get_channel_name()) + \
             ", time_start:" + to_string(self.time_start) + \
             ", time_end:" + to_string(self.time_end) + \
             ", title:" + to_string(self.get_title()) + \
             ", subtitle:" + to_string(self.get_subtitle()) + \
             ", episode_num:" + to_string(self.get_episode_num()) + \
            ", category:" + to_string(self.category) + \
            ", url:" + to_string(self.url) + \
            ", desc:" + to_string(self.desc.replace("\n", "\\n")) + \
            ", details:" + to_string(self.details) + \
        ")" 
    
    def set_details(self, details):
        self.details = details
        self._recalculate()

    def _recalculate(self):
        additional_title = None
        if self.parser_options.split_title: 
            if self.details is not None:
                if self.details.secondary_title is None or len(self.details.secondary_title.strip()) == 0:
                    episode_match = self.episode_regexp.match(self.details.primary_title)
                    if episode_match is None:
                        # brak szczegółów i nie znaleziono numeru odcinka
                        self.log.debug("  #episode not found")
                        self.calculated_title = self.details.primary_title
                        self.calculated_episode_num = None
                        self.calculated_subtitle = None
                    else:
                        # brak szczegółów i znaleziono numer odcinka
                        self.log.debug("  #title: '" + episode_match.group('title') + "'")
                        self.log.debug("  #episode: '" + episode_match.group('odc') + "'")
                        self.calculated_title = episode_match.group('title').strip()
                        self.calculated_episode_num = episode_match.group('odc').strip()
            
                        subtitle_match = self.subtitle_regexp.match(self.calculated_title)
                        if subtitle_match is None:
                            self.log.debug("  #subtitle not found")
                            self.calculated_subtitle = None
                        else:
                            self.log.debug("  #title: '" + subtitle_match.group('title') + "'")
                            self.log.debug("  #subtitle: '" + subtitle_match.group('subtitle') + "'")
                            self.calculated_title = subtitle_match.group('title').strip()
                            self.calculated_subtitle = subtitle_match.group('subtitle').strip()
                else:
                    episode_match = self.secondary_title_regexp.match(self.details.secondary_title)
                    if episode_match is None:
                        self.log.debug("  #episode not found")
                        self.calculated_title = self.details.primary_title
                        self.calculated_episode_num = None
                        self.calculated_subtitle = self.details.secondary_title
                    else:
                        self.calculated_title = self.details.primary_title
                        self.calculated_subtitle = episode_match.group('subtitle').strip()
                        self.calculated_episode_num = episode_match.group('odc').strip()
                        
                pos = self._title.find(self.details.primary_title)
                if pos > 0:
                    serie =  self._title[:pos].strip(" :")
                    additional_title = serie
        else:
                self.calculated_title = self._title
                self.calculated_subtitle = None
                self.calculated_episode_num = None

        if(self.details is None):
            self.calculated_description = self.desc
        else:

            # dodawaj rok tylko dla filmów, dla seriali pomijamy, żeby nie było kolizji z numerem odcinka
            self.calculated_title = self._add_year(self.calculated_title, self.parser_options.add_year_to_title)
            self.calculated_title = self._add_age_rating(self.calculated_title, self.parser_options.add_age_rating_to_title)
            self.calculated_description = self.desc + self.details.description 

    def _add_year(self, base_title, add_year_to_title):
        if(self.details is None):
            return base_title
        elif(self.details.year is None or len(self.details.year.strip()) == 0):
            return base_title
        elif(add_year_to_title):
            return base_title + " (" + self.details.year + ")"
        else:
            return base_title
                
    def _add_age_rating(self, base_title, add_age_rating_to_title):
        if(self.details is None):
            return base_title
        elif(self.details.pg is None):
            return base_title
        elif(self.details.pg.min_age >= add_age_rating_to_title):
            return base_title + " [od " + str(self.details.pg.min_age) + " lat]"
        else:
            return base_title

    def get_description(self):
        return self.calculated_description

    def get_year(self):
        if(self.details is None):
            d = None
        else:
            d = self.details.year
        return d

    def get_icon_url(self):
        return self.icon_url

    def get_country(self):
        if(self.details is None):
            d = None
        else:
            d = self.details.country
        return d

    def get_pg(self):
        if(self.details is None):
            d = None
        elif(self.details.pg is None):
            d = None
        else:
            d = str(self.details.pg.min_age)
        return d

    def get_star_rating(self):
        return None

class GazetaEventDetails(object):
    """
    szczegóły wydarzenia (program w telewizji)
    """
    def __init__(self, primary_title, description, year, country, genre, duration, photo_url, pg, crew):
        
        self.primary_title = primary_title
        self.secondary_title = primary_title
        self.description = description
        self.year = year
        self.country = country
        self.genre = genre
        self.duration = duration
        self.photo_url = photo_url
        self.pg = pg            

    def __str__(self):
        return "GazetaEventDetails(primary_title:'" + to_string(self.primary_title) + \
            "',description:'" + to_string(self.description) + \
            "',year:'" + to_string(self.year) + \
            "',country:'" + to_string(self.country) + \
            "',genre:'" + to_string(self.genre) + \
            "',duration:'" + to_string(self.duration) + \
             "',photo_url:'" + to_string(self.photo_url) + \
             "',pg:'" + to_string(self.pg) + "')" 
