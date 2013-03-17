# -*- coding: utf-8 -*-
from epguide.parsers.teleman import TelemanChannelListParser, \
    TelemanProgrammeParser, HttpHelper, TelemanProgrammeDetailsParser
import datetime



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
    
    def details_url(self, relative_url):
        url = "http://www.teleman.pl"
        url = url + relative_url
        return url

class TelemanParser(object):
    """
    parser pobierajacy dane ze strony teleman.pl
    """
    def __init__(self, split_title, debug_http):
        self.url_provider = TelemanUrlProvider()
        self.split_title = split_title
        self.http_helper = HttpHelper.HttpHelper(debug_http)

    def Init(self):
        pass

    def Finish(self):
        pass

    def get_channels(self):
        """ pobiera liste kanalow ze strony teleman.pl """
        url = self.url_provider.channel_list_url()
        content = self.http_helper.get(url)
        getter = TelemanChannelListParser()
        channelList = getter.get_channels(content)
        return channelList
        
#        return self.get_channels_from_file(urllib.urlopen(url))
        
    def get_channels_from_file(self, f):
        """ pobiera liste kanalow z podanego pliku html """
        buf = f.read()
        print "get_channels xxx"
        getter = TelemanChannelListParser()
        channelList = getter.get_channels(buf)
        return channelList

    def get_guide(self, eventDate, channel_id):
        """
        pobiera informacje z strony oraz parsuje dane, zwraca liste elementow
        klasy Event
        """
        url = self.url_provider.guide_url(eventDate, channel_id)
        print " url: " + url
        f = self.http_helper.get(url)
        return self.get_guide_from_file(eventDate, channel_id, f)

    def get_guide_from_file(self, eventDate, channel_id, f):
        buf = f  # .read()
        getter = TelemanProgrammeParser.TelemanProgrammeParser(self.split_title)
        events = getter.get_events(eventDate, channel_id, buf)
        for event in events:
            if event.main_category == "Movie/Drama":
                details = self.get_details(event.url)
                event.set_details(details)
        return events

    def get_details(self, relative_url):
        url = self.url_provider.details_url(relative_url)
        print " url: " + url
        f = self.http_helper.get(url, force_cache=True)
        return self.get_details_from_file(f)
    
    def get_details_from_file(self, f):
        buf = f  # .read()
        getter = TelemanProgrammeDetailsParser.TelemanProgrammeDetailsParser("dummy")
        details = getter.get_details(buf)
        return details
    
