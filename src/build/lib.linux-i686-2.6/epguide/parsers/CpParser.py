from sgmllib import SGMLParser

class CpChannelListGetter(SGMLParser):
    def reset(s):
        SGMLParser.reset(s)
        s.chan = {}
        s.chans = []
        s.lista = False
        s.dane = ""

    def get_attr (s, list, name):
        for attr in list:
            if attr[0] == name:
                return attr[1]
        return None

    def start_select(s, attrs):
        if s.get_attr(attrs, "name") == "can":
            s.lista = True

    def end_select(s):
        s.lista = False

    def start_option(s, attrs):
        if s.lista:
            if s.dane and s.chan:
                s.chan['name'] = s.dane.strip().decode("iso-8859-2", "replace")
                s.chans.append(s.chan)
            s.dane = ""
            s.chan = {'id' : s.get_attr(attrs, "value"), 'name' : ""}

    def handle_data(s, tekst):
        if s.lista:
            s.dane += tekst

class CpProgrammeGetter(SGMLParser):
    def reset(s):
        SGMLParser.reset(s)
        s.state = []
        s.programs = []
        s.chans = []
        s.i = ""
        s.s_start ("HTML")

        s.months = {'sty' : 1,
                    'lut' : 2,
                    'mar' : 3,
                    'kwi' : 4,
                    'maj' : 5,
                    'cze' : 6,
                    'lip' : 7,
                    'sie' : 8,
                    'wrz' : 9,
                    'pa\xbc' : 10,
                    'lis' : 11,
                    'gru' : 12}

        s.eps = re.compile("[0-9]+(/[0-9]+)?")
        s.tit = re.compile("(: )?(?P<title>[^\(]*?)(\((?P<org>[^\)]+)\))? -")
        s.dat = re.compile("([0-9]+) (.{3})")
        s.chan = common.Channel()
        s.data = ""
        s.success = False

    def close (s):
        if s.programs and s.chan.channel:
            s.chan.chanid = re.sub("[^a-z0-9]", "", s.chan.channel.decode('iso-8859-2', 'replace').strip().lower())+".cplus"
            s.chan.channel = s.chan.channel.decode('iso-8859-2', 'replace').strip()
            s.chan.programs = s.programs
            s.chans.append(s.chan)
            s.success = True
        SGMLParser.close (s)
        s.s_end ("HTML")

    def get_attr (s, list, name):
        for attr in list:
            if attr[0] == name:
                return attr[1]
        return None

    def start_h1(s, attrs):
        s.s_start("KANAL")
        s.s_start("name")
        if s.programs and s.chan.channel:
            s.chan.chanid = re.sub("[^a-z0-9]", "", s.chan.channel.decode('iso-8859-2', 'replace').strip().lower())+".cplus"
            s.chan.channel = s.chan.channel.decode('iso-8859-2', 'replace').strip()
            s.chan.programs = s.programs
            s.chans.append(s.chan)
        s.programs = []
        s.chan = common.Channel()

    def end_h1(s):
        if "name" in s.state:
            s.s_end ("name")
            s.s_switch ("DATA")

    def start_tr(s, attrs):
        if s.get_attr(attrs, "bgcolor") == "#27487D":
            s.s_start("TR")
            s.s_start("PROGRAM")
            s.program = {'time' : "", 'title' : "", 'sub-title' : "", 'cat' : [], 'tmp' : [], 'desc' : "", 'add' : [], "ep" : ""}

    def end_tr (s):
        if "INNE" in s.state:
            s.s_end ("INNE")
        if "TR" in s.state:
            s.s_end ("TR")

    def start_td (s, attrs):
        if s.state[-1] == "PROGRAM":
            s.s_start("godzina")
        if s.state[-1] == "TYTUL":
            s.s_start("tytul")
        if s.state[-1] == "INNE":
            s.s_start("inne")

    def end_td (s):
        if "godzina" in s.state:
            s.s_switch ("TYTUL")
        if "opis" in s.state or "kategoria" in s.state or "podtytul" in s.state:
            s.s_end ("TYTUL")
            s.s_switch ("INNE")
        if "inne" in s.state:
            tit = s.tit.match(s.program['sub-title'])
            if tit:
                if tit.group('title'):
                    s.program['sub-title'] = tit.group('title').strip()
                else:
                    s.program['sub-title'] = ""
                if tit.group('org'):
                    s.program['desc'] = "(org.: "+tit.group('org').strip()+")\n"+s.program['desc'].strip()
                else:
                    s.program['desc'] = s.program['desc'].strip()
            elif s.program['sub-title'] == "-" or s.program['sub-title'] == "odc.":
                s.program['sub-title'] = ""
            for v in s.program['tmp']:
                if s.eps.match(v):
                    s.program['ep'] = v
                    if s.program['sub-title']:
                        s.program['sub-title'] = "odc. "+v+": "+s.program['sub-title'].strip()
                    else:
                        s.program['sub-title'] = "odc. "+v
                elif v == "Premiera":
                    s.program['add'].append("prem")
                else:
                    s.program['cat'].append(v)
            del s.program['tmp']
            s.programs.append(s.program)

    def start_b (s, attrs):
        if s.state[-1] == "DATA":
            s.s_start("data")
        if s.state[-1] == "TYTUL":
            s.s_start("tytul")

    def end_b (s):
        if "data" in s.state:
            s.s_end ("data")
            s.s_end ("DATA")
        if "tytul" in s.state:
            s.s_switch ("podtytul")

    def start_i (s, attrs):
        if s.state[-1] == "tytul":
            s.s_switch ("kategoria")

    def end_i (s):
        if "kategoria" in s.state:
            s.s_switch ("tytul")

    def start_a (s, attrs):
        if s.state[-1] == "TYTUL":
            s.s_start ("tytul")

    def end_a (s):
        if "tytul" in s.state:
            s.s_switch ("opis")

    def handle_entityref(s, ref):
        if s.state[-1] == "podtytul":
            s.s_switch ("kategoria")

    def start_br (s, attrs):
        if s.state[-1] == "kategoria" or s.state[-1] == "podtytul":
            s.s_switch ("opis")
        if s.state[-1] == "opis":
            s.program['desc'] += "\n"

    def start_img (s, attrs):
        if s.state[-1] == "inne":
            s.program['add'].append(s.get_attr(attrs, "src")[39:-4])

    def handle_data(s, data):
        data = data.strip()
        if s.state[-1] == "name":
            s.chan.channel += data+" "
        if s.state[-1] == "data":
            s.data = s.dat.match(data)
            s.chan.date = time.strptime (s.data.group(1)+"."+str(s.months[s.data.group(2)])+"."+s.rok, "%d.%m.%Y")
        if s.state[-1] == "godzina":
            s.program['time'] = data
        if s.state[-1] == "tytul":
            s.program['title'] += data
        if s.state[-1] == "kategoria":
            s.program['tmp'].append(data.replace("  odc.",""))
        if s.state[-1] == "podtytul":
            s.program['sub-title'] += data.strip()
        if s.state[-1] == "opis":
            s.program['desc'] += data.strip()

    def s_start (s, state):
        s.state.append (state)
        s.i += "  "

    def s_end (s, state):
        i = 2
        while s.state.pop() != state:
          i += 2
        s.i = s.i[:-i]

    def s_switch (s, state):
        s.state[-1] = state


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
        getter = CpChannelListGetter()
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
        getter = CpProgrammeGetter()
        eventDict = getter.GetEventList(date, channel_id)
        eventClassList = []

        if getter.success:
            for event in eventDict:
                eventClass = Event(event['channel_id'], event['channel_name'],
                    event['title'], '', '', event['desc'], event['time_start'],
                    event['time_end'])
                eventClassList.append(eventClass)

        return eventClassList