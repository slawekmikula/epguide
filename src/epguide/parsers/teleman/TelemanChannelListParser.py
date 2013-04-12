# -*- coding: utf-8 -*-
from sgmllib import SGMLParser
import time
import datetime
import urllib
import re
from httplib2 import Http, FileCache
import httplib2
import os

from epguide.data_formats import Channel, Event


    
class TelemanChannelListParser(SGMLParser):
    def __init__(self):
        SGMLParser.__init__ (self)

        self.channels_data = []
        self.state = ['init']
        self.current_href = None
        self.success = False

    def get_channels(self, buf):
        station_list = self._get_channels_data(buf)
        channel_list = [Channel(station['name'], station['id']) for station in station_list]

        # usuwamy duplikaty i sortujemy liste
        channel_set = {}
        for channel in channel_list:
            channel_set[channel] = channel
        channel_list = channel_set.values()
        channel_list.sort()

        return channel_list
    
    def _get_channels_data(self, buf):
        self.feed(buf)
        self.close()
        return self.channels_data
    

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
