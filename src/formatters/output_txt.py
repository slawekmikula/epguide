
class TxtOutput(object):
    """
    klasa wyjscia w formacie tekstowym
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

    def Finish(self):
        """
        zamkniecie wyjscia
        """
        close(self.file)

    def SaveChannelList(self, channel_list):
        """
        zapisanie listy kanalow
        """
        for channel in channel_list:
           self.file.write("%s - %s\n" % (channel.id.encode('utf-8'), channel.name.encode('utf-8')))

    def SaveGuide(self, day, channel, guide):
        """
        zapisanie programu
        """
        self.file.write("%s - %s\n" % (channel.name.encode('utf-8'), day))
        for item in guide:
            self.file.write("  %s %s   %s\n" % (item.date_start, item.time_start, item.title.encode('utf-8')))
            self.file.write(textwrap.fill (item.desc, 79, initial_indent=13*" ", subsequent_indent=13*" ") + "\n")

