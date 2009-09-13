#!/usr/bin/python
# 
# plik definiujacy obiekty przechowujace dane

class Channel(object):
    """
    definicja kanalu
    """
    def __init__(self, name = "", channel_id = ""):
        self.name = name
        self.channel_id = channel_id.replace(u'&',u'&amp;')


class Event(object):
    """
    wydarzenie (program w telewizji), zawiera dane zakodowane w unicode
    """
    def __init__(self):
        self.title = u''
        self.subtitle = u''
        self.category = u''
        self.desc = u''
        self.date_start = None
        self.time_start = None
        self.date_end = None
        self.time_end = None
    
    
class ChannelParser(object):    
    """
    obiekt definiujacy pozwiazanie parsera z identyfikatorem kanalu. Wykorzystywane
    w konfiguracji, do pobierania roznych kanalow przez rozne parsery
    """
    def __init__(self):
        pass