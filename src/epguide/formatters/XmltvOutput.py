# -*- coding: utf-8 -*-
import time
import sys, string

from epguide.data_formats import Channel, Event


class XmltvOutput(object):
    """
    klasa wyjscia w formacie XMLTV
    """
    event_start_format = """  <programme start="%s %s" %schannel="%s">\n"""
    event_end_format = """  </programme>\n"""
    title_format = """    <title>%s</title>\n"""
    subtitle_format = """    <sub-title>%s</sub-title>\n"""
    desc_format = """    <desc>%s</desc>\n"""
    main_category_format = """    <category language="en">%s</category>\n"""
    category_format = """    <category language="pl">%s</category>\n"""
    episode_num_format = """    <episode-num system="onscreen">%s</episode-num>\n"""
    
    channel_format = """  <channel id="%s"><display-name lang="pl">%s</display-name></channel>\n"""
    
    def __init__(self):
        self.file = None
        self.channel_list = set()

        # strefa czasowa aktualna
        if time.localtime(time.time()).tm_isdst and time.daylight:
            self.tz = time.altzone / 60 / 60
        else:
            self.tz = time.timezone / 60 / 60

        if self.tz > 0:
            sign = "-"  # zmieniamy znak bo to roznica DO UTC (a nie od)
        else:
            sign = "+"
        self.tz = "%s0%s00" % (sign, abs(self.tz))

    
    def Init(self, file):
        """
        inicjalizacja wyjscia
        """
        self.file = file
        self.file.write('<tv generator-info-name="epguide generator">\n')
    
    def Finish(self):
        """
        zamkniecie wyjscia
        """
        self.file.write('</tv>\n')

    def _format_string(self, txt):
        formatTxt = string.replace(txt, u"&", u"&amp;")
        formatTxt = string.replace(formatTxt, u"<", u"")
        formatTxt = string.replace(formatTxt, u">", u"")
        formatTxt = formatTxt.encode('utf-8')
        return formatTxt

    def SaveChannelList(self, channel_list):
        """
        zapisanie listy kanalow
        """
        for channel in channel_list:
            self.file.write(self.channel_format % (channel.id, self._format_string(channel.name)))
    
    def _optional_element(self, elementFormat, elementValue):
        if elementValue:
            return elementFormat % (self._format_string(elementValue))
        else:
            return ''

    def _element(self, elementFormat, elementValue):
        return elementFormat % (self._format_string(elementValue))

    def SaveGuide(self, day, guide):
        """
        zapisanie programu
        """
        if len(guide) == 0:
            return

        for item in guide:
            episode_num_element = self._optional_element(self.episode_num_format, item.episode_num)
            title_element = self._element(self.title_format, item.title)
            subtitle_element = self._optional_element(self.subtitle_format, item.subtitle)
            desc_element = self._optional_element(self.desc_format, item.get_description())
            main_category_element = self._optional_element(self.main_category_format, item.main_category)
            category_element = self._element(self.category_format, item.category)

            element_start = self.event_start_format % (
                       item.time_start.strftime("%Y%m%d%H%M%S"),
                       self.tz,
                       item.time_end and \
                            'stop="%s %s" ' % \
                                (item.time_end.strftime("%Y%m%d%H%M%S"),
                                 self.tz) or '',
                       item.channel_id)
            
            element = element_start + title_element + subtitle_element + desc_element + main_category_element + category_element + episode_num_element + self.event_end_format            
            self.file.write(element)

            if item.channel_name != '':
                self.channel_list.add(Channel(item.channel_name, item.channel_id))
         
    def SaveGuideChannels(self):
        for channel in self.channel_list:
            self.file.write(self.channel_format % (channel.id, self._format_string(channel.name)))
