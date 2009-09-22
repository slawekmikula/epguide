
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
            self.channelList.append({'name': data.decode('iso-8859-2'), 'id': self.currentId})


class WpProgrammeGetter(SGMLParser):
    def __init__(self):
        SGMLParser.__init__ (self)

        self.url = "http://tv.wp.pl/index_druk.html?T[date]=%s&T[station]=%s&T[time]=0"
        self.program_id = ""
        self.program_name = ""
        self.event_date = ""
        self.event_descr = ""

        s.state = []
        s.i = ""
        s.s_start ("HTML")
        s.success = False

    def GetStationList(self):
        raise NotImplementedError
    
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

    def s_start (s, state):
        s.state.append (state)

    def s_end (s, state):
        i = 2
        while s.state.pop() != state:
            i += 2

    def s_switch (s, state):
        s.state[-1] = state
       


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
        getter = WpChannelListGetter()
        stationList = getter.GetStationList()
        channelList = []

        if getter.success:            
            for station in stationList:
                if station['id'] != '---' and station['id'] != 0:
                    channel = Channel(station['name'], station['id'])
                    channelList.append(channel)

        channelList.sort(lambda first, second: int(first.id) < second.id)
        return channelList
    
    def GetGuide(self, date, channel_id):
        """
        pobiera informacje z strony oraz parsuje dane, zwraca liste elementow
        klasy Event
        """
        event_list = []
    
        url = self.url_template % (date, channel_id) 
        buffer = urllib.urlopen (url).read()
        events_getter = WpGetter()
        event_getter.feed(buffer)
        event_list = event_getter.GetEventList()
        
        return event_list
        
        # ---------- OLD --------------
    
        start_next_day = False
        end_next_day = False
        
        for i in range(len(parser.programs)):

            prog = parser.programs[i]

            uni_title = prog['title'].decode('iso-8859-2', 'replace').replace(u"&", u"&amp;")
            uni_subtitle = prog['sub-title'].decode('iso-8859-2', 'replace').replace(u"&", u"&amp;")
            uni_category = "</category>\n<category>".join(prog['cat']).decode('iso-8859-2', 'replace')
            uni_desc = prog['desc'].decode('iso-8859-2', 'replace')
            # replace & signs with &amp;
            uni_desc = string.replace(uni_desc, u"&", u"&amp;")
            uni_desc = string.replace(uni_desc, u"<", u"")
            uni_desc = string.replace(uni_desc, u">", u"")

            # data zakonczenia rowna startowi nastepnego programu, lub
            # jesli to ostatni program rowna startowi aktualnego
            if i == len(parser.programs)- 1:
                last_time = prog['time']
            else:
                last_time = parser.programs[i + 1]['time']

            # data rozpoczecia i konca rowna dacie w parserze
            date_start = time.strftime("%Y%m%d", parser.date)
            date_end = time.strftime("%Y%m%d", parser.date)

            # czas rozpoczecia rowny czasowi audycji, zakonczenia rowny
            # wyliczonemu czasowi powyzej
            time_start = prog['time'].replace(':', '')
            time_end = last_time.replace(':', '')

            # gdy godzina konca jest w nastepnym dniu
            if int(time_end) < int(time_start):
                end_next_day = True

            # gdy godzina startu jest w nastepnym dniu
            if int(time_start) < int(parser.programs[i-1]['time'].replace(':', '')):
                start_next_day = True

            year_start = year_end = time.strftime ("%Y", parser.date)

            month_start = month_end = time.strftime ("%m", parser.date)
            month_start = month_end = int(month_start)
            dayInMonth = monthTable[month_start - 1]
            
            day_start = day_end = time.strftime ("%d", parser.date)
            day_start = day_end = int(day_start)          

            if start_next_day == True:
                day_start = day_start + 1
                if day_start > dayInMonth:
                    day_start = 1
                    month_start = month_start + 1
                    if month_start > 12:
                        month_start = 1
                    
                day_start = str(day_start)
                month_start = str(month_start)                
                if len(day_start) == 1:
                    day_start = "0" + day_start
                if len(month_start) == 1:
                    month_start = "0" + month_start
                    
                date_start = str(year_start) + str(month_start) + str(day_start)
                
            if end_next_day == True:
                day_end = day_end + 1
                if day_end > dayInMonth:
                    day_end = 1
                    month_end = month_end + 1
                    if month_end > 12:
                        month_end = 1

                day_end = str(day_end)
                month_end = str(month_end)                
                if len(day_end) == 1:
                    day_end = "0" + day_end
                if len(month_end) == 1:
                    month_end = "0" + month_end
                   
                    
                date_end = str(year_end) + str(month_end) + str(day_end)
                        
        
 
    