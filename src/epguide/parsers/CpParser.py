# -*- coding: utf-8 -*-

import urllib
import re

from datetime import datetime, timedelta
from lxml import etree
from lxml.cssselect import CSSSelector as css

from epguide.data_formats import Channel, Event

from roman import fromRoman, RomanError

DAY = timedelta(days=1)
MIN = timedelta(minutes=1)

class CpParser(object):
    """
    Parser pobierajacy dane z portalu Cyfry Plus
    """
    def __init__(self):
        self.url = "http://www.cyfraplus.pl/program/"
        self.encoding = "ISO-8859-2"
        self.args = {'action': 'find',
                     'full': 'F'}

        self.parser = etree.HTMLParser()
        
        self.res = {
            'title': re.compile("""
                    ^[\s-]*
                    (?P<title>.+?)                  # tytuł
                    (\s(?P<season>[0-9]{1,3}        # sezon w arabskich...
                    |(X{0,3})(IX|IV|V?I{0,3})))?    # ...lub rzymskich
                    (\:\s*(?P<sec_title>.+?))?      # podtytuł
                    \s*$
                """, re.IGNORECASE | re.VERBOSE),
            'span': re.compile(u"""
                    ^\s*
                    (\((?P<orig_title>.+)\))?       # tytuł oryginalny
                    (\s+-\xa0(?P<category>.+?))?    # kategoria
                    (?:\s+odc.\xa0(?P<episode>      # odcinek
                    (?P<episode_num>[0-9]+)         # nr odcinka
                    (/(?P<episode_count>[0-9]+))?   # ilość odcinków
                    .*))?                           # tytuł odcinka / komentarz
                    \s*$
                """, re.VERBOSE),
            'year': re.compile("[0-9]{4}(-[0-9]{4})?")
        }

    def Init(self):
        pass

    def Finish(self):
        pass

    def GetChannelList(self):
        """ pobiera liste kanalow """
        handle = urllib.urlopen (self.url)
        h = etree.parse(handle, self.parser)
        channelList = [Channel(e.text, e.get('value')) \
                       for e in css('select[name="can[]"] option')(h)]
        return channelList

    def GetGuide(self, date, channel_id):
        """
        pobiera informacje z strony oraz parsuje dane, zwraca liste elementow
        klasy Event
        """
        events = []

        d = date.strftime('%Y.%m.%d')
        args = urllib.urlencode(dict(
                self.args, 
                **{'dmin': d, 'dmax': d, 'can[]': channel_id}
        ))

        handle = urllib.urlopen(self.url, args)

        h = etree.parse(handle, self.parser)

        try:
            table = css('table.ptv-table')(h)[0]
        except IndexError:
            # brak programów tego dnia
            return events

        channel_name = css('th span')(table)[0].text.title()

        for tr in css('tbody tr')(table):
            category = []
            duration = None
            country = None
            year = None
            director = []
            cast = []
            ns = ''
        
            # czas rozpoczęcia
            span = tr[0][0]
            start_time = datetime.combine(date,
                                          datetime.strptime(span.text, '%H:%M').time())

            # jeśli czas rozpoczęcia w nocy, dodaj jeden dzień
            if start_time.hour < 6:
                start_time = start_time + DAY
        
            # dane podstawowe
            td = tr[1]
            a = css('td > a')(td)
            i = css('td > i')(td)
            span = css('td > span')(td)[0].text
            div = css('div.desc')(td)
            
            # tytuł
            if a:
                raw_title = a[0].text
            elif i:
                raw_title = i[0].tail
            else:
                raw_title = td.text

            m_title = self.res['title'].match(raw_title)
            m_span = self.res['span'].match(span)

            title = m_title.group('title').title()
            if m_title.group('sec_title'):
                sec_title = m_title.group('sec_title').title()
            else:
                sec_title = ''

            season = m_title.group('season')
            episode = m_span.group('episode')
            orig_title = m_span.group('orig_title')
            if m_span.group('category'):
                category.append(m_span.group('category'))
            episode_num = m_span.group('episode_num')
            episode_count = m_span.group('episode_count')

            if season:
                try:
                    season = fromRoman(season)
                except RomanError:
                    season = int(season)
                finally:
                    ns = '%s' % (season - 1)
                
            if episode_num and episode_count:
                ns = '%s.%s/%s' % (ns, int(episode_num) - 1, episode_count)
            elif episode_num:
                ns = '%s.%s' % (ns, int(episode_num) - 1)

            # numer odcinka w podtytule
            if season and episode and sec_title:
                sec_title = 'odc. %sx%s: %s' % (season, episode, sec_title)
            elif episode and sec_title:
                sec_title = 'odc. %s: %s' % (episode, sec_title)
            elif season and episode:
                sec_title = 'odc. %sx%s' % (season, episode)
            elif episode:
                sec_title = 'odc. %s' % episode

            # kategoria przed tytułem
            if i and 'Premiera' in i[0].text:
                premiere = True
            elif i and 'ostatni seans' in i[0].text:
                last_chance = True
            elif i:
                category.append(i[0].text.strip().lower())

            # dane dodatkowe
            if div:
                span = css('div > span')(div[0])
                br = css('div > br')(div[0])
                if span:
                    current = None
                    
                    span = span[0].text.strip()
                    splits = span.split(', ')

                    for element in splits:
                        m_year = self.res['year'].search(element)
                        if m_year:
                            year = m_year.group(0)
                        elif element.endswith('min'):
                            duration = int(element[:-4])
                        elif element.startswith(u'reż. '):
                            director.append(element[5:])
                            current = director
                        elif element.startswith('wyk. '):
                            cast.append(element[5:])
                            current = cast
                        elif current:
                            current.append(element)
                        else:
                            country = element.split('/')
                    try:
                        description = "%s; %s" % (span, br[0].tail.strip())
                    except AttributeError:
                        description = span
                else:
                    description = div[0].text.strip()
            else:
                description = ''
                
            # szczegóły transmisji
            for img in tr[2]:
                src = img.get('src')
                if 'lektor.gif' in src:
                    subtitles = True
                elif 'dolby.gif' in src:
                    stereo = 'surround'
                elif 'dolby5-1.gif' in src:
                    stereo = 'dolby digital'
                elif '16-9.gif' in src:
                    aspect = "16:9"
                elif 'hd.png' in src:
                    quality = "HDTV"
                elif 'dla_1.gif' in src:
                    pg = 0
                elif 'dla_3.gif' in src:
                    pg = 18
                elif 'dla_7.gif' in src:
                    pg = 7
                elif 'dla_12.gif' in src:
                    pg = 12
                elif 'dla_16.gif' in src:
                    pg = 16

            event = Event(channel_id, channel_name, title, sec_title,
                          ', '.join(category), description, start_time)
            events.append(event)
        return events
