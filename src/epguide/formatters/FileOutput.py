import sys, textwrap

class FileOutput(object):
    """
    klasa wyjscia w formacie XMLTV
    """
    
    def __init__(self, filename, formatter):
        self.file = None
        self.filename = filename
        self.formatter = formatter
    
    def Init(self):
        """
        inicjalizacja wyjscia
        """
        if self.filename is not None:
            self.file = open(self.filename   , "w+")
        else:
            self.file = sys.stdout
        self.formatter.Init(self.file)
        
    
    def Finish(self):
        """
        zamkniecie wyjscia
        """
        self.formatter.Finish()
        if self.filename is not None:
            self.file.close()

    def SaveChannelList(self, channel_list):
        """
        zapisanie listy kanalow
        """
        self.formatter.SaveChannelList(channel_list)

    def SaveGuide(self, day, guide):
        """
        zapisanie programu
        """
        self.formatter.SaveGuide(day, guide)

    def SaveGuideChannels(self):
        self.formatter.SaveGuideChannels()
