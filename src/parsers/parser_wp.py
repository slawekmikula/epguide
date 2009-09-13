

class WpGetter(SGMLParser):
    def __init__(self):
        self.program_id = ""
        self.program_name = ""
        self.event_date = ""
    
    
       

class WpParser(object):
    """
    parser pobierajacy dane z Wp.pl
    """ 
    def __init__(self):
        self.url_template = "http://tv.wp.pl/index_druk.html?T[date]=%s&T[station]=%s&T[time]=0"
   
    def Init(self): 
        pass
    
    def Finish(self):
        pass
    
    def GetChannelList(self):
        pass
    
    def GetGuide(self, date, channel_id):
        """
        pobiera informacje z strony oraz parsuje dane, zwraca liste elementow
        klasy Event
        """
        event_list = []
    
        url = self.url_template % (date, channel_id) 
        buffer = urllib.urlopen (url).read()
        events_getter = WpGetter()
        event_getter.feed(buffer)
        event_list = event_getter.GetEventList()
        
        return event_list
        
        # ---------- OLD --------------
    
        start_next_day = False
        end_next_day = False
        
        for i in range(len(parser.programs)):

            prog = parser.programs[i]

            uni_title = prog['title'].decode('iso-8859-2', 'replace').replace(u"&",u"&amp;")
            uni_subtitle = prog['sub-title'].decode('iso-8859-2', 'replace').replace(u"&",u"&amp;")
            uni_category = "</category>\n<category>".join(prog['cat']).decode('iso-8859-2', 'replace')
            uni_desc = prog['desc'].decode('iso-8859-2', 'replace')
            # replace & signs with &amp;
            uni_desc = string.replace(uni_desc, u"&",u"&amp;")
            uni_desc = string.replace(uni_desc, u"<",u"")
            uni_desc = string.replace(uni_desc, u">",u"")            

            # data zakonczenia rowna startowi nastepnego programu, lub
            # jesli to ostatni program rowna startowi aktualnego
            if i == len(parser.programs)- 1:
                last_time = prog['time']
            else :
                last_time = parser.programs[i+1]['time']

            # data rozpoczecia i konca rowna dacie w parserze
            date_start = time.strftime("%Y%m%d", parser.date)
            date_end = time.strftime("%Y%m%d", parser.date)

            # czas rozpoczecia rowny czasowi audycji, zakonczenia rowny
            # wyliczonemu czasowi powyzej
            time_start = prog['time'].replace(':','')
            time_end = last_time.replace(':','')

            # gdy godzina konca jest w nastepnym dniu
            if int(time_end) < int(time_start) :
                end_next_day = True

            # gdy godzina startu jest w nastepnym dniu
            if int(time_start) < int(parser.programs[i-1]['time'].replace(':','')) :
                start_next_day = True

            year_start = year_end = time.strftime ("%Y", parser.date)

            month_start = month_end = time.strftime ("%m", parser.date)
            month_start = month_end = int(month_start)
            dayInMonth = monthTable[month_start - 1]
            
            day_start = day_end = time.strftime ("%d", parser.date)
            day_start = day_end = int(day_start)          

            if start_next_day == True:
                day_start = day_start + 1
                if day_start > dayInMonth :
                    day_start = 1
                    month_start = month_start + 1
                    if month_start > 12:
                        month_start = 1
                    
                day_start = str(day_start)
                month_start = str(month_start)                
                if len(day_start) == 1:
                    day_start = "0" + day_start
                if len(month_start) == 1:
                    month_start = "0" + month_start
                    
                date_start =  str(year_start) + str(month_start) + str(day_start)
                
            if end_next_day == True:
                day_end = day_end + 1
                if day_end > dayInMonth :
                    day_end = 1
                    month_end = month_end + 1
                    if month_end > 12 :
                        month_end = 1

                day_end = str(day_end)
                month_end = str(month_end)                
                if len(day_end) == 1:
                    day_end = "0" + day_end
                if len(month_end) == 1:
                    month_end = "0" + month_end
                   
                    
                date_end =  str(year_end) + str(month_end) + str(day_end)
                        
        
 
    