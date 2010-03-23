from sgmllib import SGMLParser
import time
import datetime
import urllib

from epguide.data_formats import Channel, Event

class TelemanChannelListGetter(SGMLParser):
    def __init__(self):
        SGMLParser.__init__ (self)

        #http://www.teleman.pl/station.html?id=1&day=1
        self.url = "http://www.teleman.pl/station.html?id=1&day=1"
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

    def start_form(self, attrs):
        if self.state[-1] == 'init':
            for name, value in attrs:
                if name == "action" and value == '/station.html':
                    self.state.append("form")

    def end_form(self):
        if self.state[-1] == 'form':
            self.state.pop()
            self.success = True


    # <select onchange="document.searchFormT.stid.value=this.value;" name="stationId" id="stationId">
    def start_select(self, attributes):
        if self.state[-1] == 'form':
            for name, value in attributes:
                if name == "name" and value == 'id':
                    self.state.append("select")

    def end_select(self):
        if self.state[-1] == 'select':
            self.state.pop()

    # <option value="1" id="TVP-1">TVP 1</option>
    def start_option(self, attributes):
        if self.state[-1] == 'select' or self.state[-1] == 'option':
            for name, value in attributes:
                if name == "value" and value != "":
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

class TelemanProgrammeGetter(SGMLParser):
    def __init__(self):
        SGMLParser.__init__ (self)

        #http://www.teleman.pl/station.html?id=1&day=1
        self.url = "http://www.teleman.pl/station.html?id=%s&day=%s"
        self.eventDict = []
        self.prevEvent = None
        self.currentEvent = None
        self.bad_row = False

        self.state = ['init']
        self.success = False

    def GetEventList(self, eventDate, channel_id):
        self.currentDate = eventDate
        self.currentChannelId = channel_id
        self.currentChannelName = '' # wypelnione przy parsowaniu

        dateDiff = eventDate - datetime.date.today()
        self.url = self.url % (channel_id, dateDiff.days)
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
        return ""

    def FormatEventDateTime(self):
        self.currentEvent['time_start'] = "%s %s" % (self.currentEvent['date'].strftime("%Y-%m-%d"), self.currentEvent['time'])
        self.currentEvent['time_start'] = time.strptime(self.currentEvent['time_start'], '%Y-%m-%d %H:%M')
        self.currentEvent['time_start'] = datetime.datetime.fromtimestamp(time.mktime(self.currentEvent['time_start']))

        self.UpdatePreviousTimeEnd()

    def UpdatePreviousTimeEnd(self):

        if self.prevEvent is not None and self.currentEvent is not None:
            self.prevEvent['time_end'] = self.currentEvent['time_start']

            # jesli przekraczamy kolejna dobe, robimy poprawke w dacie
            if self.prevEvent['time_end'] < self.prevEvent['time_start']:
                self.prevEvent['time_end'] = self.prevEvent['time_end'] + datetime.timedelta(days=1)
                self.currentEvent['time_start'] = self.currentEvent['time_start'] + datetime.timedelta(days=1)

        # przypadek, gdy jestesmy na koncu listy
        if self.prevEvent is not None and self.currentEvent is None:
            self.prevEvent['time_end'] = self.prevEvent['time_start']


    # -------------------------------------
    def start_table(self, attrs):
        if self.state[-1] == "init" and self.getAttr(attrs, "id") == "programmes":
            self.state.append('start')

    def end_table (self):
        if self.state[-1] == 'start':
            self.state.pop()

    def start_tr(self, attrs):
        if self.state[-1] == 'start':
            self.state.append('program')
            self.currentEvent = {'channel_id': self.currentChannelId, 'channel_name': "",
                'date': self.currentDate, 'time': "", 'title': "", 'desc': "", 'category': ""}

    def end_tr(self):
        if self.state[-1] == 'program':
            if self.currentEvent is not None:
                self.FormatEventDateTime()
                self.eventDict.append(self.currentEvent)
                self.prevEvent = self.currentEvent
            self.state.pop()

    def start_th(self, attrs):
        if self.state[-1] == 'program':
            self.state.append('start_hour')

    def end_th(self):
        if self.state[-1] == 'start_hour':
            self.state.pop()

    def start_td(self, attrs):
        if self.state[-1] == 'program':
            self.state.append('description')

    def end_td(self):
        if self.state[-1] == 'description':
            self.state.pop()

    def start_span(self, attrs):
        if self.state[-1] == "description" and self.getAttr(attrs, "class") == "categ categ-xxx":
            self.state.append('category')

    def end_span(self):
        if self.state[-1] == 'category':
            self.state.pop()

    def start_a(self, attrs):
        if self.state[-1] == 'description':
            self.state.append('title')

    def end_a(self):
        if self.state[-1] == 'title':
            self.state.pop()

    def start_p(self, attrs):
        if self.state[-1] == 'description':
            self.state.append('content')

    def end_p(self):
        if self.state[-1] == 'content':
            self.state.pop()

    def start_div(self, attrs):
        if self.state[-1] == 'start_hour' and self.getAttr(attrs, "class") == "running":
            self.state.append('dummy')
        elif self.state[-1] == 'init' and self.getAttr(attrs, "id") == "station" and self.getAttr(attrs, "class") == "content":
            self.state.append('channel_name_div')

    def end_div(self):
        if self.state[-1] == 'dummy':
            self.state.pop()
        elif self.state[-1] == 'channel_name_div':
            self.state.pop()

    def start_h1(self, attrs):
        if self.state[-1] == 'channel_name_div':
            self.state.append('channel_name')

    def end_h1(self):
        if self.state[-1] == 'channel_name':
            self.state.pop()

    def start_img(self, attrs):
        if self.state[-1] == 'channel_name':
            self.state.append('channel_name_img')

    def end_img(self):
        if self.state[-1] == 'channel_name_img':
            self.state.pop()

    def handle_data (self, data):
        if self.state[-1] == "channel_name_img" and self.state[-2] == 'channel_name':
            self.currentChannelName = data.decode('utf-8').strip()
            
        if self.currentEvent is None:
            return

        data = data.strip()
        if self.state[-1] == "start_hour":
            self.currentEvent['time'] = data.decode('utf-8')
        elif self.state[-1] == "title":
            self.currentEvent['title'] += data.decode('utf-8')
        elif self.state[-1] == "category":
            self.currentEvent['category'] += data.decode('utf-8')
        elif self.state[-1] == 'content':
            self.success = True
            self.currentEvent['desc'] += data.decode('utf-8') + "\n"
            self.currentEvent['channel_name'] = self.currentChannelName


class TelemanParser(object):
    """
    parser pobierajacy dane z nowego interfejsu www tv.Wp.pl (beta)
    """
    def __init__(self):
        pass

    def Init(self):
        pass

    def Finish(self):
        pass

    def GetChannelList(self):
        """ pobiera liste kanalow """
        getter = TelemanChannelListGetter()
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
        getter = TelemanProgrammeGetter()
        eventDict = getter.GetEventList(date, channel_id)
        eventClassList = []

        if getter.success:
            for event in eventDict:
                eventClass = Event(event['channel_id'], event['channel_name'],
                    event['title'], '', event['category'], event['desc'],
                    event['time_start'], event['time_end'])
                eventClassList.append(eventClass)

        return eventClassList
