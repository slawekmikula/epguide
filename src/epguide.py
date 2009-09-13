
class EpGuide:
    """
    glowna klasa aplikacji
    """
    def __init__(self, config):
        
        self.config = config
        self.parser, self.output = self.config.ProvideExec()
        
    def Execute(self):
        """
        glowna petla wykonywania zadan
        """
        if self.config.options.licence:
            self.config.PrintLicence()
        elif self.config.options.list:
            self.GetChannelList()
        elif self.config.get_guide: 
            self.GetGuide()
        else:    
            self.config.cmdparser.print_help()

    def GetChannelList(self):
        """
        pobiera liste kanalow
        """
        
        self.parser.Init()
        self.output.Init()
        channel_list = self.parser.GetChannelList()
        self.output.SaveChannelList(channel_list)
        self.parser.Finish()
        self.output.Finish()
        
    
    def GetGuide(self):
        """
        pobiera dane programu telewizyjnego
        """
        
        self.parser.Init()
        self.output.Init()
        self.output.SaveGuideChannels(self.config.options.channel_list)
        
        for iter in range((self.config.date_to - self.config.date_to).days):
            day = self.config.date_from + datetime.timedelta(days=1)
            
            for channel in self.config.options.channel_list:
                
                guide = self.parser.GetGuide(day, channel)
                self.output.SaveGuide(day, channel, guide)
                
        self.output.Finish()
        self.parser.Finish()
    
    