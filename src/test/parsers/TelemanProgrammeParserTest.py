# -*- coding: utf-8 -*-
from epguide.parsers.teleman import TelemanProgrammeParser
import datetime
import unittest
import codecs

class  TelemanProgrammeParserTest(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None 
        pass

    def tearDown(self):
        pass

    def testChannelSplitTitle(self):
        p = TelemanProgrammeParser.TelemanProgrammeParser(split_title=True)
        f = codecs.open("TVP-1.html", "r", "UTF-8")
        buf = f.read()
        eventDate = datetime.datetime(2013, 1, 1)
        channel_id = "TVP-1"
        events = [str(c) for c in p.get_events(eventDate, channel_id, buf)]
        f.close()
        print 'actual events:\n[\n"' + '",\n"'.join(events) + '"\n]'
        
        expected = [  'Event(channel_id:\'TVP-1\', channel_name:\'TVP 1\', time_start:\'2013-01-01 23:45:00\', time_end:\'2013-01-02 00:35:00\', title:\'Sylwester z"Jak\xc4\x85 to melodi\xc4\x85"\', subtitle:\'\', episode_num:\'\', main_category:\'Leisure hobbies\', category:\'teleturniej muzyczny\', desc:\'\')',
  "Event(channel_id:'TVP-1', channel_name:'TVP 1', time_start:'2013-01-02 00:35:00', time_end:'2013-01-02 02:10:00', title:'Legalna blondynka', subtitle:'', episode_num:'', main_category:'Movie/Drama', category:'komedia, USA 2001', desc:'Pi\xc4\x99kna Elle chce udowodni\xc4\x87 by\xc5\x82emu ukochanemu, \xc5\xbce nie tylko uroda jest jej atutem.\\n')",
  "Event(channel_id:'TVP-1', channel_name:'TVP 1', time_start:'2013-01-02 02:10:00', time_end:'2013-01-02 03:50:00', title:'Liberator 2', subtitle:'', episode_num:'', main_category:'Movie/Drama', category:'film sensacyjny, USA 1995', desc:'Terrory\xc5\x9bci opanowuj\xc4\x85 luksusowy poci\xc4\x85g. W\xc5\x9br\xc3\xb3d pasa\xc5\xbcer\xc3\xb3w jest komandos.\\n')",
  "Event(channel_id:'TVP-1', channel_name:'TVP 1', time_start:'2013-01-02 03:50:00', time_end:'2013-01-02 04:20:00', title:'Jaka to melodia?', subtitle:'', episode_num:'', main_category:'Leisure hobbies', category:'fina\xc5\x82 grudnia', desc:'W prowadzonym przez Roberta Janowskiego programie uczestnicy odgaduj\xc4\x85 znane przeboje muzyki rozrywkowej.\\n')",
  "Event(channel_id:'TVP-1', channel_name:'TVP 1', time_start:'2013-01-02 04:20:00', time_end:'2013-01-02 04:20:00', title:'Zako\xc5\x84czenie programu', subtitle:'', episode_num:'', main_category:'News/Current affairs', category:'', desc:'')",
  "Event(channel_id:'TVP-1', channel_name:'TVP 1', time_start:'2013-01-02 04:20:00', time_end:'2013-01-02 05:25:00', title:'Zako\xc5\x84czenie programu', subtitle:'', episode_num:'', main_category:'News/Current affairs', category:'', desc:'')",
  "Event(channel_id:'TVP-1', channel_name:'TVP 1', time_start:'2013-01-02 05:25:00', time_end:'2013-01-02 07:00:00', title:'Legenda', subtitle:'', episode_num:'', main_category:'Movie/Drama', category:'film fantasy, Wielka Brytania/USA 1985', desc:'Nominacja do Oscara za charakteryzacj\xc4\x99.\\n')",
  "Event(channel_id:'TVP-1', channel_name:'TVP 1', time_start:'2013-01-02 07:00:00', time_end:'2013-01-02 08:00:00', title:'Transmisja mszy \xc5\x9bwi\xc4\x99tej z Sanktuarium Bo\xc5\xbcego Mi\xc5\x82osierdzia w Krakowie-\xc5\x81agiewnikach', subtitle:'', episode_num:'', main_category:'News/Current affairs', category:'', desc:'Zobaczymy transmisj\xc4\x99 mszy \xc5\x9bwi\xc4\x99tej odprawianej w Sanktuarium Bo\xc5\xbcego Mi\xc5\x82osierdzia znajduj\xc4\x85cego si\xc4\x99 w Krakowie \xc5\x81agiewnikach.\\n')",
  "Event(channel_id:'TVP-1', channel_name:'TVP 1', time_start:'2013-01-02 08:00:00', time_end:'2013-01-02 09:25:00', title:'Niebieski s\xc5\x82o\xc5\x84', subtitle:'', episode_num:'', main_category:'Children's/Youth programmes', category:'film animowany, Tajlandia 2008', desc:'Birma\xc5\x84czycy rozbijaj\xc4\x85 ob\xc3\xb3z. Ma\xc5\x82y s\xc5\x82onik Khan Kluay zakrada si\xc4\x99 tam w poszukiwaniu taty i omal nie zostaje pojmany. Pomaga mu ...\\n')",
  "Event(channel_id:'TVP-1', channel_name:'TVP 1', time_start:'2013-01-02 09:25:00', time_end:'2013-01-02 11:00:00', title:'Skok z kosmosu. Felix Baumgartner', subtitle:'', episode_num:'', main_category:'Movie/Drama', category:'film dokumentalny, Wielka Brytania 2012', desc:'14 pa\xc5\xbadziernika 2012 r. austriacki spadochroniarz Felix Baumgartner wykona\xc5\x82 skok ze stratosfery, bij\xc4\x85c m.in. rekord wysoko\xc5\x9bci skoku.\\n')",
  "Event(channel_id:'TVP-1', channel_name:'TVP 1', time_start:'2013-01-02 11:00:00', time_end:'2013-01-02 12:00:00', title:'Sportowe wydarzenia 2012', subtitle:'', episode_num:'', main_category:'Sports', category:'magazyn sportowy', desc:'')",
  "Event(channel_id:'TVP-1', channel_name:'TVP 1', time_start:'2013-01-02 12:00:00', time_end:'2013-01-02 12:15:00', title:'Anio\xc5\x82 Pa\xc5\x84ski', subtitle:'', episode_num:'', main_category:'News/Current affairs', category:'', desc:'Transmisja tradycyjnej modlitwy Anio\xc5\x82 Pa\xc5\x84ski odmawianej z wiernymi przez Ojca \xc5\x9awi\xc4\x99tego w Bazylice \xc5\x9awi\xc4\x99tego Piotra w Watykanie.\\n')",
  "Event(channel_id:'TVP-1', channel_name:'TVP 1', time_start:'2013-01-02 12:15:00', time_end:'2013-01-02 13:50:00', title:'Podr\xc3\xb3\xc5\xbc do wn\xc4\x99trza Ziemi', subtitle:'', episode_num:'', main_category:'Movie/Drama', category:'film przygodowy, Kanada/USA 2008', desc:'XIX wiek. Do prof. Brocka przychodzi \xc5\xbcona jego kolegi, kt\xc3\xb3ry nie wr\xc3\xb3ci\xc5\x82 z wyprawy do wn\xc4\x99trza Ziemi. Ma map\xc4\x99 z ...\\n')",
  "Event(channel_id:'TVP-1', channel_name:'TVP 1', time_start:'2013-01-02 13:50:00', time_end:'2013-01-02 14:00:00', title:'Skoki narciarskie', subtitle:'Turniej Czterech Skoczni w Garmisch-Partenkirchen', episode_num:'', main_category:'Sports', category:'studio', desc:'')",
  "Event(channel_id:'TVP-1', channel_name:'TVP 1', time_start:'2013-01-02 14:00:00', time_end:'2013-01-02 16:10:00', title:'Skoki narciarskie', subtitle:'Turniej Czterech Skoczni w Garmisch-Partenkirchen', episode_num:'', main_category:'Sports', category:'skoki narciarskie', desc:'Noworoczny konkurs w Garmisch- Partenkirchen to drugie zawody Turnieju Czterech Skoczni. Jednym z faworyt\xc3\xb3w jest Gregor Schlierenzauer.\\n')",
  "Event(channel_id:'TVP-1', channel_name:'TVP 1', time_start:'2013-01-02 16:10:00', time_end:'2013-01-02 16:25:00', title:'Tylko hity! Opole 2012', subtitle:'Maciej Stuhr', episode_num:'', main_category:'Leisure hobbies', category:'koncert', desc:'Przegl\xc4\x85d najwi\xc4\x99kszych przeboj\xc3\xb3w, jakie zosta\xc5\x82y zaprezentowane podczas koncert\xc3\xb3w na tegorocznym, 49. KFPP w Opolu.\\n')",
  "Event(channel_id:'TVP-1', channel_name:'TVP 1', time_start:'2013-01-02 16:25:00', time_end:'2013-01-02 16:55:00', title:'Gwiazdy w Jedynce', subtitle:'II Divo', episode_num:'', main_category:'Leisure hobbies', category:'koncert', desc:'')",
  "Event(channel_id:'TVP-1', channel_name:'TVP 1', time_start:'2013-01-02 16:55:00', time_end:'2013-01-02 17:10:00', title:'Teleexpress', subtitle:'', episode_num:'', main_category:'News/Current affairs', category:'', desc:'Dynamicznie prowadzony serwis informacyjny prezentuj\xc4\x85cy aktualne wydarzenia, wiadomo\xc5\x9bci kulturalne oraz ciekawostki z kraju i ze \xc5\x9bwiata.\\n')",
  "Event(channel_id:'TVP-1', channel_name:'TVP 1', time_start:'2013-01-02 17:10:00', time_end:'2013-01-02 17:15:00', title:'Pogoda', subtitle:'', episode_num:'', main_category:'News/Current affairs', category:'', desc:'Szczeg\xc3\xb3\xc5\x82owe informacje na temat stanu pogody w najbli\xc5\xbcszych dniach.\\n')",
  "Event(channel_id:'TVP-1', channel_name:'TVP 1', time_start:'2013-01-02 17:15:00', time_end:'2013-01-02 17:45:00', title:'Jaka to melodia?', subtitle:'', episode_num:'', main_category:'Leisure hobbies', category:'fina\xc5\x82 roku', desc:'W prowadzonym przez Roberta Janowskiego programie uczestnicy odgaduj\xc4\x85 znane przeboje muzyki rozrywkowej.\\n')",
  "Event(channel_id:'TVP-1', channel_name:'TVP 1', time_start:'2013-01-02 17:45:00', time_end:'2013-01-02 19:30:00', title:'Wall-E', subtitle:'', episode_num:'', main_category:'Children's/Youth programmes', category:'film animowany, USA 2008', desc:'Historia mi\xc5\x82o\xc5\x9bci dwojga robot\xc3\xb3w.\\n')",
  "Event(channel_id:'TVP-1', channel_name:'TVP 1', time_start:'2013-01-02 19:30:00', time_end:'2013-01-02 20:00:00', title:'Wiadomo\xc5\x9bci', subtitle:'', episode_num:'', main_category:'News/Current affairs', category:'', desc:'Serwis informacyjny prezentuj\xc4\x85cy najnowsze wydarzenia z kraju i ze \xc5\x9bwiata, m.in. z dziedziny polityki, gospodarki, kultury.\\n')",
  "Event(channel_id:'TVP-1', channel_name:'TVP 1', time_start:'2013-01-02 20:00:00', time_end:'2013-01-02 20:05:00', title:'Sport', subtitle:'', episode_num:'', main_category:'Sports', category:'', desc:'Przegl\xc4\x85d najwa\xc5\xbcniejszych aktualnych wydarze\xc5\x84 sportowych ze szczeg\xc3\xb3lnym uwzgl\xc4\x99dnieniem osi\xc4\x85gni\xc4\x99\xc4\x87 polskich zawodnik\xc3\xb3w.\\n')",
  "Event(channel_id:'TVP-1', channel_name:'TVP 1', time_start:'2013-01-02 20:05:00', time_end:'2013-01-02 20:20:00', title:'Pogoda', subtitle:'', episode_num:'', main_category:'News/Current affairs', category:'', desc:'Szczeg\xc3\xb3\xc5\x82owe informacje na temat stanu pogody w najbli\xc5\xbcszych dniach.\\n')",
  "Event(channel_id:'TVP-1', channel_name:'TVP 1', time_start:'2013-01-02 20:20:00', time_end:'2013-01-02 22:05:00', title:'Legalna blondynka', subtitle:'', episode_num:'', main_category:'Movie/Drama', category:'komedia, USA 2001', desc:'Pi\xc4\x99kna Elle chce udowodni\xc4\x87 by\xc5\x82emu ukochanemu, \xc5\xbce nie tylko uroda jest jej atutem.\\n')",
  "Event(channel_id:'TVP-1', channel_name:'TVP 1', time_start:'2013-01-02 22:05:00', time_end:'2013-01-02 23:55:00', title:'Liberator 2', subtitle:'', episode_num:'', main_category:'Movie/Drama', category:'film sensacyjny, USA 1995', desc:'Terrory\xc5\x9bci opanowuj\xc4\x85 luksusowy poci\xc4\x85g. W\xc5\x9br\xc3\xb3d pasa\xc5\xbcer\xc3\xb3w jest komandos.\\n')",
  "Event(channel_id:'TVP-1', channel_name:'TVP 1', time_start:'2013-01-02 23:55:00', time_end:'2013-01-02 01:20:00', title:'Hell Ride', subtitle:'', episode_num:'', main_category:'Movie/Drama', category:'film sensacyjny, USA 2008', desc:'Johnny zwany Pistolero jest przyw\xc3\xb3dc\xc4\x85 gangu motocyklowego\\n'\\nThe Victors\\n'\\n. Jego celem jest zemsta na liderach grupy\\n'\\nThe 666ers\\n'\\n.\\n')",
  "Event(channel_id:'TVP-1', channel_name:'TVP 1', time_start:'2013-01-02 01:20:00', time_end:'2013-01-02 03:20:00', title:'Underworld', subtitle:'', episode_num:'', main_category:'Movie/Drama', category:'horror, Niemcy/Wielka Brytania/USA/W\xc4\x99gry 2003', desc:'Student trafia w \xc5\x9brodek wojny tocz\xc4\x85cej si\xc4\x99 mi\xc4\x99dzy wampirami a wilko\xc5\x82akami.\\n')",
  "Event(channel_id:'TVP-1', channel_name:'TVP 1', time_start:'2013-01-02 03:20:00', time_end:'2013-01-02 04:20:00', title:'Zagadkowa Jedynka', subtitle:'', episode_num:'', main_category:'Leisure hobbies', category:'program rozrywkowy', desc:'W tej zabawie do zdobycia s\xc4\x85 nagrody pieni\xc4\x99\xc5\xbcne. Wystarczy telefonicznie lub za pomoc\xc4\x85 sms-a poda\xc4\x87 prawid\xc5\x82owe rozwi\xc4\x85zanie zagadki s\xc5\x82ownej.\\n')",
  "Event(channel_id:'TVP-1', channel_name:'TVP 1', time_start:'2013-01-02 04:20:00', time_end:'2013-01-02 04:20:00', title:'Zako\xc5\x84czenie programu', subtitle:'', episode_num:'', main_category:'News/Current affairs', category:'', desc:'')"]
        self.assertEqual(events, expected)

    def testChannelNoSplitTitle(self):
        p = TelemanProgrammeParser.TelemanProgrammeParser(False)
        f = codecs.open("TVP-1.html", "r", "UTF-8")
        buf = f.read()
        eventDate = datetime.datetime(2013, 1, 1)
        channel_id = "TVP-1"
        events = [str(c) for c in p.get_events(eventDate, channel_id, buf)]
        f.close()
        print 'actual events:\n[\n"' + '",\n"'.join(events) + '"\n]'
        
        expected = [  'Event(channel_id:\'TVP-1\', channel_name:\'TVP 1\', time_start:\'2013-01-01 23:45:00\', time_end:\'2013-01-02 00:35:00\', title:\'Sylwester z"Jak\xc4\x85 to melodi\xc4\x85"\', subtitle:\'\', episode_num:\'\', main_category:\'Leisure hobbies\', category:\'teleturniej muzyczny\', desc:\'\')',
  "Event(channel_id:'TVP-1', channel_name:'TVP 1', time_start:'2013-01-02 00:35:00', time_end:'2013-01-02 02:10:00', title:'Legalna blondynka', subtitle:'', episode_num:'', main_category:'Movie/Drama', category:'komedia, USA 2001', desc:'Pi\xc4\x99kna Elle chce udowodni\xc4\x87 by\xc5\x82emu ukochanemu, \xc5\xbce nie tylko uroda jest jej atutem.\\n')",
  "Event(channel_id:'TVP-1', channel_name:'TVP 1', time_start:'2013-01-02 02:10:00', time_end:'2013-01-02 03:50:00', title:'Liberator 2', subtitle:'', episode_num:'', main_category:'Movie/Drama', category:'film sensacyjny, USA 1995', desc:'Terrory\xc5\x9bci opanowuj\xc4\x85 luksusowy poci\xc4\x85g. W\xc5\x9br\xc3\xb3d pasa\xc5\xbcer\xc3\xb3w jest komandos.\\n')",
  "Event(channel_id:'TVP-1', channel_name:'TVP 1', time_start:'2013-01-02 03:50:00', time_end:'2013-01-02 04:20:00', title:'Jaka to melodia?', subtitle:'', episode_num:'', main_category:'Leisure hobbies', category:'fina\xc5\x82 grudnia', desc:'W prowadzonym przez Roberta Janowskiego programie uczestnicy odgaduj\xc4\x85 znane przeboje muzyki rozrywkowej.\\n')",
  "Event(channel_id:'TVP-1', channel_name:'TVP 1', time_start:'2013-01-02 04:20:00', time_end:'2013-01-02 04:20:00', title:'Zako\xc5\x84czenie programu', subtitle:'', episode_num:'', main_category:'News/Current affairs', category:'', desc:'')",
  "Event(channel_id:'TVP-1', channel_name:'TVP 1', time_start:'2013-01-02 04:20:00', time_end:'2013-01-02 05:25:00', title:'Zako\xc5\x84czenie programu', subtitle:'', episode_num:'', main_category:'News/Current affairs', category:'', desc:'')",
  "Event(channel_id:'TVP-1', channel_name:'TVP 1', time_start:'2013-01-02 05:25:00', time_end:'2013-01-02 07:00:00', title:'Legenda', subtitle:'', episode_num:'', main_category:'Movie/Drama', category:'film fantasy, Wielka Brytania/USA 1985', desc:'Nominacja do Oscara za charakteryzacj\xc4\x99.\\n')",
  "Event(channel_id:'TVP-1', channel_name:'TVP 1', time_start:'2013-01-02 07:00:00', time_end:'2013-01-02 08:00:00', title:'Transmisja mszy \xc5\x9bwi\xc4\x99tej z Sanktuarium Bo\xc5\xbcego Mi\xc5\x82osierdzia w Krakowie-\xc5\x81agiewnikach', subtitle:'', episode_num:'', main_category:'News/Current affairs', category:'', desc:'Zobaczymy transmisj\xc4\x99 mszy \xc5\x9bwi\xc4\x99tej odprawianej w Sanktuarium Bo\xc5\xbcego Mi\xc5\x82osierdzia znajduj\xc4\x85cego si\xc4\x99 w Krakowie \xc5\x81agiewnikach.\\n')",
  "Event(channel_id:'TVP-1', channel_name:'TVP 1', time_start:'2013-01-02 08:00:00', time_end:'2013-01-02 09:25:00', title:'Niebieski s\xc5\x82o\xc5\x84', subtitle:'', episode_num:'', main_category:'Children's/Youth programmes', category:'film animowany, Tajlandia 2008', desc:'Birma\xc5\x84czycy rozbijaj\xc4\x85 ob\xc3\xb3z. Ma\xc5\x82y s\xc5\x82onik Khan Kluay zakrada si\xc4\x99 tam w poszukiwaniu taty i omal nie zostaje pojmany. Pomaga mu ...\\n')",
  "Event(channel_id:'TVP-1', channel_name:'TVP 1', time_start:'2013-01-02 09:25:00', time_end:'2013-01-02 11:00:00', title:'Skok z kosmosu. Felix Baumgartner', subtitle:'', episode_num:'', main_category:'Movie/Drama', category:'film dokumentalny, Wielka Brytania 2012', desc:'14 pa\xc5\xbadziernika 2012 r. austriacki spadochroniarz Felix Baumgartner wykona\xc5\x82 skok ze stratosfery, bij\xc4\x85c m.in. rekord wysoko\xc5\x9bci skoku.\\n')",
  "Event(channel_id:'TVP-1', channel_name:'TVP 1', time_start:'2013-01-02 11:00:00', time_end:'2013-01-02 12:00:00', title:'Sportowe wydarzenia 2012', subtitle:'', episode_num:'', main_category:'Sports', category:'magazyn sportowy', desc:'')",
  "Event(channel_id:'TVP-1', channel_name:'TVP 1', time_start:'2013-01-02 12:00:00', time_end:'2013-01-02 12:15:00', title:'Anio\xc5\x82 Pa\xc5\x84ski', subtitle:'', episode_num:'', main_category:'News/Current affairs', category:'', desc:'Transmisja tradycyjnej modlitwy Anio\xc5\x82 Pa\xc5\x84ski odmawianej z wiernymi przez Ojca \xc5\x9awi\xc4\x99tego w Bazylice \xc5\x9awi\xc4\x99tego Piotra w Watykanie.\\n')",
  "Event(channel_id:'TVP-1', channel_name:'TVP 1', time_start:'2013-01-02 12:15:00', time_end:'2013-01-02 13:50:00', title:'Podr\xc3\xb3\xc5\xbc do wn\xc4\x99trza Ziemi', subtitle:'', episode_num:'', main_category:'Movie/Drama', category:'film przygodowy, Kanada/USA 2008', desc:'XIX wiek. Do prof. Brocka przychodzi \xc5\xbcona jego kolegi, kt\xc3\xb3ry nie wr\xc3\xb3ci\xc5\x82 z wyprawy do wn\xc4\x99trza Ziemi. Ma map\xc4\x99 z ...\\n')",
  "Event(channel_id:'TVP-1', channel_name:'TVP 1', time_start:'2013-01-02 13:50:00', time_end:'2013-01-02 14:00:00', title:'Skoki narciarskie: Turniej Czterech Skoczni w Garmisch-Partenkirchen', subtitle:'', episode_num:'', main_category:'Sports', category:'studio', desc:'')",
  "Event(channel_id:'TVP-1', channel_name:'TVP 1', time_start:'2013-01-02 14:00:00', time_end:'2013-01-02 16:10:00', title:'Skoki narciarskie: Turniej Czterech Skoczni w Garmisch-Partenkirchen', subtitle:'', episode_num:'', main_category:'Sports', category:'skoki narciarskie', desc:'Noworoczny konkurs w Garmisch- Partenkirchen to drugie zawody Turnieju Czterech Skoczni. Jednym z faworyt\xc3\xb3w jest Gregor Schlierenzauer.\\n')",
  "Event(channel_id:'TVP-1', channel_name:'TVP 1', time_start:'2013-01-02 16:10:00', time_end:'2013-01-02 16:25:00', title:'Tylko hity! Opole 2012: Maciej Stuhr', subtitle:'', episode_num:'', main_category:'Leisure hobbies', category:'koncert', desc:'Przegl\xc4\x85d najwi\xc4\x99kszych przeboj\xc3\xb3w, jakie zosta\xc5\x82y zaprezentowane podczas koncert\xc3\xb3w na tegorocznym, 49. KFPP w Opolu.\\n')",
  "Event(channel_id:'TVP-1', channel_name:'TVP 1', time_start:'2013-01-02 16:25:00', time_end:'2013-01-02 16:55:00', title:'Gwiazdy w Jedynce: II Divo', subtitle:'', episode_num:'', main_category:'Leisure hobbies', category:'koncert', desc:'')",
  "Event(channel_id:'TVP-1', channel_name:'TVP 1', time_start:'2013-01-02 16:55:00', time_end:'2013-01-02 17:10:00', title:'Teleexpress', subtitle:'', episode_num:'', main_category:'News/Current affairs', category:'', desc:'Dynamicznie prowadzony serwis informacyjny prezentuj\xc4\x85cy aktualne wydarzenia, wiadomo\xc5\x9bci kulturalne oraz ciekawostki z kraju i ze \xc5\x9bwiata.\\n')",
  "Event(channel_id:'TVP-1', channel_name:'TVP 1', time_start:'2013-01-02 17:10:00', time_end:'2013-01-02 17:15:00', title:'Pogoda', subtitle:'', episode_num:'', main_category:'News/Current affairs', category:'', desc:'Szczeg\xc3\xb3\xc5\x82owe informacje na temat stanu pogody w najbli\xc5\xbcszych dniach.\\n')",
  "Event(channel_id:'TVP-1', channel_name:'TVP 1', time_start:'2013-01-02 17:15:00', time_end:'2013-01-02 17:45:00', title:'Jaka to melodia?', subtitle:'', episode_num:'', main_category:'Leisure hobbies', category:'fina\xc5\x82 roku', desc:'W prowadzonym przez Roberta Janowskiego programie uczestnicy odgaduj\xc4\x85 znane przeboje muzyki rozrywkowej.\\n')",
  "Event(channel_id:'TVP-1', channel_name:'TVP 1', time_start:'2013-01-02 17:45:00', time_end:'2013-01-02 19:30:00', title:'Wall-E', subtitle:'', episode_num:'', main_category:'Children's/Youth programmes', category:'film animowany, USA 2008', desc:'Historia mi\xc5\x82o\xc5\x9bci dwojga robot\xc3\xb3w.\\n')",
  "Event(channel_id:'TVP-1', channel_name:'TVP 1', time_start:'2013-01-02 19:30:00', time_end:'2013-01-02 20:00:00', title:'Wiadomo\xc5\x9bci', subtitle:'', episode_num:'', main_category:'News/Current affairs', category:'', desc:'Serwis informacyjny prezentuj\xc4\x85cy najnowsze wydarzenia z kraju i ze \xc5\x9bwiata, m.in. z dziedziny polityki, gospodarki, kultury.\\n')",
  "Event(channel_id:'TVP-1', channel_name:'TVP 1', time_start:'2013-01-02 20:00:00', time_end:'2013-01-02 20:05:00', title:'Sport', subtitle:'', episode_num:'', main_category:'Sports', category:'', desc:'Przegl\xc4\x85d najwa\xc5\xbcniejszych aktualnych wydarze\xc5\x84 sportowych ze szczeg\xc3\xb3lnym uwzgl\xc4\x99dnieniem osi\xc4\x85gni\xc4\x99\xc4\x87 polskich zawodnik\xc3\xb3w.\\n')",
  "Event(channel_id:'TVP-1', channel_name:'TVP 1', time_start:'2013-01-02 20:05:00', time_end:'2013-01-02 20:20:00', title:'Pogoda', subtitle:'', episode_num:'', main_category:'News/Current affairs', category:'', desc:'Szczeg\xc3\xb3\xc5\x82owe informacje na temat stanu pogody w najbli\xc5\xbcszych dniach.\\n')",
  "Event(channel_id:'TVP-1', channel_name:'TVP 1', time_start:'2013-01-02 20:20:00', time_end:'2013-01-02 22:05:00', title:'Legalna blondynka', subtitle:'', episode_num:'', main_category:'Movie/Drama', category:'komedia, USA 2001', desc:'Pi\xc4\x99kna Elle chce udowodni\xc4\x87 by\xc5\x82emu ukochanemu, \xc5\xbce nie tylko uroda jest jej atutem.\\n')",
  "Event(channel_id:'TVP-1', channel_name:'TVP 1', time_start:'2013-01-02 22:05:00', time_end:'2013-01-02 23:55:00', title:'Liberator 2', subtitle:'', episode_num:'', main_category:'Movie/Drama', category:'film sensacyjny, USA 1995', desc:'Terrory\xc5\x9bci opanowuj\xc4\x85 luksusowy poci\xc4\x85g. W\xc5\x9br\xc3\xb3d pasa\xc5\xbcer\xc3\xb3w jest komandos.\\n')",
  "Event(channel_id:'TVP-1', channel_name:'TVP 1', time_start:'2013-01-02 23:55:00', time_end:'2013-01-02 01:20:00', title:'Hell Ride', subtitle:'', episode_num:'', main_category:'Movie/Drama', category:'film sensacyjny, USA 2008', desc:'Johnny zwany Pistolero jest przyw\xc3\xb3dc\xc4\x85 gangu motocyklowego\\n'\\nThe Victors\\n'\\n. Jego celem jest zemsta na liderach grupy\\n'\\nThe 666ers\\n'\\n.\\n')",
  "Event(channel_id:'TVP-1', channel_name:'TVP 1', time_start:'2013-01-02 01:20:00', time_end:'2013-01-02 03:20:00', title:'Underworld', subtitle:'', episode_num:'', main_category:'Movie/Drama', category:'horror, Niemcy/Wielka Brytania/USA/W\xc4\x99gry 2003', desc:'Student trafia w \xc5\x9brodek wojny tocz\xc4\x85cej si\xc4\x99 mi\xc4\x99dzy wampirami a wilko\xc5\x82akami.\\n')",
  "Event(channel_id:'TVP-1', channel_name:'TVP 1', time_start:'2013-01-02 03:20:00', time_end:'2013-01-02 04:20:00', title:'Zagadkowa Jedynka', subtitle:'', episode_num:'', main_category:'Leisure hobbies', category:'program rozrywkowy', desc:'W tej zabawie do zdobycia s\xc4\x85 nagrody pieni\xc4\x99\xc5\xbcne. Wystarczy telefonicznie lub za pomoc\xc4\x85 sms-a poda\xc4\x87 prawid\xc5\x82owe rozwi\xc4\x85zanie zagadki s\xc5\x82ownej.\\n')",
  "Event(channel_id:'TVP-1', channel_name:'TVP 1', time_start:'2013-01-02 04:20:00', time_end:'2013-01-02 04:20:00', title:'Zako\xc5\x84czenie programu', subtitle:'', episode_num:'', main_category:'News/Current affairs', category:'', desc:'')"]
        self.assertEqual(events, expected)



if __name__ == '__main__':
    unittest.main()
