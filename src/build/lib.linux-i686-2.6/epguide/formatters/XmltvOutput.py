import sys, string

from epguide.data_formats import Channel, Event

event_format="""
<programme start="%s" stop="%s" channel="%s">
  <title>%s</title>
  <sub-title>%s</sub-title>
  <desc>%s</desc>
  <category>%s</category>
</programme>\n 
"""

channel_format="""<channel id="%s"><display-name lang="pl">%s</display-name></channel>\n"""

class XmltvOutput(object):
    """
    klasa wyjscia w formacie XMLTV
    """
    
    def __init__(self, config):
        self.file = None
        self.config = config
        self.channel_list = set()
    
    def Init(self):
        """
        inicjalizacja wyjscia
        """
        if self.config.options.filename is not None:
            self.file = open(self.config.options.filename   , "w+")
        else:
            self.file = sys.stdout
        
        self.file.write('<tv generator-info-name="epguide generator">\n')
    
    def Finish(self):
        """
        zamkniecie wyjscia
        """
        self.file.write('</tv>')
        self.file.close()

    def FormatString(self, txt):
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
            self.file.write(channel_format % (channel.id, channel.name.encode('utf-8')))
    
    def SaveGuide(self, day, guide):
        """
        zapisanie programu
        """
        if len(guide) == 0:
            return

        for item in guide:
            self.file.write(event_format  % (
                       item.time_start.strftime("%Y%m%d%H%M%S +0100"),
                       item.time_end.strftime("%Y%m%d%H%M%S +0100"),
                       item.channel_id,
                       self.FormatString(item.title),
                       self.FormatString(item.subtitle),
                       self.FormatString(item.desc),
                       self.FormatString(item.category)))

            self.channel_list.add(Channel(item.channel_name, int(item.channel_id)))
         
    def SaveGuideChannels(self):
        for channel in self.channel_list:
            self.file.write(channel_format % (channel.id, self.FormatString(channel.name)))