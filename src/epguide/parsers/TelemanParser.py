# -*- coding: utf-8 -*-
from sgmllib import SGMLParser
import time
import datetime
import urllib
import re

from epguide.data_formats import Channel, Event

    
class TelemanChannelListGetter(SGMLParser):
    def __init__(self):
        SGMLParser.__init__ (self)

        self.channels_data = []

        self.state = ['init']
        self.current_href = None
        self.success = False

    def get_channels_data(self, buf):
        self.feed(buf)
        self.close()
        return self.channels_data
    
    def get_channels(self, buf):
        station_list = self.get_channels_data(buf)
#        if self.success:
        channel_list = [Channel(station['name'], station['id']) for station in station_list]

        # usuwamy duplikaty i sortujemy liste
        channel_set = {}
        for channel in channel_list:
            channel_set[channel] = channel
        channel_list = channel_set.values()
        channel_list.sort()

        return channel_list
    

    def close (self):
        SGMLParser.close (self)

    def start_div(self, attrs):
        if self.state[-1] == 'init':
            for name, value in attrs:
                if name == "id" and value == 'stations_index':
                    self.state.append("div")

    def end_div(self):
        if self.state[-1] == 'div':
            self.state.pop()
            self.success = True


    def start_li(self, attributes):
        if self.state[-1] == 'div':
            self.state.append("li")

    def end_li(self):
        if self.state[-1] == 'li':
            self.state.pop()

    # <option value="1" id="TVP-1">TVP 1</option>
    def start_a(self, attrs):
        if self.state[-1] == 'li':
            self.state.append("a")
            for name, value in attrs:
                if name == "href":
                    self.current_href = value.split("/")[-1]

    def end_a(self):
        if self.state[-1] == 'a':
            self.state.pop()

    def handle_data(self, data):
        data = data.strip()
        if self.state[-1] == 'a':
            self.channels_data.append({'name': data.decode('iso-8859-2'), 'id': self.current_href})

class TelemanProgrammeGetter(SGMLParser):
    def __init__(self, split_title):
        SGMLParser.__init__ (self)
        self.split_title = split_title
        self.event_dict = []
        self.prev_event = None
        self.current_event = None
        self.bad_row = False
        self.episode_regexp = re.compile(r'(?P<title>.+)\((?P<odc>.+)\)')
        self.subtitle_regexp = re.compile(r'(?P<title>.+):(?P<subtitle>.+)')
        self.category_classes_to_main_category = {'cat-roz':"Leisure hobbies", 'cat-ser':"Show/Game show", 'cat-fil':"Movie/Drama", 'cat-xxx':"News/Current affairs", 'cat-dzi':"Children's/Youth programmes", "cat-spo":"Sports"}
        self.state = ['init']
        self.success = False

    def get_events(self, event_date, channel_id, buf):
        """
        parsuje stronę, zwraca liste elementow
        klasy Event
        """
        self.current_date = event_date
        self.current_channel_id = channel_id
        self.current_channel_name = ''  # wypelnione przy parsowaniu
        self.feed(buf)
        self.close()
        self._update_previous_time_end()

        events = []

        if self.success:
            events = [self.create_event(event_data) for event_data in self.event_dict]

        return events
    
    def create_event(self, event):
        title = event['title']
        # print "  title: '" + title + "'"
        if self.split_title:
            episode_match = self.episode_regexp.match(title)
            if episode_match is None:
                # print "  #odc not found"
                episode_num = ''
            else:
                # print "  #title: '" + episode_match.group('title') + "'"
                # print "  #odc: '" + episode_match.group('odc') + "'"
                title = episode_match.group('title').strip()
                episode_num = episode_match.group('odc').strip()
    
            subtitle_match = self.subtitle_regexp.match(title)
            if subtitle_match is None:
                # print "  #subtitle not found"
                subtitle = ''
            else:
                # print "  #title: '" + subtitle_match.group('title') + "'"
                # print "  #subtitle: '" + subtitle_match.group('subtitle') + "'"
                title = subtitle_match.group('title').strip()
                subtitle = subtitle_match.group('subtitle').strip()
        else:
                subtitle = ''
                episode_num = ''
            
        time_start = event['time_start']
        time_end = event['time_end']
        channel_id = event['channel_id']
        main_category = event['main_category']
        category = event['category']
        print "event: " + channel_id + " " + str(time_start) + " " + str(time_end) + " " + title + " " + subtitle + " " + episode_num + " " + main_category + " " + category
        eventClass = Event(
                           channel_id,
                           event['channel_name'],
                           title,
                           subtitle,
                           main_category,
                           category,
                           event['desc'],
                           time_start,
                           time_end,
                           episode_num)
        return eventClass

    def close(self):
        SGMLParser.close(self)

    def getAttr(self, attrs, name):
        for attr in attrs:
            if attr[0] == name:
                return attr[1]
        return ""

    def _format_event_datetime(self):
        self.current_event['time_start'] = "%s %s" % (self.current_event['date'].strftime("%Y-%m-%d"), self.current_event['time'])
        self.current_event['time_start'] = time.strptime(self.current_event['time_start'], '%Y-%m-%d %H:%M')
        self.current_event['time_start'] = datetime.datetime.fromtimestamp(time.mktime(self.current_event['time_start']))

        self._update_previous_time_end()

    def _update_previous_time_end(self):

        if self.prev_event is not None and self.current_event is not None:
            self.prev_event['time_end'] = self.current_event['time_start']

            # jesli przekraczamy kolejna dobe, robimy poprawke w dacie
            if self.prev_event['time_end'] < self.prev_event['time_start']:
                self.prev_event['time_end'] = self.prev_event['time_end'] + datetime.timedelta(days=1)
                self.current_event['time_start'] = self.current_event['time_start'] + datetime.timedelta(days=1)

        # przypadek, gdy jestesmy na koncu listy
        if self.prev_event is not None and self.current_event is None:
            self.prev_event['time_end'] = self.prev_event['time_start']

    # -------------------------------------
    def start_ul(self, attrs):
        if self.state[-1] == "init" and self.getAttr(attrs, "id") == "station-listing":
            self.state.append('start')

    def end_ul (self):
        if self.state[-1] == 'start':
            self.state.pop()

    def start_li(self, attrs):
        if self.state[-1] == 'start':
            self.state.append('program')
            class_attrs = self.getAttr(attrs, "class").split()
            main_category_class = next((c for c in class_attrs if c.startswith("cat-")), None)
            main_category = self.category_classes_to_main_category.get(main_category_class, "")
            print "main_category_class:" + main_category_class + " main_category:" + main_category
            self.current_event = {'channel_id': self.current_channel_id, 'channel_name': "",
                'date': self.current_date, 'time': "", 'title': "", 'desc': "", 'main_category': main_category, 'category': ""}

    def end_li(self):
        if self.state[-1] == 'program':
            if self.current_event is not None:
                self._format_event_datetime()
                self.event_dict.append(self.current_event)
                self.prev_event = self.current_event
            self.state.pop()

    def start_em(self, attrs):
        if self.state[-1] == 'program' and not self.current_event.get('time'):
            self.state.append('start_hour')

    def end_em(self):
        if self.state[-1] == 'start_hour':
            self.state.pop()

    def start_div(self, attrs):
        if self.state[-1] == 'program' and self.getAttr(attrs, "class") == "detail":
            self.state.append('description')
        elif self.state[-1] == 'init' and self.getAttr(attrs, "class") == "station_title":
            self.state.append('channel_name_div')

    def end_div(self):
        if self.state[-1] in ('description', 'channel_name_div'):
            self.state.pop()

    def start_a(self, attrs):
        if self.state[-1] == 'description':
            self.state.append('title')

    def end_a(self):
        if self.state[-1] == 'title':
            self.state.pop()

    def start_p(self, attrs):
        if self.state[-1] == 'description':
            if self.getAttr(attrs, "class") == "genre":
                self.state.append('category')
            else:
                self.state.append('content')

    def end_p(self):
        if self.state[-1] in ('content', 'category'):
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
        # nazwa kanalu
        if self.state[-1] == "channel_name_img" and self.state[-2] == 'channel_name':
            self.current_channel_name = data.decode('utf-8').strip()
        # dla kanalow bez obrazka logo kanalu
        elif self.state[-1] == "channel_name" and data != "":
            self.current_channel_name = data.decode('utf-8').strip()

        if self.current_event is None:
            return

        data = data.strip()
        if self.state[-1] == "start_hour":
            self.current_event['time'] = data.decode('utf-8')
        elif self.state[-1] == "title":
            self.current_event['title'] += data.decode('utf-8')
            self.current_event['channel_name'] = self.current_channel_name
        elif self.state[-1] == "category":
            self.current_event['category'] += data.decode('utf-8')
        elif self.state[-1] == 'content':
            self.success = True
            self.current_event['desc'] += data.decode('utf-8') + "\n"


class TelemanUrlProvider(object):
    def channel_list_url(self):
        return "http://www.teleman.pl/program-tv/stacje"
        
    def guide_url(self, eventDate, channel_id):
        url = "http://www.teleman.pl/program-tv/stacje/%s?day=%s&hour=-1"
        today = datetime.datetime.today()
        eventMidnight = datetime.datetime(eventDate.year, eventDate.month, eventDate.day)
        todayMidnight = datetime.datetime(today.year, today.month, today.day)
        dateDiff = eventMidnight - todayMidnight
        print " eventMidnight: " + str(eventMidnight) + " todayMidnight:" + str(todayMidnight) + " dateDiff" + str(dateDiff)
        url = url % (channel_id, dateDiff.days)
        return url

class TelemanParser(object):
    """
    parser pobierajacy dane ze strony teleman.pl
    """
    def __init__(self, split_title, debug_http):
        self.url_provider = TelemanUrlProvider()
        self.split_title = split_title
        if debug_http:
            import httplib
            httplib.HTTPConnection.debuglevel = 1 

    def Init(self):
        pass

    def Finish(self):
        pass

    def get_channels(self):
        """ pobiera liste kanalow ze strony teleman.pl """
        url = self.url_provider.channel_list_url()
        return self.get_channels_from_file(urllib.urlopen(url))
        
    def get_channels_from_file(self, f):
        """ pobiera liste kanalow z podanego pliku html """
        buf = f.read()
        print "get_channels"
        getter = TelemanChannelListGetter()
        channelList = getter.get_channels(buf)
        return channelList

    def get_guide(self, eventDate, channel_id):
        """
        pobiera informacje z strony oraz parsuje dane, zwraca liste elementow
        klasy Event
        """
        url = self.url_provider.guide_url(eventDate, channel_id)
        print " url: " + url
        f = urllib.urlopen(url)
        return self.get_guide_from_file(eventDate, channel_id, f)

    def get_guide_from_file(self, eventDate, channel_id, f):
        buf = f.read()
        getter = TelemanProgrammeGetter(self.split_title)
        return getter.get_events(eventDate, channel_id, buf)
