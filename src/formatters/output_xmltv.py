
event_format="""
<programme start="%s%s00 +0100" stop="%s%s00 +0100" channel="%s">
  <title>%s</title>
  <sub-title>%s</sub-title>
  <desc>%s</desc>
  <category>%s</category>
</programme>\n 
"""

channel_format="""
<channel id="%s"><display-name lang="pl">%s</display-name></channel>\n
"""

class XmltvOutput(object):
    """
    klasa wyjscia w formacie XMLTV
    """
    
    def __init__(self, config):
        self.file = None
        self.config = config
    
    def Init(self):
        """
        inicjalizacja wyjscia
        """
        if self.config.options.output is not None:
            self.file = open(self.config.options.output)
        else:
            self.file = stdout
        
        self.file.write('<tv generator-info-name="epguide generator">\n')
    
    def Finish(self):
        """
        zamkniecie wyjscia
        """
        self.file.write('</tv>')
        close(self.file)
    
    def SaveChannelList(self, channel_list):
        """
        zapisanie listy kanalow
        """
        for channel in channel_list:
            self.file.write(channel_format % (channel.id.encode('utf-8'), channel.name.encode('utf-8')))
    
    def SaveGuide(self, day, channel, guide):
        """
        zapisanie programu
        """
        for item in guide:
            self.file.write(event_format  % ( item.date_start, item.time_start,
                       item.date_end, item.time_end, item.id.encode('utf-8'),
                       item.title.encode('utf-8'),
                       item.subtitle.encode('utf-8'),
                       item.desc.encode('utf-8'),
                       item.category.encode('utf-8')))
         