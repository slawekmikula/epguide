# -*- coding: utf-8 -*-
import textwrap

class TxtOutput(object):
    """
    klasa wyjscia w formacie tekstowym
    """

    def __init__(self):
        self.file = None

    def Init(self, file):
        self.file = file
    
    def Finish(self):
        pass

    def SaveChannelList(self, channel_list):
        """
        zapisanie listy kanalow
        """
        for channel in channel_list:
            self.file.write("%s - %s\n" % (channel.id, channel.name))

    def SaveGuide(self, day, guide):
        """
        zapisanie programu
        """
        if len(guide) == 0:
            self.file.write("Brak programu dla tego dnia")
            return
        
        self.file.write(u"\nProgram %s na dzień: %s\n" % (guide[0].get_channel_name(), day.strftime("%Y-%m-%d")))
        self.file.write("--------------------------------------------\n\n")
        for item in guide:
            self.file.write(" %s %s %s | %s | %s | %s\n" % (item.time_start.strftime("%H:%M"), item.time_end and item.time_end.strftime("%H:%M") or '',
                item.get_title(), item.get_episode_num() or '', (item.get_subtitle() or ''), item.main_category))
            self.file.write(textwrap.fill (item.get_description(), 79, initial_indent=13*" ", subsequent_indent=13*" ") + "\n")

    def SaveGuideChannels(self):
        pass