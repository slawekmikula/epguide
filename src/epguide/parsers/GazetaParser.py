# -*- coding: utf-8 -*-
from epguide.parsers.gazeta import GazetaChannelListParser, \
    GazetaProgrammeParser, GazetaProgrammeDetailsParser
from epguide.parsers import HttpHelper    

class GazetaUrlProvider(object):
    def channel_list_url(self):
        return "http://tv.gazeta.pl/program_tv/0,110740,8750044.html"
        
    def guide_url(self, eventDate, channel_id):
        url = "http://tv.gazeta.pl/program_tv/0,110298,8700474,,,%s,3,%s,--,0.html"
        date = eventDate.strftime("%Y-%m-%d") 
        url = url % (date, channel_id)
        return url
    
    def details_url(self, event_id):
        url = "http://tv.gazeta.pl%s"
        url = url % event_id
        return url

class GazetaParser(object):
    """
    parser pobierajacy dane ze strony tv.gazeta.pl
    """
    def __init__(self, parser_options, debug_http):
        self.url_provider = GazetaUrlProvider()
        self.parser_options = parser_options
        self.http_helper = HttpHelper.HttpHelper(debug_http)

    def Init(self):
        pass

    def Finish(self):
        pass

    def get_channels(self):
        """ pobiera liste kanalow ze strony tv.gazeta.pl """
        url = self.url_provider.channel_list_url()
        content = self.http_helper.get(url, False, "ISO-8859-2")
        getter = GazetaChannelListParser.GazetaChannelListParser()
        channelList = getter.get_channels(content)
        return channelList
        
    def get_channels_from_file(self, f):
        """ pobiera liste kanalow z podanego pliku html """
        buf = f.read()
        getter = GazetaChannelListParser.GazetaChannelListParser()
        channelList = getter.get_channels(buf)
        return channelList

    def get_guide(self, eventDate, channel_id):
        """
        pobiera informacje z strony oraz parsuje dane, zwraca liste elementow
        klasy Event
        """
        url = self.url_provider.guide_url(eventDate, channel_id)
        f = self.http_helper.get(url, False, "ISO-8859-2")
        return self.get_guide_from_file(eventDate, channel_id, f)

    def get_guide_from_file(self, eventDate, channel_id, f):
        getter = GazetaProgrammeParser.GazetaProgrammeParser(self.parser_options)
        events = getter.get_events(eventDate, channel_id, f)
        for event in events:
            details = self.get_details(event.url)
            event.set_details(details)
        return events

    def get_details(self, relative_url):
        url = self.url_provider.details_url(relative_url)
        f = self.http_helper.get(url, True, "ISO-8859-2")
        return self.get_details_from_file(f)
    
    def get_details_from_file(self, f):
        getter = GazetaProgrammeDetailsParser.GazetaProgrammeDetailsParser("dummy")
        details = getter.get_details(f)
        return details
    