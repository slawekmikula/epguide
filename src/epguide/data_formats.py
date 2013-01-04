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
        desc, time_start, time_end=None, episode_num=None):
            
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
    
    def __hash__(self):
        return self.channel_id + self.time_start

    def __cmp__(self, other):
        return (self.channel_id + self.time_start) - (other.channel_id + other.time_start)

    def __str__(self):
        return "Event(channel_id:'" + self.channel_id + "', channel_name:'" + self.channel_name + "', time_start:'" + str(self.time_start) + "', time_end:'" + str(self.time_end) + "', title:'" + self.title + "', subtitle:'" + self.subtitle + "', episode_num:'" + self.episode_num + "', main_category:'" + self.main_category + "', category:'" + self.category + "', desc:'" + self.desc.replace("\n", "\\n") + "')" 
