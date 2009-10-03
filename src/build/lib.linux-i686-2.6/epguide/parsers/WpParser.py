from sgmllib import SGMLParser
import time
import datetime
import urllib

from epguide.data_formats import Channel, Event

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
        self.prevEvent = None
        self.currentEvent = None

        self.state = ['init']
        self.success = False

    def GetEventList(self, eventDate, channel_id):
        self.currentDate = eventDate
        self.currentChannelId = channel_id

        self.url = self.url % (eventDate.strftime("%Y-%m-%d"), channel_id)
        buf = urllib.urlopen (self.url).read()
        self.feed(buf)
        self.close()
        self.UpdatePreviousTimeEnd()
        
        return self.eventDict
    
    def close(self):
        SGMLParser.close(self)

    def getAttr(self, list, name):
        for attr in list:
            if attr[0] == name:
                return attr[1]
        return None

    def FormatEventDateTime(self):
        self.currentEvent['time_start'] = "%s %s" % (self.currentEvent['date'].strftime("%Y-%m-%d"), self.currentEvent['time'])
        self.currentEvent['time_start'] = time.strptime(self.currentEvent['time_start'], '%Y-%m-%d %H:%M')
        self.currentEvent['time_start'] = datetime.datetime.fromtimestamp(time.mktime(self.currentEvent['time_start']))
        
        self.UpdatePreviousTimeEnd()

    def UpdatePreviousTimeEnd(self):
        
        if self.prevEvent is not None:
            self.prevEvent['time_end'] = self.currentEvent['time_start']

            # jesli przekraczamy kolejna dobe, robimy poprawke w dacie
            if self.prevEvent['time_end'] < self.prevEvent['time_start']:
                self.prevEvent['time_end'] = self.prevEvent['time_end'] + datetime.timedelta(days=1)
                self.currentEvent['time_start'] = self.currentEvent['time_start'] + datetime.timedelta(days=1)

    # -------------------------------------
    def start_table(self, attrs):
        if self.state[-1] == "init" and self.getAttr(attrs, "class") == "drukowalne":
            self.state.append('table')

    def end_table (self):
        if self.state[-1] == 'table':
            self.state.pop()

    def start_tr(self, attrs):
        if self.getAttr(attrs, "bgcolor") == '#D9E5FF':
            self.state.append('dummy')
        elif self.state[-1] == "table":
            self.currentEvent = {'channel_id': self.currentChannelId, 'channel_name': "",
                'date': self.currentDate, 'time': "", 'title': "", 'desc': ""}
            self.state.append("program")
            self.state.append("time")

    def end_tr (self):
        if self.state[-1] == "program":
            self.FormatEventDateTime()
            self.eventDict.append(self.currentEvent)
            self.prevEvent = self.currentEvent
            self.state.pop()
        elif self.state[-1] == 'dummy':
            self.state.pop()

    def start_td(self, attrs):
        if self.state[-1] != 'dummy':
            if self.getAttr(attrs, 'colspan') == '2':
                self.state.append('channel_name')

    def end_td(self):
        if self.state[-1] == 'channel_name':
            self.state.pop()

    def start_b (self, attrs):
        if self.state[-1] == "time":
            self.state.append("data_time")
        elif self.state[-1] == "title":
            self.state.append("data_title")
        elif self.state[-1] == 'channel_name':
            self.state.append("data_channel_name")

    def end_b (self):
        if self.state[-1] == "time":
            self.state.pop()
            self.state.append('title')
        elif self.state[-1] == "title":
            self.state.pop()
            self.state.append('desc')

    def start_span (self, attrs):
        if self.getAttr(attrs, "class") == "SGinfo":
            if self.state[-1] == "desc":
                self.state.append("data_desc")

    def end_span (self):
        if self.state[-1] == 'data_desc':
            self.state.pop()
            self.state.pop()

    def handle_data (self, data):
        data = data.strip()
        if self.state[-1] == "data_time":
            self.currentEvent['time'] = data.decode('iso-8859-2')
            self.state.pop()
        elif self.state[-1] == "data_title":
            self.currentEvent['title'] = data.decode('iso-8859-2')
            self.state.pop()            
        elif self.state[-1] == "data_desc":
            self.success = True
            self.currentEvent['desc'] += data.decode('iso-8859-2') + "\n"
        elif self.state[-1] == "data_channel_name":
            self.currentEvent['channel_name'] = data.decode('iso-8859-2')
            self.state.pop()



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
                eventClass = Event(event['channel_id'], event['channel_name'],
                    event['title'], '', '', event['desc'], event['time_start'],
                    event['time_end'])
                eventClassList.append(eventClass)

        return eventClassList
        