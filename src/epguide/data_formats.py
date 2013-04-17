# -*- coding: utf-8 -*-
# 
# plik definiujacy obiekty przechowujace dane

class Channel(object):
    """
    definicja kanalu
    """
    def __init__(self, name="", id="", icon_url=None):
        self.name = name
        self.id = id
        self.icon_url = icon_url

    def __hash__(self):
        return hash(self.id)

    def __cmp__(self, other):
        return cmp(self.id, other.id)
    
    def __str__(self):
        return "Channel(id:'" + self.id + "',name:'" + self.name +  "',icon_url:'" + self.icon_url+ "')"

class Event(object):
    """
    wydarzenie (program w telewizji), zawiera dane zakodowane w unicode
    """
    def __init__(self, channel_id, channel_name, channel_icon_url, title, subtitle, main_category, category,
        desc, time_start, time_end=None, episode_num=None, url=None, details=None):
            
        self.channel_id = channel_id
        self.channel_name = channel_name
        self.channel_icon_url = channel_icon_url
        self.title = title
        self.subtitle = subtitle
        self.episode_num = episode_num
        self.main_category = main_category
        self.category = category
        self.desc = desc
        self.time_start = time_start
        self.time_end = time_end
        self.url = url
        self.details = details
    
    def __hash__(self):
        return self.channel_id + self.time_start

    def __cmp__(self, other):
        return (self.channel_id + self.time_start) - (other.channel_id + other.time_start)

    def __str__(self):
        return "Event(channel_id:'" + self.channel_id + "', channel_name:'" + self.channel_name+ "', channel_icon_url:'" + self.channel_icon_url + "', time_start:'" + str(self.time_start) + \
        "', time_end:'" + str(self.time_end) + "', title:'" + self.title + "', subtitle:'" + self.subtitle + "', episode_num:'" + self.episode_num + \
        "', main_category:'" + self.main_category + "', category:'" + self.category + "', url:'" + self.url + "', desc:'" + self.desc.replace("\n", "\\n") + \
        "', details:'" + str(self.details) + \
        "')" 
    
    def set_details(self, details):
        self.details = details
        
    def get_title(self):
        if(self.details is None):
            return self.title
        elif(self.details.pg is None):
            return self.title
        elif(self.details.pg.min_age >= 16):
            return str(self.details.pg.min_age)+" "+self.title
        else:
            return self.title
                
    def get_description(self):
        if(self.details is None):
            d = self.desc
        else:
            d = self.desc + u"\nOpis:\n" + self.details.description + u"\nTytul oryginalny:" + self.details.original_title
        return d

    def get_year(self):
        if(self.details is None):
            d = None
        else:
            d = self.details.year
        return d

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

class EventDetails(object):
    """
    szczegóły wydarzenia (program w telewizji), zawiera dane zakodowane w unicode
    """
    def __init__(self, description, original_title, year, country, genre, imdb, filmweb, photo_url, pg):
        self.description = description
        self.original_title = original_title
        self.year = year
        self.country = country
        self.genre = genre
        self.imdb = imdb
        self.filmweb = filmweb
        self.photo_url = photo_url
        self.pg = pg
            

    def __str__(self):
        return "EventDetails(description:'" + self.description + "',original_title:'" + self.original_title + "',year:'" + self.year + \
            "',country:'" + self.country + "',genre:'" + self.genre + "',imdb:'" + str(self.imdb) + \
             "',filmweb:'" + str(self.filmweb) + "',photo_url:'" + self.photo_url + "',pg:'" + str(self.pg) + "')" 

class Imdb(object):
    def __init__(self, url, rank):
        self.url = url
        self.rank = rank
        
    def __str__(self):
        return "Imdb(url:'" + self.url + "',rank:'" + self.rank + ")" 

class ParentalRating(object):
    def __init__(self, desc, min_age):
        self.desc = desc
        self.min_age = min_age
        
    def __str__(self):
        return "ParentalRating(desc:'" + self.desc+ "',min_age:" + str(self.min_age) + ")" 
