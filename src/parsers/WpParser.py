
from sgmllib import SGMLParser

import string
import time
import urllib
import re
import parser

from data_formats import Channel

class WpChannelListGetter(SGMLParser):
    def __init__(self):
        SGMLParser.__init__ (self)

        self.url = "http://tv.wp.pl/index.html"
        self.channelList = []

        self.state = ['init']
        self.currentId = None
        self.success = False

    def GetStationList(self):
        buf = urllib.urlopen (self.url).read()
        self.feed(buf)
        self.close()
        return self.channelList

    def close (self):
        SGMLParser.close (self)

    # <select name=T[station] style="max-width: 200px; width: 200px">
    def start_select(self, attributes):
        if self.state[-1] == 'init':
            for name, value in attributes:
                if name == "name" and value == 'T[station]':
                    self.state.append("select")

    def end_select(self):
        if self.state[-1] == 'select':
            self.state.pop()
            self.success = True

    # <option value="1">TVP 1
    def start_option(self, attributes):
        if self.state[-1] == 'select' or self.state[-1] == 'option':
            for name, value in attributes:
                if name == "value":
                    self.currentId = value
                    self.state.append("option")


    def end_option(self):
        if self.state[-1] == 'option':
            self.state.pop()

    def handle_data(self, data):
        data = data.strip()
        if self.state[-1] == 'option':
            if data == '&':
                self.state.append('ampersand')
                self.channelList[-1]['name'] += ' & '
            else:
                self.channelList.append({'name': data.decode('iso-8859-2'), 'id': self.currentId})
        elif self.state[-1] == 'ampersand':
            self.channelList[-1]['name'] += data.decode('iso-8859-2')
            self.state.pop()

class WpProgrammeGetter(SGMLParser):
    def __init__(self):
        SGMLParser.__init__ (self)

        self.url = "http://tv.wp.pl/index_druk.html?T[date]=%s&T[station]=%s&T[time]=0"
        self.eventDict = []

        self.state = ['init']
        self.currentId = None
        self.success = False

    def GetEventList(self, date, channel_id):
        buf = urllib.urlopen (self.url).read()
        self.feed(buf)
        print self.eventDict
        self.close()
        return self.eventDict
    
    def close (s):
        SGMLParser.close (s)
        s.channel = s.channel.decode("iso-8859-2", "replace").strip()
        s.chanid = re.sub("[^a-z0-9]", "", s.channel.lower()) + ".wp"
        s.s_end ("HTML")

    def get_attr (s, list, name):
        for attr in list:
            if attr[0] == name:
                return attr[1]
        return None

    def s_start (s, state):
        s.state.append (state)

    def s_end (s, state):
        i = 2
        while s.state.pop() != state:
            i += 2

    def s_switch (s, state):
        s.state[-1] = state

    # -------------------------------------

    def start_table(s, attrs):
        if s.state[-1] == "HTML" and s.get_attr (attrs, "class") == "drukowalne":
            s.s_start ("TABLE")
            s.s_start ("NAME")

    def end_table (s):
        if "TABLE" in s.state:
            s.s_end ("TABLE")

    def start_b (s, attrs):
        if s.get_attr (attrs, "class") == "ng":
            if s.state[-1] == "NAME":
                s.s_start ("name")
            elif s.state[-1] == "DATE":
                s.s_start ("date")
        elif s.state[-1] == "P_TIME":
            s.s_start ("p_time")
        elif s.state[-1] == "P_TITLE":
            s.s_start ("p_title")

    def end_b (s):
        if "name" in s.state:
            s.s_end ("name")
            s.s_switch ("DATE")
        elif "date" in s.state:
            s.s_end ("date")
            s.s_switch ("PROGRAMS")
            s.programs = []
        elif "p_time" in s.state:
            s.s_end ("p_time")
            s.s_switch ("P_TITLE")
        elif "p_title" in s.state:
            s.s_end ("p_title")
            s.s_switch ("P_DESC")

    def start_span (s, attrs):
        if s.get_attr (attrs, "class") == "SGinfo":
            if s.state[-1] == "P_DESC":
                s.s_start ("p_desc")

    def end_span (s):
        if "p_desc" in s.state:
            s.s_end ("p_desc")

    def start_tr (s, attrs):
        if s.state[-1] == "PROGRAMS":
            s.program = {'time': "", 'title': "", 'desc': ""}
            s.s_start ("PROGRAM")
            s.s_start ("P_TIME")

    def end_tr (s):
        if "PROGRAM" in s.state:
            s.program['sub-title'] = ""
            s.program['cat'] = []
            s.programs.append (s.program)
            s.s_end ("PROGRAM")

    def handle_data (s, data):
        data = data.strip()
        if s.state[-1] == "name":
            s.channel = data
        elif s.state[-1] == "date":
            s.date = time.strptime (data[11:21], "%d.%m.%Y")
        elif s.state[-1] == "p_time":
            s.program['time'] = data
        elif s.state[-1] == "p_title":
            s.program['title'] = data
        elif s.state[-1] == "p_desc":
            s.success = True
            s.program['desc'] += data + "\n"



class WpParser(object):
    """
    parser pobierajacy dane z Wp.pl
    """ 
    def __init__(self):
        pass
   
    def Init(self): 
        pass
    
    def Finish(self):
        pass
    
    def GetChannelList(self):
        """ pobiera liste kanalow """
        getter = WpChannelListGetter()
        stationList = getter.GetStationList()
        channelList = []

        if getter.success:            
            for station in stationList:
                # usuwamy elementy kontrolne oraz 'Wszystkie kanaly'
                if station['id'] != '---' and int(station['id']) != 0:
                    channel = Channel(station['name'], int(station['id']))
                    channelList.append(channel)

        # usuwamy duplikaty i sortujemy liste
        dict = {}
        for channel in channelList:
            dict[channel] = channel
        channelList = dict.values()
        channelList.sort()

        return channelList

    def GetGuide(self, date, channel_id):
        """
        pobiera informacje z strony oraz parsuje dane, zwraca liste elementow
        klasy Event
        """
        getter = WpProgrammeGetter()
        eventDict = getter.GetEventList(date, channel_id)
        eventClassList = []

        if getter.success:
            for event in eventDict:
                eventClass = Event(event['channel_id'], event['title'], event['subtitle'],
                    event['category'], event['description'],
                    event['time_start'], event['time_end'])
                eventClassList.append(eventClass)

        return eventClassList
        
    