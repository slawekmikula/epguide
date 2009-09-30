

class CpParser(object):
    """
    parser pobierajacy dane z strony C+
    """
    def __init__(self):
        pass

    def Init(self):
        pass

    def Finish(self):
        pass

    def GetChannelList(self):
        """ pobiera liste kanalow """
        getter = WpChannelListGetter()
        stationList = getter.GetStationList()
        channelList = []

        if getter.success:
            for station in stationList:
                # usuwamy elementy kontrolne oraz 'Wszystkie kanaly'
                if station['id'] != '---' and int(station['id']) != 0:
                    channel = Channel(station['name'], int(station['id']))
                    channelList.append(channel)

        # usuwamy duplikaty i sortujemy liste
        dict = {}
        for channel in channelList:
            dict[channel] = channel
        channelList = dict.values()
        channelList.sort()

        return channelList

    def GetGuide(self, date, channel_id):
        """
        pobiera informacje z strony oraz parsuje dane, zwraca liste elementow
        klasy Event
        """
        getter = WpProgrammeGetter()
        eventDict = getter.GetEventList(date, channel_id)
        eventClassList = []

        if getter.success:
            for event in eventDict:
                eventClass = Event(event['channel_id'], event['channel_name'],
                    event['title'], '', '', event['desc'], event['time_start'],
                    event['time_end'])
                eventClassList.append(eventClass)

        return eventClassList