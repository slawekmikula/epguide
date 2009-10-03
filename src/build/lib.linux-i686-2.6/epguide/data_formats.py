#!/usr/bin/python
# 
# plik definiujacy obiekty przechowujace dane

class Channel(object):
    """
    definicja kanalu
    """
    def __init__(self, name = "", id = ""):
        self.name = name
        self.id = id

    def __hash__(self):
        return self.id

    def __cmp__(self, other):
        return self.id - other.id

class Event(object):
    """
    wydarzenie (program w telewizji), zawiera dane zakodowane w unicode
    """
    def __init__(self, channel_id, channel_name, title, subtitle, category,
        desc, time_start, time_end):
            
        self.channel_id = channel_id
        self.channel_name = channel_name
        self.title = title
        self.subtitle = subtitle
        self.category = category
        self.desc = desc
        self.time_start = time_start
        self.time_end = time_end
    
    def __hash__(self):
        return self.channel_id + self.time_start

    def __cmp__(self, other):
        return (self.channel_id + self.time_start) - (other.channel_id + other.time_start)
