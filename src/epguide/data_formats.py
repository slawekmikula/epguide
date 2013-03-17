# -*- coding: utf-8 -*-
# 
# plik definiujacy obiekty przechowujace dane

class Channel(object):
    """
    definicja kanalu
    """
    def __init__(self, name="", id=""):
        self.name = name
        self.id = id

    def __hash__(self):
        return hash(self.id)

    def __cmp__(self, other):
        return cmp(self.id, other.id)
    
    def __str__(self):
        return "Channel(id:'" + self.id + "',name:'" + self.name + "')"

class Event(object):
    """
    wydarzenie (program w telewizji), zawiera dane zakodowane w unicode
    """
    def __init__(self, channel_id, channel_name, title, subtitle, main_category, category,
        desc, time_start, time_end=None, episode_num=None, url=None, details=None):
            
        self.channel_id = channel_id
        self.channel_name = channel_name
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
        return "Event(channel_id:'" + self.channel_id + "', channel_name:'" + self.channel_name + "', time_start:'" + str(self.time_start) + \
        "', time_end:'" + str(self.time_end) + "', title:'" + self.title + "', subtitle:'" + self.subtitle + "', episode_num:'" + self.episode_num + \
        "', main_category:'" + self.main_category + "', category:'" + self.category + "', url:'" + self.url + "', desc:'" + self.desc.replace("\n", "\\n") +\
        "', details:'" +str(self.details) +\
        "')" 
    
    def set_details(self, details):
        self.details = details
        
    def get_description(self):
        if(self.details is None):
            d = self.desc
        else:
            d = self.desc + u"\nOpis:\n" + self.details.description + u"\nTytul oryginalny:" + self.details.original_title
        return d

class EventDetails(object):
    """
    szczegóły wydarzenia (program w telewizji), zawiera dane zakodowane w unicode
    """
    def __init__(self, description, original_title):
        self.description = description
        self.original_title = original_title
            

    def __str__(self):
        return "EventDetails(description:'" + self.description+"',original_title:'"+self.original_title+"')" 
