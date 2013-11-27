# -*- coding: utf-8 -*-
import time
import string
import logging

class XmltvOutput(object):
    """
    klasa wyjscia w formacie XMLTV
    """
    
    
    header = """<?xml version='1.0' encoding='utf-8'?>
<!DOCTYPE tv SYSTEM "xmltv.dtd">
<tv generator-info-name="epguide generator">\n"""
#<!ELEMENT programme (title+, sub-title*, desc*, credits?, date?,
#                     category*, language?, orig-language?, length?,
#                     icon*, url*, country*, episode-num*, video?, audio?,
#                     previously-shown?, premiere?, last-chance?, new?,
#                     subtitles*, rating*, star-rating*, review* )>    
# <programme start="200006031633" channel="3sat.de">
    event_start_format = """  <programme start="%s %s" %schannel="%s">\n"""
#    <title lang="de">blah</title>
    title_format = """    <title>%s</title>\n"""
#    <title lang="en">blah</title>
    subtitle_format = """    <sub-title>%s</sub-title>\n"""
#    <desc lang="de">
#       Blah Blah Blah.
#    </desc>
    desc_format = """    <desc>%s</desc>\n"""
#    <credits>
#      <director>blah</director>
#      <actor>a</actor>
#      <actor>b</actor>
#    </credits>
#    <date>19901011</date>
    year_format = """    <date>%s</date>\n"""
    main_category_format = """    <category language="en">%s</category>\n"""
    category_format = """    <category language="pl">%s</category>\n"""
    programme_icon_format = """    <icon src="%s"/>\n"""
#    <country>ES</country>
    country_format = """    <country>%s</country>\n"""
#    <episode-num system="xmltv_ns">2 . 9 . 0/1</episode-num>
    episode_num_format = """    <episode-num system="onscreen">%s</episode-num>\n"""
#    <video>
#      <aspect>16:9</aspect>
#    </video>
#    <rating system="MPAA">
#      <value>PG</value>
#      <icon src="pg_symbol.png" />
#    </rating>
    pg_format = """    <rating system="pl"><value>%s</value></rating>\n"""
#    <star-rating>
#      <value>3/3</value>
#    </star-rating>
    star_rating_format = """    <star-rating><value>%s</value></star-rating>\n"""
#  </programme>
    event_end_format = """  </programme>\n"""
    
    channel_format = """  <channel id="%s"><display-name lang="pl">%s</display-name>%s</channel>\n"""

    channel_icon_format = """<icon src="%s"/>"""
    
    def __init__(self):
        self.file = None
        self.channel_list = set()
        self.log = logging.getLogger("XmltvOutput")

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
        self.file.write(self.header)
    
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

    def _cdata_string(self, txt):
        formatTxt = u"<![CDATA["+txt+u"]]>"
        formatTxt = formatTxt.encode('utf-8')
        return formatTxt


    def _channel_element(self, channel):
        return self.channel_format % (channel.id, self._format_string(channel.name), self._optional_element(self.channel_icon_format, channel.icon_url))

    def SaveChannelList(self, channel_list):
        """
        zapisanie listy kanalow
        """
        for channel in channel_list:
            self.file.write(self._channel_element(channel))
    
    def _optional_element(self, elementFormat, elementValue):
        if elementValue:
            return elementFormat % (self._format_string(elementValue))
        else:
            return ''

    def _optional_element_cdata(self, elementFormat, elementValue):
        if elementValue:
            return elementFormat % (self._cdata_string(elementValue))
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
            episode_num_element = self._optional_element(self.episode_num_format, item.get_episode_num())
            title_element = self._element(self.title_format, item.get_title())
            subtitle_element = self._optional_element(self.subtitle_format, item.get_subtitle())
            desc_element = self._optional_element_cdata(self.desc_format, item.get_description())
            main_category_element = self._optional_element(self.main_category_format, item.main_category)
            category_element = self._element(self.category_format, item.category)
            icon_element = self._optional_element(self.programme_icon_format, item.get_icon_url())
            year_element = self._optional_element(self.year_format, item.get_year())
            country_element = self._optional_element(self.country_format, item.get_country())
            pg_element = self._optional_element(self.pg_format, item.get_pg())
            star_rating_element = self._optional_element(self.star_rating_format, item.get_star_rating())

            element_start = self.event_start_format % (
                       item.time_start.strftime("%Y%m%d%H%M%S"),
                       self.tz,
                       item.time_end and \
                            'stop="%s %s" ' % \
                                (item.time_end.strftime("%Y%m%d%H%M%S"),
                                 self.tz) or '',
                       item.get_channel_id())
            
            element = element_start + \
                title_element + \
                subtitle_element + \
                desc_element + \
                year_element + \
                main_category_element + \
                category_element + \
                icon_element +\
                country_element + \
                episode_num_element + \
                pg_element + \
                star_rating_element + \
                self.event_end_format
            self.file.write(element)

            self.log.debug("item channel: id: %s name: %s icon_url: %s", item.get_channel_id(), item.get_channel_name(), item.get_channel_icon_url())
            if item.get_channel_name != '':
                self.channel_list.add(item.channel)
         
    def SaveGuideChannels(self):
        for channel in self.channel_list:
            self.file.write(self._channel_element(channel))
