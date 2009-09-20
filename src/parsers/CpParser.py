

class CpParser(object):
    """
    parser pobierajacy dane z strony C+
    """
    def __init__(self):
        raise NotImplementedError
    
    def Init(self): 
        raise NotImplementedError
    
    def Finish(self):
        raise NotImplementedError
    
    def GetChannelList(self):
        raise NotImplementedError
    
    def GetGuide(self, date, channel_id):
        raise NotImplementedError
    
    