from sgmllib import SGMLParser
import time
import datetime
import urllib

from epguide.data_formats import Channel, Event

class WpNgChannelListGetter(SGMLParser):
    def __init__(self):
        SGMLParser.__init__ (self)

        self.url = "http://beta.tv.wp.pl/index.html"
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

    # <select onchange="document.searchFormT.stid.value=this.value;" name="stationId" id="stationId">
    def start_select(self, attributes):
        if self.state[-1] == 'init':
            for name, value in attributes:
                if name == "name" and value == 'stationId':
                    self.state.append("select")

    def end_select(self):
        if self.state[-1] == 'select':
            self.state.pop()
            self.success = True

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

class WpNgProgrammeGetter(SGMLParser):
    def __init__(self):
        SGMLParser.__init__ (self)


        self.url = "http://beta.tv.wp.pl/date,%s,name,TVP-2,stid,%s,program.html"
        self.eventDict = []
        self.prevEvent = None
        self.currentEvent = None
        self.bad_row = False

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
    def start_div(self, attrs):
        if self.state[-1] == "init" and self.getAttr(attrs, "class") == "bx bx2":
            self.state.append('start')
        elif self.state[-1] == "start" and self.getAttr(attrs, "class") == "content":
            self.state.append('content')
        elif self.state[-1] == "content" and self.getAttr(attrs, "class").startswith("program"):
            self.currentEvent = {'channel_id': self.currentChannelId, 'channel_name': "",
                'date': self.currentDate, 'time': "", 'title': "", 'desc': ""}
            self.state.append('program')
        elif self.state[-1] == "content" and self.getAttr(attrs, "class") != "program":
            self.state.append('dummy')
        elif self.state[-1] == "program" and self.getAttr(attrs, "class") == "programIn clra":
            self.state.append('program clra')
        elif self.state[-1] == "program clra" and self.getAttr(attrs, "class") == "programL":
            self.state.append('programL')
        elif self.state[-1] == "programL" and self.getAttr(attrs, "class") == "icons":
            self.state.append('dummy')
        elif self.state[-1] == "programL" and self.getAttr(attrs, "class") == "imgDiv":
            self.state.append('dummy')
        elif self.state[-1] == "programL" and self.getAttr(attrs, "class") == "imgDivEmpty":
            self.state.append('dummy')
        elif self.state[-1] == "program clra" and self.getAttr(attrs, "class") == "programR":
            self.state.append('programR')


    def end_div (self):
        if self.state[-1] == 'start':
            self.state.pop()
        elif self.state[-1] == 'content':
            self.state.pop()
        elif self.state[-1] == 'dummy':
            self.state.pop()
        elif self.state[-1] == 'program clra':
            self.state.pop()
        elif self.state[-1] == 'program':
            if self.currentEvent is not None:
                self.FormatEventDateTime()
                self.eventDict.append(self.currentEvent)
                self.prevEvent = self.currentEvent
            self.state.pop()
        elif self.state[-1] == 'programL':
            self.state.pop()
        elif self.state[-1] == 'programR':
            self.state.pop()


    def start_strong(self, attrs):
        if self.state[-1] == 'programL':
            self.state.append("start_hour")

    def end_strong(self):
        if self.state[-1] == 'start_hour':
            self.state.pop()

    def start_h4(self, attrs):
        if self.state[-1] == 'programR':
            self.state.append("title")

    def end_h4(self):
        if self.state[-1] == 'title':
            self.state.pop()

    def start_a(self, attrs):
        if self.state[-1] == 'title':
            self.state.append("title_a")

    def end_a(self):
        if self.state[-1] == 'title_a':
            self.state.pop()

    def start_p(self, attrs):
        if self.state[-1] == 'programR' and self.getAttr(attrs, "class") == "opis":
            self.state.append("description")
        if self.state[-1] == 'programR' and self.getAttr(attrs, "class") == "ekipa":
            self.state.append("crew")

    def end_p(self):
        if self.state[-1] == 'description':
            self.state.pop()
        if self.state[-1] == 'crew':
            self.state.pop()

    def handle_data (self, data):
        if self.currentEvent is None:
            return

        data = data.strip()
        if self.state[-1] == "start_hour":
            self.currentEvent['time'] = data.decode('iso-8859-2')
        elif self.state[-1] == "title" or self.state[-1] == "title_a" :
            self.currentEvent['title'] += data.decode('iso-8859-2')
        elif self.state[-1] == 'description' or self.state[-1] == 'crew':
            self.success = True
            if data.decode('iso-8859-2') != 'czytaj dalej':
                self.currentEvent['desc'] += data.decode('iso-8859-2') + "\n"


class WpNgParser(object):
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
        getter = WpNgChannelListGetter()
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
        getter = WpNgProgrammeGetter()
        eventDict = getter.GetEventList(date, channel_id)
        eventClassList = []

        if getter.success:
            for event in eventDict:
                eventClass = Event(event['channel_id'], event['channel_name'],
                    event['title'], '', '', event['desc'], event['time_start'],
                    event['time_end'])
                eventClassList.append(eventClass)

        return eventClassList
